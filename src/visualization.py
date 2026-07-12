"""Chart generation for the customer churn analysis pipeline.

All functions save a matplotlib/seaborn figure to disk and return the
path, so they can be used both from scripts and notebooks.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams["figure.dpi"] = 120


def _save_fig(fig: plt.Figure, out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    return out_path


def plot_churn_rate_overall(df: pd.DataFrame, out_path: Path) -> Path:
    """Pie chart of overall churn vs retention.

    Args:
        df: Cleaned churn DataFrame.
        out_path: File path to save the PNG chart to.

    Returns:
        Path to the saved image.
    """
    counts = df["churn"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(counts, labels=counts.index, autopct="%1.1f%%", colors=["#16a34a", "#dc2626"], startangle=90)
    ax.set_title("Overall Churn vs Retention")
    return _save_fig(fig, out_path)


def plot_churn_by_contract_type(churn_by_contract: pd.DataFrame, out_path: Path) -> Path:
    """Bar chart of churn rate by contract type.

    Args:
        churn_by_contract: Output of eda.churn_by_column(df, "contract_type").
        out_path: File path to save the PNG chart to.

    Returns:
        Path to the saved image.
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=churn_by_contract, x="contract_type", y="churn_rate_pct", ax=ax, color="#2563eb")
    ax.set_title("Churn Rate by Contract Type")
    ax.set_xlabel("Contract Type")
    ax.set_ylabel("Churn Rate (%)")
    return _save_fig(fig, out_path)


def plot_tenure_distribution(df: pd.DataFrame, out_path: Path) -> Path:
    """Histogram of customer tenure.

    Args:
        df: Cleaned churn DataFrame.
        out_path: File path to save the PNG chart to.

    Returns:
        Path to the saved image.
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df["tenure_months"], bins=30, color="#0891b2", edgecolor="white")
    ax.set_title("Customer Tenure Distribution")
    ax.set_xlabel("Tenure (months)")
    ax.set_ylabel("Frequency")
    return _save_fig(fig, out_path)


def plot_monthly_charges_by_churn(df: pd.DataFrame, out_path: Path) -> Path:
    """Box plot comparing monthly charges for churned vs retained customers.

    Args:
        df: Cleaned churn DataFrame.
        out_path: File path to save the PNG chart to.

    Returns:
        Path to the saved image.
    """
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.boxplot(data=df, x="churn", y="monthly_charges", ax=ax, palette=["#16a34a", "#dc2626"])
    ax.set_title("Monthly Charges by Churn Status")
    ax.set_xlabel("Churn")
    ax.set_ylabel("Monthly Charges")
    return _save_fig(fig, out_path)


def plot_churn_by_segment(segment_summary: pd.DataFrame, out_path: Path) -> Path:
    """Bar chart of churn rate by risk segment.

    Args:
        segment_summary: Output of segmentation.segment_summary().
        out_path: File path to save the PNG chart to.

    Returns:
        Path to the saved image.
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=segment_summary, x="risk_segment", y="churn_rate_pct", ax=ax, color="#7c3aed")
    ax.set_title("Churn Rate by Risk Segment")
    ax.set_xlabel("Risk Segment")
    ax.set_ylabel("Churn Rate (%)")
    return _save_fig(fig, out_path)


def plot_clv_distribution(df: pd.DataFrame, out_path: Path) -> Path:
    """Histogram of estimated customer lifetime value.

    Args:
        df: DataFrame with an estimated_clv column.
        out_path: File path to save the PNG chart to.

    Returns:
        Path to the saved image.
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df["estimated_clv"], bins=30, color="#ea580c", edgecolor="white")
    ax.set_title("Estimated Customer Lifetime Value Distribution")
    ax.set_xlabel("Estimated CLV")
    ax.set_ylabel("Frequency")
    return _save_fig(fig, out_path)


def plot_tenure_vs_monthly_charges(df: pd.DataFrame, out_path: Path) -> Path:
    """Scatter plot of tenure vs. monthly charges, colored by churn.

    Args:
        df: Cleaned churn DataFrame.
        out_path: File path to save the PNG chart to.

    Returns:
        Path to the saved image.
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(data=df, x="tenure_months", y="monthly_charges", hue="churn", alpha=0.6, ax=ax)
    ax.set_title("Tenure vs. Monthly Charges")
    ax.set_xlabel("Tenure (months)")
    ax.set_ylabel("Monthly Charges")
    return _save_fig(fig, out_path)
