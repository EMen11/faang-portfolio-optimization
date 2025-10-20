# FAANG Portfolio Optimization (2020–2023)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Completed-success)

This project applies **Modern Portfolio Theory (Markowitz)** to a universe of **FAANG stocks**  
(**AAPL, AMZN, GOOGL, META, NFLX**) using daily market data from 2020 to 2023.

It explores how different portfolio optimization strategies perform in terms of **return, risk, and efficiency**:
- **Equal-weight portfolio** (naive benchmark)  
- **Minimum-variance portfolio** (risk minimization objective)  
- **Maximum-Sharpe portfolio** (risk-adjusted return maximization)

Using the **mean–variance optimization framework**, each portfolio is constructed under realistic constraints  
(no short-selling, full investment) and compared across key **performance metrics**:  
annualized return, volatility, Sharpe ratio, and portfolio weights.

The analysis demonstrates how optimization improves the **risk–return efficiency** of a portfolio  
even within a concentrated equity universe like FAANG.  
Visual outputs include the **efficient frontier**, **weights allocation**, and **performance comparison** charts.

---
## Project Structure 

```bash
faang-portfolio-optimization/
├── data/faang_prices.csv
├── src/
│   ├── part1_equal_weight.py
│   ├── part2_min_vol.py
│   ├── part3_max_sharpe.py
│   └── part4_comparison.py
├── reports/figures/
├── requirements.txt
└── README.md
```

---

## Analyse  


1. **Benchmark Portfolio (Equal-Weight)
   - Naive allocation: each asset weight = 1/N (here N=5 → 20%).  
  

   ![Equal-Weight Portfolio](images/equal_weight.png)


2. Minimum Volatility Portfolio 
- Mean–variance optimization (Markowitz framework).

- Objective: find the portfolio weights w = (w1, w2, …, wn) that minimize the variance of returns.


Mathematical formulation:
Minimize:  σ_p² = wᵀ Σ w
Subject to: ∑ wi = 1  and  wi ≥ 0

Where:
σ_p² = variance of the portfolio
Σ = covariance matrix of asset returns
wi = weight of asset i

This portfolio provides the lowest possible risk (volatility) for a given set of assets.

![Minimum Volatility Portfolio](images/min_vol.png)


3. Maximum Sharpe Portfolio 
- Mean–variance optimization with Sharpe ratio as objective.

- Objective: maximize risk-adjusted return, defined as the Sharpe ratio.

Sharpe ratio formula (risk-free rate Rf = 0% here):
S = (E[R_p] – Rf) / σ_p  = E[R_p] / σ_p

Mathematical formulation:
Maximize:  S = (wᵀ μ) / √(wᵀ Σ w)
Subject to: ∑ wi = 1  and  wi ≥ 0

Where:
E[R_p] = expected return of the portfolio
μ = vector of expected returns of assets
σ_p = portfolio volatility

This portfolio gives the best trade-off between return and risk.

![Maximum Sharpe Portfolio](images/max_sharpe.png)


4. Comparison & Reporting 
- Compare different portfolios (Equally Weighted, Minimum Volatility, Maximum Sharpe).

- Metrics used: growth of $1 invested, annualized expected return, annualized volatility, Sharpe ratio, portfolio weights.


Mathematical indicators:
E[R_p] = expected annualized return
σ_p = annualized volatility
S = Sharpe ratio = E[R_p] / σ_p

This comparison highlights the efficiency of optimized portfolios versus the simple equally weighted benchmark.

![Comparison of Portfolios](images/comparison.png)


---

## ⚙️ Methodology 

- **Returns**: arithmetic daily returns (`pct_change()`), annualized ×252.  
- **Volatility**: standard deviation of returns, annualized ×√252.  
- **Sharpe Ratio**: (Return − Risk-Free) ÷ Volatility, risk-free = 0%.  
- **Optimization**: `scipy.optimize.minimize` (SLSQP), constraints:  
  - sum(weights) = 1
  - weights ≥ 0 

---

##  Results

### Annualized Performance Summary 

| Portfolio      | Return | Volatility | Sharpe (rf=0) |
|----------------|--------|------------|---------------|
| Equal-Weight   | 23.60% | 32.69%     | 0.72          |
| Min-Vol        | 25.01% | 30.31%     | 0.83          |
| Max-Sharpe     | 28.01% | 31.75%     | 0.88          |

---

### Optimal Weights (%) 

| Ticker | Equal-Weight | Min-Vol | Max-Sharpe |
|--------|--------------|---------|------------|
| AAPL   | 20.0         | 39.84   | 78.74      |
| AMZN   | 20.0         | 14.91   | 0.00       |
| GOOGL  | 20.0         | 38.29   | 19.97      |
| META   | 20.0         | 0.00    | 0.00       |
| NFLX   | 20.0         | 6.96    | 1.29       |

---

## 🗝️ Key Takeaways

- **Naive diversification (Equal-Weight)** underperformed both optimized portfolios.   

- **Min-Vol Portfolio** delivered lower risk and improved Sharpe, favoring AAPL + GOOGL.    

- **Max-Sharpe Portfolio** concentrated in AAPL (≈79%) and GOOGL (≈20%), achieving the best Sharpe.  

- Even within a concentrated FAANG universe, **optimization improves efficiency**.   

---

##  How to Run

1. Clone this repository and place `faang_stocks.csv` in the root folder.  

2. Run the Python scripts sequentially:  
   - `part1_equal_weight.py`  
   - `part2_min_vol.py`  
   - `part3_max_sharpe.py`  
   - `part4_comparison.py`  

3. Results (plots + CSV summaries) will be saved in the project directory.    

---

## Tech Stack 

- **Python** (pandas, numpy, matplotlib, scipy)  
- **Optimization**: SLSQP (from `scipy.optimize`)  
- **Data**: FAANG daily prices (2020–2023)  



---



