import pandas as pd
import numpy as np

# -------------------------------
# 1. Define Alternative-Specific Baselines
# (Using optimal price points and corresponding quantities)
# -------------------------------
baseline_opt1 = {
    # Alternative 1: Titaluk Premium
    'unit_sales': 13403,          # Optimal quantity from elasticity sim
    'avg_unit_price': 757.58     # Optimal retail price
}

baseline_opt2 = {
    # Alternative 2: Walmart Rods
    'unit_sales': 71777,         # Optimal quantity from elasticity sim
    'avg_unit_price': 65.10      # Optimal wholesale price
}

baseline_opt3 = {
    # Alternative 3: Direct Expansion for Occasional Customers
    'unit_sales': 12112,         # Optimal quantity from elasticity sim
    'avg_unit_price': 365.66     # Optimal retail price (for the occasional segment)
}

# -------------------------------
# 2. Define Assumptions for Each Alternative (for Sales projections)
# We assume the optimal price is fixed (price_growth = 0) and unit sales grow per year.
# -------------------------------
assumptions_alt1 = {
    'unit_sales_growth': 0.02,     # 2% growth per year for Titaluk Premium
    'price_growth': 0.00           # Price remains fixed
}

assumptions_alt2 = {
    'unit_sales_growth': 0.08,     # Avg 6% growth per year for Walmart Rods
    'price_growth': 0.02           # Price remains fixed
}

assumptions_alt3 = {
    'unit_sales_growth': 0.06,     # Avg. 6% growth per year for Direct Expansion (Occasional)
    'price_growth': 0.03           # Price remains fixed
}

# -------------------------------
# 3. Projection Function for Income Statements (Sales only)
# -------------------------------
def project_income_statement(baseline, assumptions, years=3):
    """
    Projects an income statement over a given number of years.
    Uses the baseline unit_sales and avg_unit_price as the starting points.
    Returns a DataFrame with yearly projections for:
      - Year
      - unit_sales
      - avg_unit_price
      - Sales (unit_sales * avg_unit_price)
    """
    projections = []
    last_year = baseline.copy()
    
    for i in range(1, years + 1):
        projection = {}
        projection['Year'] = 2018 + i
        
        # Update unit_sales and average unit price using the specified growth rates.
        projection['unit_sales'] = last_year['unit_sales'] * (1 + assumptions['unit_sales_growth'])
        projection['avg_unit_price'] = last_year['avg_unit_price'] * (1 + assumptions['price_growth'])
        projection['Sales'] = projection['unit_sales'] * projection['avg_unit_price']
        
        projections.append(projection)
        last_year = projection.copy()  # Use current year's projection as baseline for next year.
    
    return pd.DataFrame(projections)

# -------------------------------
# 4. Monte Carlo Simulation Function (For Sales Projections)
# -------------------------------
def monte_carlo_simulation_sales(baseline, base_assumptions, years=3, iterations=10000):
    """
    Runs a Monte Carlo simulation to project year-by-year Sales over 'years'.
    Applies random noise (using a normal distribution) to unit_sales_growth and price_growth assumptions.
    Returns a DataFrame with the average (mean) unit_sales, avg_unit_price, and Sales for each Year.
    """
    results = []
    for j in range(iterations):
        # Apply random noise to the key parameters
        noise = {
            'unit_sales_growth': np.random.normal(loc=base_assumptions['unit_sales_growth'], scale=0.005),
            'price_growth': np.random.normal(loc=base_assumptions['price_growth'], scale=0.005)
        }
        proj = project_income_statement(baseline, noise, years=years)
        results.append(proj)
    
    # Combine all iterations into one DataFrame
    combined = pd.concat(results)
    # Group by Year and compute the mean for each metric.
    summary = combined.groupby('Year')[['unit_sales', 'avg_unit_price', 'Sales']].mean().reset_index()
    return summary

# -------------------------------
# 5. Run Monte Carlo Simulations for Each Alternative
# -------------------------------
iterations = 10000

summary_alt1 = monte_carlo_simulation_sales(baseline_opt1, assumptions_alt1, years=3, iterations=iterations)
summary_alt2 = monte_carlo_simulation_sales(baseline_opt2, assumptions_alt2, years=3, iterations=iterations)
summary_alt3 = monte_carlo_simulation_sales(baseline_opt3, assumptions_alt3, years=3, iterations=iterations)

# -------------------------------
# 6. Print Year-by-Year Sales Projections for Each Alternative (2019-2021)
# -------------------------------
print("Alternative 1 (Titaluk Premium) Year-by-Year Sales Projections:")
print(summary_alt1)
print("\nAlternative 2 (Walmart Rods) Year-by-Year Sales Projections:")
print(summary_alt2)
print("\nAlternative 3 (Direct Expansion for Occasional Customers) Year-by-Year Sales Projections:")
print(summary_alt3)
