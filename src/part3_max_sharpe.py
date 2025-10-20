# %% 0) Imports & configuration
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

TRADING_DAYS = 252
RISK_FREE = 0.0  # annualized risk-free rate (set to 0% for simplicity)

print("CWD:", os.getcwd())

# %% 1) Load prices
CSV_PATHS = [
    "faang_stocks.csv",
    "/Users/eliemenassa/Desktop/Projet 3/faang_stocks.csv",
]
df = None
for p in CSV_PATHS:
    if os.path.isfile(p):
        df = pd.read_csv(p, parse_dates=["Date"])
        CSV_PATH = p
        print("Loaded:", p)
        break
if df is None:
    raise FileNotFoundError("faang_stocks.csv not found — set Spyder working dir to your project folder.")

df = df.set_index("Date").sort_index()
tickers = [c for c in ["AAPL","AMZN","GOOGL","META","NFLX"] if c in df.columns]
if len(tickers) < 2:
    raise ValueError("Need at least 2 FAANG tickers.")
prices = df[tickers].ffill().dropna()

# %% 2) Daily returns and annualized stats
returns = prices.pct_change().dropna()
mean_daily = returns.mean()
cov_daily  = returns.cov()

mu = mean_daily * TRADING_DAYS          # annualized expected returns
Sigma = cov_daily * TRADING_DAYS        # annualized covariance matrix
# %% 3) Max-Sharpe optimization (SciPy)
n = len(tickers)

def ann_metrics(weights, mu_vec, cov_mat, rf=0.0):
    w = np.asarray(weights)
    ann_ret = float(mu_vec @ w)
    ann_vol = float(np.sqrt(w.T @ cov_mat.values @ w))
    sharpe  = (ann_ret - rf) / ann_vol if ann_vol > 0 else np.nan
    return ann_ret, ann_vol, sharpe

def neg_sharpe(weights, mu_vec, cov_mat, rf=0.0):
    ann_ret, ann_vol, sharpe = ann_metrics(weights, mu_vec, cov_mat, rf)
    return -sharpe if np.isfinite(sharpe) else 1e6

cons   = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0},)
bounds = tuple((0.0, 1.0) for _ in range(n))
w0     = np.ones(n) / n

res = minimize(
    fun=lambda w: neg_sharpe(w, mu, Sigma, RISK_FREE),
    x0=w0,
    method='SLSQP',
    bounds=bounds,
    constraints=cons,
    options={'ftol': 1e-12, 'disp': False, 'maxiter': 10000}
)
if not res.success:
    raise RuntimeError(f"Optimization failed: {res.message}")

w_maxsharpe = res.x
ret_ms, vol_ms, sharpe_ms = ann_metrics(w_maxsharpe, mu, Sigma, RISK_FREE)

print("\n=== Maximum-Sharpe Portfolio (SciPy) ===")
print("Weights (%):")
for t, w in zip(tickers, w_maxsharpe):
    print(f"  {t:5s} : {100*w:6.2f}%")
print(f"Annualized return     : {ret_ms:.2%}")
print(f"Annualized volatility : {vol_ms:.2%}")
print(f"Sharpe (rf=0)         : {sharpe_ms:.2f}")

# %% 4) Growth of $1 — Max Sharpe portfolio
port_daily_ms = returns @ w_maxsharpe
growth_ms = (1 + port_daily_ms).cumprod()

plt.figure()
growth_ms.plot()
plt.title("Maximum-Sharpe Portfolio — Growth of $1")
plt.xlabel("Date")
plt.ylabel("Growth")
plt.tight_layout()
plt.show()

# %% 5) Export results
pd.Series(w_maxsharpe, index=tickers, name="weight").to_csv("maxsharpe_weights_scipy.csv")
pd.DataFrame(
    {"metric": ["ann_return","ann_volatility","sharpe_rf0"],
     "value":  [ret_ms,       vol_ms,         sharpe_ms]}
).to_csv("maxsharpe_summary_scipy.csv", index=False)
print("\nSaved: maxsharpe_weights_scipy.csv, maxsharpe_summary_scipy.csv")
