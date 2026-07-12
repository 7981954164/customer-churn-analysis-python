"""Customer Lifetime Value (CLV) estimation for the churn dataset.

Uses a simple, explainable approximation:
    CLV = average_monthly_charges * expected_tenure_months
This is intentionally simple so it is easy to explain to stakeholders;
see Future Improvements in the README for more advanced approaches.
"""

from __future__ import annotations

import pandas as pd


def add_estimated_clv(df: pd.DataFrame) -> pd.DataFrame:
    """Add an estimated_clv column using monthly charges and tenure.

    Args:
        df: Cleaned churn DataFrame with monthly_charges and tenure_months.

    Returns:
        DataFrame with an added estimated_clv column.
    """
    df = df.copy()
    df["estimated_clv"] = (df["monthly_charges"] * df["tenure_months"]).round(2)
    return df


def clv_summary_by_segment(df: pd.DataFrame, segment_col: str = "risk_segment") -> pd.DataFrame:
    """Summarize average estimated CLV by a segment column.

    Args:
        df: DataFrame that already has an estimated_clv column.
        segment_col: Column name to group by, e.g. risk_segment or contract_type.

    Returns:
        DataFrame with average CLV and customer count per segment.
    """
    return (
        df.groupby(segment_col, as_index=False)
        .agg(avg_clv=("estimated_clv", "mean"), n_customers=("customer_id", "nunique"))
        .round(2)
        .sort_values("avg_clv", ascending=False)
        .reset_index(drop=True)
    )


def clv_at_risk(df: pd.DataFrame) -> float:
    """Estimate total CLV currently at risk among churned customers.

    Args:
        df: DataFrame with estimated_clv and churn columns.

    Returns:
        Sum of estimated CLV for customers who have already churned.
    """
    churned = df[df["churn"].str.lower() == "yes"]
    return float(churned["estimated_clv"].sum().round(2))
