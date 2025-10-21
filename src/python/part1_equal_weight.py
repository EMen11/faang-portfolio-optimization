# %% 0) Imports & configuration
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Average number of trading days per year (used for annualization)
TRADING_DAYS = 252

# Risk-free rate assumption (set to 0% for simplicity)
RISK_FREE = 0.0

print("Working directory:", os.getcwd())

# %% 1) Load dataset
# Load historical FAANG stock prices (2020–2023).
# The CSV file must be located in the same working directory.
CSV_PATH = "/.../faang_stocks.csv"


try:
    df = pd.read_csv(CSV_PATH, parse_dates=["Date"])
except FileNotFoundError as e:
    raise FileNotFoundError(
        f"File not found: {CSV_PATH}\n"
        "Check your working directory in Spyder (top-right folder icon)\n"
        "or use an absolute path if needed."
    ) from e

# Set the date as index and sort chronologically
df = df.set_index("Date").sort_index()

# Quick validation: ensure expected tickers are present
expected_cols = {"AAPL", "AMZN", "GOOGL", "META", "NFLX"}
missing = expected_cols - set(df.columns)
assert not missing, f"Missing columns in CSV: {missing}"

print("Available tickers:", df.columns.tolist())
print(df.head())

# %% 2) Compute daily arithmetic returns
# Use simple daily returns (arithmetic), not log returns.
# These will be the building blocks for portfolio construction.
returns = df.pct_change().dropna()

print("\nSample of daily returns:")
print(returns.head())

print("\nBasic statistics (daily mean and std):")
print(returns.describe().T[["mean", "std"]])

# %% 3) Equal-weight portfolio definition
# Benchmark portfolio: each stock has equal weight (20%).
tickers = returns.columns.tolist()
n = len(tickers)
weights = np.ones(n) / n   # e.g. [0.2, 0.2, 0.2, 0.2, 0.2]

print("\nTickers:", tickers)
print("Equal weights:", weights.round(3))

# %% 4) Portfolio performance metrics
# Step 1: Compute portfolio daily returns
port_daily = returns @ weights

# Step 2: Compute mean and volatility of daily returns
mean_daily = port_daily.mean()
std_daily  = port_daily.std()

# Step 3: Annualize the Sharpe ratio (risk-free rate assumed 0%)
sharpe_annualized = (mean_daily / std_daily) * np.sqrt(TRADING_DAYS)

# Step 4 (extra): Compute annualized return (CAGR) and annualized volatility
cagr = (1 + mean_daily) ** TRADING_DAYS - 1
vol_annualized = std_daily * np.sqrt(TRADING_DAYS)

print("\n=== Equal-Weight Benchmark Portfolio ===")
print(f"Mean daily return        : {mean_daily:.6f}")
print(f"Daily volatility         : {std_daily:.6f}")
print(f"Annualized Sharpe (rf=0) : {sharpe_annualized:.2f}")
print(f"CAGR (annual return)     : {cagr:.2%}")
print(f"Annualized volatility    : {vol_annualized:.2%}")

# %% 5) Visualization: growth of $1
# Plot portfolio cumulative growth over time.
growth = (1 + port_daily).cumprod()

plt.figure()
growth.plot()
plt.title("Equal-Weight Portfolio — Growth of $1 (2020–2023)")
plt.xlabel("Date")
plt.ylabel("Growth")
plt.tight_layout()
plt.show()

# %% 6) Export results (optional)
# Save summary statistics to a CSV file for reporting/documentation.
summary = pd.DataFrame({
    "metric": ["mean_daily", "std_daily", "sharpe_ann_rf0", "CAGR", "vol_annualized"],
    "value":  [mean_daily,   std_daily,   sharpe_annualized, cagr,   vol_annualized]
})
summary.to_csv("benchmark_equal_weight_summary.csv", index=False)
print("\nResults saved: benchmark_equal_weight_summary.csv")
