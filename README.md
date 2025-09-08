# Hunley, Inc. — Quantitative Case Analysis (UBC)

Python models for a Harvard Business School case used in a UBC class. The code projects income statements, simulates multi-year EBITDA with Monte Carlo, and explores price–demand elasticity to compare three go-to-market strategies:

* **Titaluk Premium**
* **Walmart Entry-Level**
* **Direct Sales**

**Timeline:** March 2025 – April 2025

---

## Tech

* **Python**
* **NumPy**
* **pandas**
* **Matplotlib**

---

## What It Does

* **Baselines**
  Set unit sales and price for each alternative.

* **Financial Projections**
  Roll forward **Sales → COGS → Gross Profit → Commissions/G\&A → EBITDA**.

* **Market Sizing & Drivers**
  Parameterize demand, pricing, cost drivers, and **TAM**; incorporate random noise.

* **Monte Carlo (Risk/Return)**
  Run **100,000** simulations to quantify distributions of **3-year cumulative EBITDA** and **3-year NPV**.

* **Pricing (PED/CVP)**
  Sweep prices, sample elasticity, and plot the distribution of **profit-maximizing prices**.
  Simulate **825** price points per alternative to set baseline demand and optimal prices.

---

## Methods at a Glance

* **Projection Engine:** Deterministic roll-forward of line items to EBITDA for each strategy.
* **Uncertainty Modeling:** Randomize growth and margin assumptions to generate outcome distributions.
* **Price Elasticity (PED):** Sample elasticity to translate price changes into demand changes.
* **Cost–Volume–Profit (CVP):** Evaluate contribution and profit across a grid of prices.
* **Scenario Comparison:** Contrast strategy outcomes via projected statements, simulated EBITDA/NPV, and optimal price distributions.

---

## Outputs

* **Projected financials** (Sales, COGS, G\&A, EBITDA) by strategy and year.
* **Distributions** of 3-year cumulative EBITDA and NPV (from Monte Carlo).
* **Pricing curves & histograms** showing optimal prices under elasticity uncertainty.
* **Matplotlib visualizations** for projections and simulation results.

---

## Setup

Install dependencies in your Python environment:

```bash
pip install numpy pandas matplotlib
```

> The repository uses standard Python, NumPy, pandas, and Matplotlib. Run the provided Python code to execute baseline projections, Monte Carlo simulations, and pricing sweeps for the three strategies.

---

## Notes

* This analysis is for academic coursework and depends on case-specific assumptions.
* Results are sensitive to demand, pricing, margin, and elasticity parameters; interpret distributions accordingly.
* All figures and plots are generated programmatically; no production guarantees are implied.
