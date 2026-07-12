"""Data cleaning utilities for the customer churn dataset.

Loads raw churn data, assesses data quality, cleans it, and prepares
it for downstream churn analysis, segmentation, and CLV estimation.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd

from src.utils import get_logger

logger = get_logger(__name__)

REQUIRED_COLUMNS = [
    "customer_id",
    "gender",
    "senior_citizen",
    "partner",
    "dependents",
    "tenure_months",
    "contract_type",
    "monthly_charges",
    "total_charges",
    "internet_service",
    "tech_support",
    "churn",
]


def load_raw_data(path: Path) -> pd.DataFrame:
    """Load the raw churn CSV file into a DataFrame.

    Args:
        path: Path to the raw CSV file.

    Returns:
        Raw, uncleaned DataFrame.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If required columns are missing.
    """
    if not path.exists():
        raise FileNotFoundError(f"Raw data file not found: {path}")

    df = pd.read_csv(path)
    missing_cols = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {sorted(missing_cols)}")

    logger.info("Loaded raw churn data with shape %s from %s", df.shape, path)
    return df


def generate_data_quality_report(df: pd.DataFrame) -> Dict[str, object]:
    """Generate a summary data-quality report for the given DataFrame.

    Args:
        df: DataFrame to inspect.

    Returns:
        Dictionary summarizing shape, dtypes, missing values, and duplicates.
    """
    report: Dict[str, object] = {
        "n_rows": len(df),
        "n_columns": df.shape[1],
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isna().sum().to_dict(),
        "missing_pct": (df.isna().mean() * 100).round(2).to_dict(),
        "n_duplicate_rows": int(df.duplicated().sum()),
    }
    logger.info(
        "Data quality report: %s rows, %s duplicate rows",
        report["n_rows"],
        report["n_duplicate_rows"],
    )
    return report


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Handle missing values using column-appropriate strategies.

    Args:
        df: DataFrame with potential missing values.

    Returns:
        DataFrame with missing values handled.
    """
    df = df.copy()
    before = len(df)
    df = df.dropna(subset=["customer_id"])
    dropped = before - len(df)
    if dropped:
        logger.info("Dropped %s rows missing customer_id", dropped)

    numeric_cols = ["tenure_months", "monthly_charges", "total_charges"]
    for col in numeric_cols:
        if col in df.columns and df[col].isna().any():
            median_value = df[col].median()
            df[col] = df[col].fillna(median_value)
            logger.info("Filled missing values in %s with median=%.2f", col, median_value)

    categorical_cols = ["gender", "partner", "dependents", "contract_type", "internet_service", "tech_support", "churn"]
    for col in categorical_cols:
        if col in df.columns and df[col].isna().any():
            df[col] = df[col].fillna("Unknown")
            logger.info("Filled missing values in %s with 'Unknown'", col)

    return df


def remove_duplicates(df: pd.DataFrame, subset: list[str] | None = None) -> pd.DataFrame:
    """Remove duplicate rows from the DataFrame.

    Args:
        df: Input DataFrame.
        subset: Optional list of columns to consider for duplication.

    Returns:
        DataFrame without duplicate rows.
    """
    before = len(df)
    df = df.drop_duplicates(subset=subset).reset_index(drop=True)
    removed = before - len(df)
    if removed:
        logger.info("Removed %s duplicate rows", removed)
    return df


def fix_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Coerce columns to their expected data types.

    Args:
        df: Input DataFrame.

    Returns:
        DataFrame with corrected dtypes.
    """
    df = df.copy()
    df["senior_citizen"] = pd.to_numeric(df["senior_citizen"], errors="coerce").astype("Int64")
    df["tenure_months"] = pd.to_numeric(df["tenure_months"], errors="coerce")
    for col in ["monthly_charges", "total_charges"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in ["customer_id", "gender", "partner", "dependents", "contract_type", "internet_service", "tech_support", "churn"]:
        df[col] = df[col].astype("string")

    return df


def clean_pipeline(raw_path: Path) -> tuple[pd.DataFrame, Dict[str, object]]:
    """Run the full cleaning pipeline on the raw churn data.

    Args:
        raw_path: Path to the raw CSV file.

    Returns:
        A tuple of (cleaned_dataframe, data_quality_report_before_cleaning).
    """
    raw_df = load_raw_data(raw_path)
    quality_report = generate_data_quality_report(raw_df)

    df = handle_missing_values(raw_df)
    df = remove_duplicates(df, subset=["customer_id"])
    df = fix_data_types(df)

    logger.info("Cleaning pipeline complete. Final shape: %s", df.shape)
    return df, quality_report
