"""Reproducible exploratory analysis for the synthetic transaction dataset."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATA = Path(__file__).with_name("transactions.csv")
OUT = Path(__file__).with_name("outputs")
OUT.mkdir(exist_ok=True)

df = pd.read_csv(DATA, parse_dates=["transaction_date"])
print("Raw shape:", df.shape)
print("Duplicate transaction IDs:", df.duplicated("transaction_id").sum())

# Data quality treatment: retain the first row for each transaction ID.
df = df.drop_duplicates(subset="transaction_id").copy()
print("Clean shape:", df.shape)
print("Missing values:\\n", df.isna().sum())

# KPI summary
summary = pd.DataFrame({
    "metric": ["transactions", "fraud_transactions", "fraud_rate_pct",
               "total_transaction_value_try", "fraud_value_try"],
    "value": [
        len(df), int(df.is_fraud.sum()), round(100*df.is_fraud.mean(), 2),
        round(df.amount.sum(), 2), round(df.loc[df.is_fraud.eq(1), "amount"].sum(), 2)
    ]
})
summary.to_csv(OUT/"kpi_summary.csv", index=False)
print(summary.to_string(index=False))

# Segment analysis
for col in ["payment_method", "merchant_category", "is_international", "device_change"]:
    result = (df.groupby(col, dropna=False)
                .agg(transactions=("transaction_id","count"),
                     fraud_transactions=("is_fraud","sum"),
                     fraud_rate=("is_fraud","mean"),
                     transaction_value=("amount","sum"))
                .reset_index())
    result["fraud_rate_pct"] = (100*result.pop("fraud_rate")).round(2)
    result.to_csv(OUT/f"fraud_by_{col}.csv", index=False)

# Daily trend
daily = (df.groupby("transaction_date")
           .agg(transactions=("transaction_id","count"),
                fraud_transactions=("is_fraud","sum"),
                fraud_value=("amount", lambda x: x[df.loc[x.index,"is_fraud"].eq(1)].sum()))
           .reset_index())
daily["fraud_rate_pct"] = (100*daily.fraud_transactions/daily.transactions).round(2)
daily.to_csv(OUT/"daily_fraud_trend.csv", index=False)

# Simple visualizations
daily["transaction_date"] = pd.to_datetime(daily["transaction_date"])
plt.figure(figsize=(10,5))
plt.plot(daily.transaction_date, daily.fraud_rate_pct)
plt.title("Daily Fraud Rate")
plt.xlabel("Date"); plt.ylabel("Fraud rate (%)")
plt.tight_layout(); plt.savefig(OUT/"daily_fraud_rate.png", dpi=150); plt.close()

by_method = df.groupby("payment_method").is_fraud.mean().mul(100).sort_values(ascending=False)
plt.figure(figsize=(7,5))
by_method.plot(kind="bar")
plt.title("Fraud Rate by Payment Method")
plt.xlabel("Payment method"); plt.ylabel("Fraud rate (%)")
plt.tight_layout(); plt.savefig(OUT/"fraud_by_payment_method.png", dpi=150); plt.close()
