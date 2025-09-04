# faang-portfolio-optimization
Application of Modern Portfolio Theory (MPT) to FAANG stocks (2020–2023).  
Analyse de portefeuilles : équipondéré, volatilité minimale et Sharpe maximal.

# FAANG Portfolio Optimization (2020–2023)  
# Optimisation de Portefeuille FAANG (2020–2023)

This project applies **Modern Portfolio Theory (MPT)** to a portfolio of FAANG stocks  
(**AAPL, AMZN, GOOGL, META, NFLX**) using daily price data from 2020–2023.  

Ce projet applique la **Théorie Moderne du Portefeuille (Markowitz)** à un portefeuille FAANG  
(**AAPL, AMZN, GOOGL, META, NFLX**) en utilisant des données quotidiennes de 2020 à 2023.  

The objective is to compare different allocation strategies  from a simple equal-weight benchmark  
to optimized portfolios and evaluate their **risk–return trade-offs**.  

L’objectif est de comparer différentes stratégies d’allocation d’un portefeuille équipondéré simple  
à des portefeuilles optimisés et d’évaluer leurs compromis **rendement/risque**.  

---

## Project Structure / Structure du projet


1. **Benchmark Portfolio (Equal-Weight) / Portefeuille de référence (Équipondéré)**  
   - Naive allocation: each asset weight = 1/N (here N=5 → 20%).  
   - Allocation naïve : poids de chaque actif = 1/N (ici N=5 → 20%).  

   ![Equal-Weight Portfolio](images/equal_weight.png)


2. Minimum Volatility Portfolio / Portefeuille à Volatilité Minimale
- Mean–variance optimization (Markowitz framework).
- Optimisation moyenne–variance (cadre de Markowitz).
- Objective: find the portfolio weights w = (w1, w2, …, wn) that minimize the variance of returns.
- Objectif : trouver les poids du portefeuille w = (w1, w2, …, wn) qui minimisent la variance des rendements.

Mathematical formulation:
Minimize:  σ_p² = wᵀ Σ w
Subject to: ∑ wi = 1  and  wi ≥ 0

Where:
σ_p² = variance of the portfolio
Σ = covariance matrix of asset returns
wi = weight of asset i

This portfolio provides the lowest possible risk (volatility) for a given set of assets.

![Minimum Volatility Portfolio](images/min_vol.png)


3. Maximum Sharpe Portfolio / Portefeuille au Ratio de Sharpe Maximum
- Mean–variance optimization with Sharpe ratio as objective.
- Optimisation moyenne–variance en maximisant le ratio de Sharpe.
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


4. Comparison & Reporting / Comparaison et Reporting
- Compare different portfolios (Equally Weighted, Minimum Volatility, Maximum Sharpe).
- Comparer différents portefeuilles (équipondéré, volatilité minimale, Sharpe maximum).
- Metrics used: growth of $1 invested, annualized expected return, annualized volatility, Sharpe ratio, portfolio weights.
- Mesures utilisées : croissance de $1 investi, rendement espéré annualisé, volatilité annualisée, ratio de Sharpe, pondérations des portefeuilles.

Mathematical indicators:
E[R_p] = expected annualized return
σ_p = annualized volatility
S = Sharpe ratio = E[R_p] / σ_p

This comparison highlights the efficiency of optimized portfolios versus the simple equally weighted benchmark.

![Comparison of Portfolios](images/comparison.png)


---

## ⚙️ Methodology / Méthodologie

- **Returns / Rendements**: arithmetic daily returns (`pct_change()`), annualized ×252.  
- **Volatility / Volatilité**: standard deviation of returns, annualized ×√252.  
- **Sharpe Ratio / Ratio de Sharpe**: (Return − Risk-Free) ÷ Volatility, risk-free = 0%.  
- **Optimization / Optimisation**: `scipy.optimize.minimize` (SLSQP), constraints:  
  - sum(weights) = 1 / somme des poids = 1  
  - weights ≥ 0 / pas de ventes à découvert  

---

##  Results / Résultats

### Annualized Performance Summary / Résumé des Performances Annualisées

| Portfolio      | Return | Volatility | Sharpe (rf=0) |
|----------------|--------|------------|---------------|
| Equal-Weight   | 23.60% | 32.69%     | 0.72          |
| Min-Vol        | 25.01% | 30.31%     | 0.83          |
| Max-Sharpe     | 28.01% | 31.75%     | 0.88          |

---

### Optimal Weights (%) / Poids Optimaux (%)

| Ticker | Equal-Weight | Min-Vol | Max-Sharpe |
|--------|--------------|---------|------------|
| AAPL   | 20.0         | 39.84   | 78.74      |
| AMZN   | 20.0         | 14.91   | 0.00       |
| GOOGL  | 20.0         | 38.29   | 19.97      |
| META   | 20.0         | 0.00    | 0.00       |
| NFLX   | 20.0         | 6.96    | 1.29       |

---

## 🗝️ Key Takeaways / Points Clés

- **Naive diversification (Equal-Weight)** underperformed both optimized portfolios.  
- La **diversification naïve (équipondérée)** a sous-performé par rapport aux portefeuilles optimisés.  

- **Min-Vol Portfolio** delivered lower risk and improved Sharpe, favoring AAPL + GOOGL.  
- Le **Portefeuille Min-Vol** a réduit le risque et amélioré le Sharpe, en privilégiant AAPL + GOOGL.  

- **Max-Sharpe Portfolio** concentrated in AAPL (≈79%) and GOOGL (≈20%), achieving the best Sharpe.  
- Le **Portefeuille Max-Sharpe** s’est concentré sur AAPL (≈79%) et GOOGL (≈20%), atteignant le meilleur Sharpe.  

- Even within a concentrated FAANG universe, **optimization improves efficiency**.  
- Même dans un univers concentré comme les FAANG, **l’optimisation améliore l’efficacité du portefeuille**.  

---

##  How to Run / Comment Exécuter

1. Clone this repository and place `faang_stocks.csv` in the root folder.  
   Clonez ce dépôt et placez `faang_stocks.csv` à la racine.  

2. Run the Python scripts sequentially:  
   Exécutez les scripts Python dans l’ordre :  
   - `part1_equal_weight.py`  
   - `part2_min_vol.py`  
   - `part3_max_sharpe.py`  
   - `part4_comparison.py`  

3. Results (plots + CSV summaries) will be saved in the project directory.  
   Les résultats (graphes + CSV) seront sauvegardés dans le dossier du projet.  

---

## Tech Stack / Technologies Utilisées

- **Python** (pandas, numpy, matplotlib, scipy)  
- **Optimization / Optimisation**: SLSQP (from `scipy.optimize`)  
- **Data / Données**: FAANG daily prices (2020–2023)  



---

 **Author / Auteur**: E.Menassa  
Aspiring Data & Risk Analyst | Passionate about Finance & Quantitative Research  
Analyste Données & Risques en devenir | Passionné par la Finance & la Recherche Quantitative

