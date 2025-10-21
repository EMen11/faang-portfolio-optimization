
import sys
!"{sys.executable}" -m ensurepip --upgrade
!"{sys.executable}" -m pip install --upgrade pip setuptools wheel
!"{sys.executable}" -m pip install scipy
# %% 0) Imports & config
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.optimize import minimize  # SLSQP solver

TRADING_DAYS = 252

print("CWD:", os.getcwd())
# %% 1) Load prices
# The CSV file must be located in the same working directory.
CSV_PATHS = [
    "faang_stocks.csv",
    "/.../faang_stocks.csv",
]
df = None
for p in CSV_PATHS:
    if os.path.isfile(p):
        df = pd.read_csv(p, parse_dates=["Date"])
        CSV_PATH = p
        print("Loaded:", p)
        break
if df is None:
    raise FileNotFoundError("faang_stocks.csv not found — set the working dir to your project folder.")

df = df.set_index("Date").sort_index()

tickers = [c for c in ["AAPL","AMZN","GOOGL","META","NFLX"] if c in df.columns]
if len(tickers) < 2:
    raise ValueError("Need at least 2 FAANG tickers.")
prices = df[tickers].ffill().dropna()
# %% 2) Returns, annualized mean & covariance (per instructions)
returns = prices.pct_change().dropna()
if returns.empty:
    raise ValueError("Empty returns after pct_change().")

mean_daily = returns.mean()
cov_daily  = returns.cov()

# Annualize (×252)
mu = mean_daily * TRADING_DAYS          # vector of expected returns (not strictly needed for min-vol)
Sigma = cov_daily * TRADING_DAYS        # annualized covariance matrix
# %% 3) Min-Vol optimization (long-only, fully invested)
n = len(tickers)

def portfolio_variance(weights, cov_matrix):
    w = np.asarray(weights)
    return float(w.T @ cov_matrix.values @ w)

# Constraints: sum(w) == 1
cons = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0},)

# Bounds: 0 <= w_i <= 1  (no shorting)
bounds = tuple((0.0, 1.0) for _ in range(n))

# Start at equal weights
w0 = np.ones(n) / n

res = minimize(
    fun=lambda w: portfolio_variance(w, Sigma),
    x0=w0,
    method='SLSQP',
    bounds=bounds,
    constraints=cons,
    options={'ftol': 1e-12, 'disp': False, 'maxiter': 10_000}
)

if not res.success:
    raise RuntimeError(f"Optimization failed: {res.message}")

w_minvol = res.x

# Annualized volatility and return of the min-vol portfolio
vol_minvol = np.sqrt(w_minvol.T @ Sigma.values @ w_minvol)
ret_minvol = float(mu @ w_minvol)

# (rf=0) Sharpe
sharpe_minvol = ret_minvol / vol_minvol if vol_minvol > 0 else np.nan

print("\n=== Minimum-Volatility Portfolio (SciPy) ===")
print("Weights (%):")
for t, w in zip(tickers, w_minvol):
    print(f"  {t:5s} : {100*w:6.2f}%")
print(f"Annualized volatility : {vol_minvol:.2%}")
print(f"Annualized return     : {ret_minvol:.2%}")
print(f"Sharpe (rf=0)         : {sharpe_minvol:.2f}")
# %% 4) Growth of $1 — min-vol portfolio
port_daily_minvol = returns @ w_minvol
growth_minvol = (1 + port_daily_minvol).cumprod()

plt.figure()
growth_minvol.plot()
plt.title("Minimum-Volatility Portfolio — Growth of $1")
plt.xlabel("Date")
plt.ylabel("Growth")
plt.tight_layout()
plt.show()
# %% 5) Export weights & summary
pd.Series(w_minvol, index=tickers, name="weight").to_csv("minvol_weights_scipy.csv")
pd.DataFrame(
    {"metric": ["ann_return","ann_volatility","sharpe_rf0"],
     "value":  [ret_minvol,   vol_minvol,      sharpe_minvol]}
).to_csv("minvol_summary_scipy.csv", index=False)
print("\nSaved: minvol_weights_scipy.csv, minvol_summary_scipy.csv")
