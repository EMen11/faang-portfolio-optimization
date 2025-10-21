# %% 0) Imports & config
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

TRADING_DAYS = 252
RISK_FREE = 0.0  # assumed 0% for Sharpe

print("CWD:", os.getcwd())

# %% 1) Load prices
# The CSV file must be located in the same working directory.
CSV_PATHS = ["faang_stocks.csv", "/.../faang_stocks.csv"]
df = None
for p in CSV_PATHS:
    if os.path.isfile(p):
        df = pd.read_csv(p, parse_dates=["Date"]); CSV_PATH = p; print("Loaded:", p); break
if df is None:
    raise FileNotFoundError("faang_stocks.csv not found — set Spyder working dir to your project folder.")

df = df.set_index("Date").sort_index()
tickers = [c for c in ["AAPL","AMZN","GOOGL","META","NFLX"] if c in df.columns]
if len(tickers) < 2: raise ValueError("Need at least 2 FAANG tickers.")
prices = df[tickers].ffill().dropna()
returns = prices.pct_change().dropna()
# %% 2) Helpers (annualized metrics)
def ann_metrics(weights, ret_df, rf=0.0):
    w = np.asarray(weights)
    mean_d = ret_df.mean()
    cov_d  = ret_df.cov()
    ann_ret = float(mean_d @ w) * TRADING_DAYS
    ann_vol = float(np.sqrt(w.T @ (cov_d.values*TRADING_DAYS) @ w))
    sharpe  = (ann_ret - rf) / ann_vol if ann_vol>0 else np.nan
    return ann_ret, ann_vol, sharpe

def min_vol_weights(ret_df):
    n = ret_df.shape[1]
    cov_a = ret_df.cov()*TRADING_DAYS
    cons = ({'type': 'eq','fun': lambda w: np.sum(w)-1.0},)
    bnds = tuple((0.0,1.0) for _ in range(n))
    w0   = np.ones(n)/n
    res = minimize(lambda w: float(w.T @ cov_a.values @ w), w0, method='SLSQP',
                   bounds=bnds, constraints=cons, options={'maxiter':10000, 'ftol':1e-12})
    if not res.success: raise RuntimeError(res.message)
    return res.x

def max_sharpe_weights(ret_df, rf=0.0):
    n = ret_df.shape[1]
    mean_d = ret_df.mean(); cov_a = ret_df.cov()*TRADING_DAYS
    mu_a = mean_d*TRADING_DAYS
    def neg_sharpe(w):
        w = np.asarray(w)
        ann_ret = float(mu_a @ w)
        ann_vol = float(np.sqrt(w.T @ cov_a.values @ w))
        return -((ann_ret - rf)/ann_vol) if ann_vol>0 else 1e6
    cons = ({'type': 'eq','fun': lambda w: np.sum(w)-1.0},)
    bnds = tuple((0.0,1.0) for _ in range(n))
    w0   = np.ones(n)/n
    res = minimize(neg_sharpe, w0, method='SLSQP', bounds=bnds, constraints=cons,
                   options={'maxiter':10000, 'ftol':1e-12})
    if not res.success: raise RuntimeError(res.message)
    return res.x
# %% 3) Compute the three portfolios
n = returns.shape[1]
w_eq = np.ones(n)/n
w_mv = min_vol_weights(returns)
w_ms = max_sharpe_weights(returns, RISK_FREE)

def port_cum(ret_df, w): return (1 + (ret_df @ w)).cumprod()

g_eq = port_cum(returns, w_eq)
g_mv = port_cum(returns, w_mv)
g_ms = port_cum(returns, w_ms)
# %% 4) Plot: Growth of $1 (three curves)
plt.figure()
g_eq.plot(label="Equal-Weight")
g_mv.plot(label="Min-Vol")
g_ms.plot(label="Max-Sharpe")
plt.title("Portfolio Growth (Base = $1)")
plt.xlabel("Date"); plt.ylabel("Growth"); plt.legend()
plt.tight_layout(); plt.show()
# %% 5) Summary table (annualized)
summary = pd.DataFrame({
    "Equal-Weight": ann_metrics(w_eq, returns, RISK_FREE),
    "Min-Vol":      ann_metrics(w_mv, returns, RISK_FREE),
    "Max-Sharpe":   ann_metrics(w_ms, returns, RISK_FREE),
}, index=["Ann.Return","Ann.Volatility","Sharpe(rf=0)"]).T

weights_df = pd.DataFrame({"Ticker": tickers,
                           "Equal-Weight": w_eq,
                           "Min-Vol": w_mv,
                           "Max-Sharpe": w_ms})

print("\n=== Annualized Summary ===")
print(summary.applymap(lambda x: f"{x:.2%}" if isinstance(x,(float,np.floating)) else x))

print("\n=== Weights (%) ===")
print(weights_df.assign(**{
    "Equal-Weight": weights_df["Equal-Weight"]*100,
    "Min-Vol":      weights_df["Min-Vol"]*100,
    "Max-Sharpe":   weights_df["Max-Sharpe"]*100
}).round(2).to_string(index=False))
# %% 6) Export artifacts
summary.to_csv("comparison_summary.csv")
weights_df.to_csv("comparison_weights.csv", index=False)
print("\nSaved: comparison_summary.csv, comparison_weights.csv")
