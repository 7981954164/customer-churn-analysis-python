# Processed Data

This folder receives the cleaned dataset produced by running the pipeline:

```bash
python -m src.main --input data/raw/sample_churn_data.csv
```

The output file cleaned_churn_data.csv will contain the cleaned dataset with added risk_segment and estimated_clv columns. This folder is empty until you run the pipeline.
