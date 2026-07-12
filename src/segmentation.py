"""Rule-based customer segmentation for churn risk and retention targeting."""

from __future__ import annotations

import pandas as pd


def assign_risk_segment(row: pd.Series) -> str:
    """Assign a simple, explainable churn-risk segment to a customer row.

    Args:
        row: A row of the cleaned churn DataFrame.

    Returns:
        One of "High Risk", "Medium Risk", or "Low Risk".
    """
    is_month_to_month = str(row.get("contract_type", "")).strip().lower() == "month-to-month"
    low_tenure = row.get("tenure_months", 0) <= 6
    high_charges = row.get("monthly_charges", 0) >= 70

    if is_month_to_month and low_tenure:
        return "High Risk"
    if is_month_to_month and high_charges:
        return "Medium Risk"
    return "Low Risk"


def add_risk_segment(df: pd.DataFrame) -> pd.DataFrame:
    """Add a risk_segment column to the DataFrame using simple business rules.

    Args:
        df: Cleaned churn DataFrame.

    Returns:
        DataFrame with an added risk_segment column.
    """
    df = df.copy()
    df["risk_segment"] = df.apply(assign_risk_segment, axis=1)
    return df


def segment_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize churn rate and customer count by risk segment.

    Args:
        df: DataFrame that already has a risk_segment column (see add_risk_segment).

    Returns:
        DataFrame with churn rate and customer count per segment.
    """
    working = df.assign(is_churned=(df["churn"].str.lower() == "yes").astype(int))
    summary = (
        working.groupby("risk_segment", as_index=False)
        .agg(n_customers=("customer_id", "nunique"), churn_rate_pct=("is_churned", "mean"))
    )
    summary["churn_rate_pct"] = (summary["churn_rate_pct"] * 100).round(2)
    return summary.sort_values("churn_rate_pct", ascending=False).reset_index(drop=True)
