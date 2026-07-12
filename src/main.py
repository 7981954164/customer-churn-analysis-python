"""CLI entry point orchestrating the customer churn analysis pipeline.

Usage:
    python -m src.main --input data/raw/sample_churn_data.csv --outdir outputs
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src import clv, eda, segmentation, visualization
from src.data_cleaning import clean_pipeline
from src.utils import ensure_dir, get_logger

logger = get_logger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run the customer churn analysis pipeline.")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/raw/sample_churn_data.csv"),
        help="Path to the raw churn CSV file.",
    )
    parser.add_argument(
        "--outdir",
        type=Path,
        default=Path("outputs"),
        help="Directory to write summary tables and reports to.",
    )
    parser.add_argument(
        "--imagesdir",
        type=Path,
        default=Path("images"),
        help="Directory to write chart images to.",
    )
    parser.add_argument(
        "--processed-dir",
        type=Path,
        default=Path("data/processed"),
        help="Directory to write the cleaned dataset to.",
    )
    return parser.parse_args()


def run(input_path: Path, outdir: Path, imagesdir: Path, processed_dir: Path) -> None:
    """Run the end-to-end pipeline: clean, analyze, segment, visualize, export.

    Args:
        input_path: Path to the raw churn CSV file.
        outdir: Directory to write summary tables and reports to.
        imagesdir: Directory to write chart images to.
        processed_dir: Directory to write the cleaned dataset to.
    """
    ensure_dir(outdir)
    ensure_dir(imagesdir)
    ensure_dir(processed_dir)

    logger.info("Starting churn pipeline for %s", input_path)
    df, quality_report = clean_pipeline(input_path)
    df = segmentation.add_risk_segment(df)
    df = clv.add_estimated_clv(df)

    cleaned_path = processed_dir / "cleaned_churn_data.csv"
    df.to_csv(cleaned_path, index=False)
    logger.info("Exported cleaned dataset to %s", cleaned_path)

    with open(outdir / "data_quality_report.json", "w", encoding="utf-8") as fh:
        json.dump(quality_report, fh, indent=2, default=str)

    churn_by_contract = eda.churn_by_column(df, "contract_type")
    tenure_summary = eda.tenure_summary(df)
    monthly_charges_summary = eda.monthly_charges_summary(df)
    segment_summary = segmentation.segment_summary(df)
    clv_by_segment = clv.clv_summary_by_segment(df)

    churn_by_contract.to_csv(outdir / "churn_by_contract_type.csv", index=False)
    tenure_summary.to_csv(outdir / "tenure_summary.csv", index=False)
    monthly_charges_summary.to_csv(outdir / "monthly_charges_summary.csv", index=False)
    segment_summary.to_csv(outdir / "segment_summary.csv", index=False)
    clv_by_segment.to_csv(outdir / "clv_by_segment.csv", index=False)

    kpi_summary = {
        "churn_rate_pct": eda.churn_rate(df),
        "retention_rate_pct": eda.retention_rate(df),
        "total_clv_at_risk": clv.clv_at_risk(df),
        "total_customers": int(df["customer_id"].nunique()),
    }
    with open(outdir / "kpi_summary.json", "w", encoding="utf-8") as fh:
        json.dump(kpi_summary, fh, indent=2)
    logger.info("KPI summary: %s", kpi_summary)

    visualization.plot_churn_rate_overall(df, imagesdir / "churn_rate_overall.png")
    visualization.plot_churn_by_contract_type(churn_by_contract, imagesdir / "churn_by_contract_type.png")
    visualization.plot_tenure_distribution(df, imagesdir / "tenure_distribution.png")
    visualization.plot_monthly_charges_by_churn(df, imagesdir / "monthly_charges_by_churn.png")
    visualization.plot_churn_by_segment(segment_summary, imagesdir / "churn_by_segment.png")
    visualization.plot_clv_distribution(df, imagesdir / "clv_distribution.png")
    visualization.plot_tenure_vs_monthly_charges(df, imagesdir / "tenure_vs_monthly_charges_scatter.png")

    logger.info("Pipeline complete. Outputs written to %s and %s", outdir, imagesdir)


def main() -> None:
    """Entry point for command-line execution."""
    args = parse_args()
    run(args.input, args.outdir, args.imagesdir, args.processed_dir)


if __name__ == "__main__":
    main()
