**Hunley, Inc. — Quantitative Case Analysis (UBC)**

Python models for a Harvard Business School case used in a UBC class. The repo projects income statements, simulates multi-year EBITDA with Monte Carlo, and explores price–demand elasticity to compare three strategies (Titaluk Premium, Walmart Entry-Level, Direct Sales).

*Tech*

Python, NumPy, pandas, Matplotlib.

**What it does**

Baselines: set unit sales + price for each alternative.

Projections: roll forward Sales → COGS → Gross Profit → Commissions/G&A → EBITDA.

Monte Carlo: randomize growth/margins to get a distribution of 3-year cumulative EBITDA.

Pricing (PED/CVP): sweep prices, sample elasticity, and plot the distribution of optimal prices.