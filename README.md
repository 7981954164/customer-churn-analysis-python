# Customer Churn Analysis

![Python](https://img.shields.io/badge/Python-3.13-blue.svg) ![Pandas](https://img.shields.io/badge/Pandas-2.x-150458.svg) ![License](https://img.shields.io/badge/License-MIT-green.svg) ![Status](https://img.shields.io/badge/Status-Portfolio%20Project-orange.svg)

An intermediate-level data analytics project that explores customer churn for a subscription-style business, segments customers, estimates customer lifetime value, and produces retention recommendations using Python, pandas, NumPy, Matplotlib, and Seaborn.

**Note on outputs:** This repository ships with a small, hand-authored sample dataset (`data/raw/sample_churn_data.csv`) and fully implemented analysis code in `src/`. Charts and summary tables under `outputs/` and `images/` are generated when you run the pipeline (`python -m src.main`). They are not pre-computed in this repository. Any figures mentioned below are illustrative placeholders describing the shape of the analysis, not verified results.

## Table of Contents
- [Business Problem](#business-problem)
- [Objectives](#objectives)
- [Key Performance Indicators](#key-performance-indicators)
- [Project Structure](#project-structure)
- [Dataset](#dataset)
- [Installation](#installation)
- [Usage](#usage)
- [Analysis Workflow](#analysis-workflow)
- [Sample Visualizations](#sample-visualizations)
- [Business Insights](#business-insights)
- [Business Recommendations](#business-recommendations)
- [Future Improvements](#future-improvements)
- [License](#license)

## Business Problem

A subscription business is losing customers (churn) and wants to understand who is churning, why, and what it is worth to retain them. Leadership needs a repeatable analysis of demographics, contract type, tenure, and monthly charges to prioritize retention spend and estimate the financial impact of churn.

## Objectives

1. Clean and prepare raw customer churn data, handling missing values, duplicates, and data types.
2. Analyze churn rate and retention rate overall and across key customer segments.
3. Examine the relationship between churn and contract type, tenure, and monthly charges.
4. Segment customers using simple, explainable rules for targeted retention campaigns.
5. Estimate customer lifetime value (CLV) to prioritize retention investment.
6. Deliver clear, actionable business recommendations for reducing churn.

## Key Performance Indicators

| KPI | Description |
|---|---|
| Churn Rate % | Share of customers who have churned |
| Retention Rate % | 100% minus churn rate |
| Average Tenure (months) | Average customer tenure, churned vs retained |
| Average Monthly Charges | Average monthly spend, churned vs retained |
| Estimated CLV | Average monthly charges times average tenure |
| Churn Rate by Contract Type | Month-to-month vs one/two year contracts |
| Churn Rate by Segment | Demographic and usage-based segments |

## Project Structure

```
customer-churn-analysis-python/
assets/                  - design assets such as banners and icons
data/raw/                - original or sample raw churn data
data/processed/          - cleaned data exported by the pipeline
images/                  - exported chart images (PNG)
notebooks/               - demo notebook showing usage of src/
outputs/                 - exported summary tables and reports
src/__init__.py
src/data_cleaning.py     - missing values, duplicates, dtypes
src/eda.py               - churn rate, demographics, contract analysis
src/segmentation.py      - rule-based customer segmentation
src/clv.py               - customer lifetime value estimation
src/visualization.py     - chart generation using matplotlib and seaborn
src/utils.py             - shared helpers and logging setup
src/main.py              - CLI entry point orchestrating the pipeline
.gitignore
LICENSE
requirements.txt
README.md
```

## Dataset

The sample dataset (`data/raw/sample_churn_data.csv`) mirrors the structure of a typical telecom or subscription churn export, with the following columns:

| Column | Type | Description |
|---|---|---|
| customer_id | string | Unique customer identifier |
| gender | string | Customer gender |
| senior_citizen | integer | 1 if senior citizen, else 0 |
| partner | string | Whether the customer has a partner (Yes/No) |
| dependents | string | Whether the customer has dependents (Yes/No) |
| tenure_months | integer | Number of months the customer has stayed |
| contract_type | string | Month-to-month, One year, or Two year |
| monthly_charges | float | Current monthly charge amount |
| total_charges | float | Total amount charged to date |
| internet_service | string | Type of internet service, if any |
| tech_support | string | Whether the customer has tech support (Yes/No) |
| churn | string | Whether the customer churned (Yes/No) |

To use your own data, replace the CSV in `data/raw/` with a file following this schema, or adjust the column mapping in `src/data_cleaning.py`.

## Installation

```bash
git clone https://github.com/7981954164/customer-churn-analysis-python.git
cd customer-churn-analysis-python

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

On Windows, activate the virtual environment with `.venv\Scripts\activate` instead.

## Usage

```bash
python -m src.main --input data/raw/sample_churn_data.csv --outdir outputs
```

This will load and clean the raw CSV, export the cleaned dataset to `data/processed/cleaned_churn_data.csv`, compute churn KPIs and segment summaries to `outputs/`, and generate and save charts to `images/`.

You can also open `notebooks/01_churn_analysis_demo.ipynb` for a guided, cell-by-cell walkthrough using the functions in `src/`.

## Analysis Workflow

1. Data Understanding: inspect schema, dtypes, missing values, and duplicates.
2. Data Cleaning: impute or drop missing values, fix dtypes, remove duplicates.
3. Exploratory Data Analysis: churn rate, demographics, contract type, tenure, and monthly charges.
4. Customer Segmentation: simple rule-based segments (for example high-risk month-to-month customers with low tenure).
5. Customer Lifetime Value Estimation: approximate CLV from tenure and monthly charges.
6. Visualization: bar, line, histogram, scatter, and pie charts saved as PNGs.
7. Insights and Recommendations: written up in this README and outputs/business_insights.md.

## Sample Visualizations

Running the pipeline generates charts such as:

- images/churn_rate_overall.png - pie chart of overall churn vs retention
- images/churn_by_contract_type.png - bar chart of churn rate by contract type
- images/tenure_distribution.png - histogram of customer tenure
- images/monthly_charges_by_churn.png - box or bar comparison of monthly charges
- images/churn_by_segment.png - bar chart of churn rate by customer segment
- images/clv_distribution.png - histogram of estimated customer lifetime value
- images/tenure_vs_monthly_charges_scatter.png - scatter plot of tenure vs monthly charges

These are generated locally when you run python -m src.main. They are not committed as pre-rendered images since no code has been executed in this environment.

## Business Insights

The following are illustrative example insight statements in the format the pipeline is designed to produce. Run the pipeline on real data to generate verified, numeric findings for your own dataset.

1. Month-to-month contracts typically churn at a much higher rate than annual contracts.
2. Customers with low tenure are usually at higher risk of churning than long-tenured customers.
3. Higher monthly charges can correlate with higher churn among month-to-month customers.
4. Customers without tech support often churn more than those with tech support.
5. Senior citizens may churn at different rates than non-senior customers, worth investigating separately.
6. Customers without a partner or dependents can show different retention patterns than those with family ties.
7. Estimated CLV is usually lower for high-churn-risk segments, compounding the cost of losing them.
8. A small number of high-value, low-tenure customers may represent an urgent retention priority.
9. Internet service type can be associated with materially different churn rates.
10. Bundled services (for example tech support plus internet) often correlate with lower churn.
11. Early-tenure customers (first few months) are frequently the highest-risk group for churn.
12. Contract type is often one of the strongest single predictors of churn risk.
13. Segmentation can reveal that a minority of segments account for a majority of churned revenue.
14. Retention offers targeted at month-to-month customers may have the highest ROI.
15. Long-term contract incentives can materially reduce churn among price-sensitive segments.

## Business Recommendations

- Prioritize retention outreach for month-to-month customers with low tenure and high monthly charges.
- Offer incentives to migrate high-risk month-to-month customers to annual contracts.
- Bundle tech support or additional services for customers who currently lack them.
- Build a simple early-warning segment for customers in their first few months of tenure.
- Track churn rate and CLV by segment monthly to measure the impact of retention campaigns.
- Set up a recurring, for example monthly, run of this pipeline to keep churn KPIs current.

Manager Actions Checklist:
- Review the churn-by-contract-type chart and prioritize month-to-month customers for outreach.
- Review the CLV distribution to identify high-value customers at risk.
- Feed data/processed/cleaned_churn_data.csv into the BI tool of choice such as Power BI or Tableau.
- Schedule a monthly re-run of the pipeline as new data arrives.

## Executive Summary

This project delivers a reusable pipeline that turns raw customer churn exports into clean data, churn and retention KPIs, customer segments, and CLV estimates. It is designed so a retention or customer success team can run one command and receive a cleaned CSV plus a folder of charts and summary tables highlighting where churn risk is concentrated.

## Future Improvements

- Add a simple logistic regression or decision tree churn-propensity model.
- Add automated tests using pytest for the src modules.
- Add a lightweight Streamlit dashboard on top of outputs.
- Add continuous integration with GitHub Actions to lint and test on every push.
- Add cohort-based retention curves over time.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Author

Maintained as a data analytics portfolio project.
