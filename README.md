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

## Analysis

### 1. Benchmark Portfolio — Equal Weight  
The baseline strategy allocates each asset an equal weight (1/N = 20%).  
This naive diversification approach serves as the reference point to evaluate optimized portfolios.  

![Equal-Weight Portfolio](reports/figures/equal_weight.png)

---

### 2. Minimum-Variance Portfolio  
Built within the **Markowitz mean–variance framework**, this portfolio minimizes total volatility  
for a given set of assets under realistic constraints (*no short selling, fully invested*).

**Optimization problem:**

\[
\text{Minimize } \sigma_p^2 = w^T \Sigma w
\quad \text{subject to } \sum_i w_i = 1,\; w_i \ge 0
\]

where  
- \( \sigma_p^2 \): portfolio variance  
- \( \Sigma \): covariance matrix of asset returns  
- \( w_i \): portfolio weights  

This portfolio achieves the **lowest attainable risk** given the data.  

![Minimum Volatility Portfolio](reports/figures/min_vol.png)

---

### 3. Maximum-Sharpe Portfolio  
This strategy maximizes the **risk-adjusted return**, defined by the **Sharpe ratio**.  
It finds the allocation that offers the **best trade-off between return and risk**.

**Optimization problem:**

\[
\text{Maximize } S = \frac{w^T \mu}{\sqrt{w^T \Sigma w}}
\quad \text{subject to } \sum_i w_i = 1,\; w_i \ge 0
\]

where  
- \( \mu \): expected return vector  
- \( S \): Sharpe ratio (here, risk-free rate \( R_f = 0\% \))  

![Maximum Sharpe Portfolio](reports/figures/max_sharpe.png)

---

### 4. Portfolio Comparison  
All three portfolios — **Equal-Weight**, **Minimum-Variance**, and **Maximum-Sharpe** —  
are evaluated and compared across the following metrics:
- Annualized return  
- Annualized volatility  
- Sharpe ratio  
- Portfolio weights  
- Growth of $1 invested  

These comparisons highlight how optimization improves **risk–return efficiency**  
relative to naive diversification.

![Portfolio Comparison](reports/figures/comparison.png)



---

## Methodology 

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

##  Key Takeaways

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



