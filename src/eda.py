"""Exploratory data analysis functions for the customer churn dataset."""

from __future__ import annotations

import pandas as pd


def churn_rate(df: pd.DataFrame) -> float:
    """Return the overall churn rate as a percentage.

    Args:
        df: Cleaned churn DataFrame with a churn column (Yes/No).

    Returns:
        Churn rate as a percentage rounded to 2 decimal places.
    """
    total = len(df)
    if total == 0:
        return 0.0
    churned = (df["churn"].str.lower() == "yes").sum()
    return round(churned / total * 100, 2)


def retention_rate(df: pd.DataFrame) -> float:
    """Return the overall retention rate as a percentage."""
    return round(100 - churn_rate(df), 2)


def churn_by_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Compute churn rate broken down by a categorical column.

    Args:
        df: Cleaned churn DataFrame.
        column: Column to group by, e.g. contract_type or gender.

    Returns:
        DataFrame with churn rate and customer count per group.
    """
    grouped = (
        df.assign(is_churned=(df["churn"].str.lower() == "yes").astype(int))
        .groupby(column, as_index=False)
        .agg(n_customers=("customer_id", "nunique"), churn_rate_pct=("is_churned", "mean"))
    )
    grouped["churn_rate_pct"] = (grouped["churn_rate_pct"] * 100).round(2)
    return grouped.sort_values("churn_rate_pct", ascending=False).reset_index(drop=True)


def tenure_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Compare average tenure between churned and retained customers.

    Args:
        df: Cleaned churn DataFrame.

    Returns:
        DataFrame with average tenure per churn status.
    """
    return (
        df.groupby("churn", as_index=False)
        .agg(avg_tenure_months=("tenure_months", "mean"), n_customers=("customer_id", "nunique"))
        .round(2)
    )


def monthly_charges_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Compare average monthly charges between churned and retained customers.

    Args:
        df: Cleaned churn DataFrame.

    Returns:
        DataFrame with average monthly charges per churn status.
    """
    return (
        df.groupby("churn", as_index=False)
        .agg(avg_monthly_charges=("monthly_charges", "mean"), n_customers=("customer_id", "nunique"))
        .round(2)
    )


def demographic_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Compute churn rate by a combination of gender and senior citizen status.

    Args:
        df: Cleaned churn DataFrame.

    Returns:
        DataFrame with churn rate per demographic group.
    """
    grouped = (
        df.assign(is_churned=(df["churn"].str.lower() == "yes").astype(int))
        .groupby(["gender", "senior_citizen"], as_index=False)
        .agg(n_customers=("customer_id", "nunique"), churn_rate_pct=("is_churned", "mean"))
    )
    grouped["churn_rate_pct"] = (grouped["churn_rate_pct"] * 100).round(2)
    return grouped
