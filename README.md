# E-commerce Fraud Analytics — Data Analyst Portfolio Project

## Project objective
Analyze e-commerce payment transactions to identify fraud patterns, quantify exposure,
and propose practical monitoring rules. This is a **synthetic portfolio dataset**;
it contains no real customer or payment information.

## Dataset
- File: `transactions.csv`
- Raw rows: 12,036
- Columns: transaction ID/date, customer ID, amount, merchant category, payment method,
  transaction hour, device-change flag, IP risk score, failed attempts, international flag,
  account age, and fraud label.
- The data intentionally includes duplicate transaction rows for a data-quality exercise.
- `is_fraud` is the target label (1 = fraud, 0 = legitimate).

## Business questions
1. What is the overall fraud rate and estimated fraud transaction value?
2. Which payment methods and merchant categories have higher fraud rates?
3. Are overnight, high-value, international, or device-change transactions riskier?
4. How do daily transaction volume and fraud rate change over time?
5. Which customer activity patterns could justify additional verification?

## How to run
Requirements: Python 3.10+, pandas, numpy, matplotlib.

```bash
pip install pandas numpy matplotlib
python analyze.py
```

The script removes duplicate `transaction_id` records and writes KPI and segment outputs
to the `outputs/` directory.

## SQL work
Open `analysis.sql` in PostgreSQL, SQLite (after importing the CSV), or adapt the syntax
to your database. It includes duplicate checks, KPI calculations, segment analysis,
daily monitoring, and customer-level investigation queries.

## Suggested Power BI dashboard
Create a one-page dashboard with:
- KPI cards: total transactions, fraud transactions, fraud rate, fraud value (TRY)
- Line chart: daily fraud rate and transaction count
- Bar chart: fraud rate by payment method and merchant category
- Matrix: transaction hour × amount band, colored by fraud rate
- Slicers: date, payment method, merchant category, international flag

## Suggested findings to validate
Do not assume that a segment is risky just because its fraud count is high.
Compare **fraud rate** as well as volume, and check sample size before recommending
controls. A high-risk segment can have a low number of transactions.

## Important limitations
- The dataset is synthetic and intentionally constructed to demonstrate analysis skills.
- Fraud labels are provided; this project focuses on descriptive analytics and monitoring,
  not production-grade fraud detection.
- Correlation does not establish causation. Thresholds should be validated against
  business costs (false positives vs. missed fraud).

## Portfolio presentation
Explain the work in this order: business problem → data quality → KPI definitions →
segment findings → monitoring recommendations → limitations.
