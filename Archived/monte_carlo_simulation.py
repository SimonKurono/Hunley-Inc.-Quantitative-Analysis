import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---- Baseline 2018 values ----
baseline_2018 = {
    'Sales': 26260000.00,          # in dollars
    'COGS': 12342200.00,
    'Sales_Commissions': 1313000.00,
    'G_and_A': 6039800.00,
    'EBITDA': 6565000.00,
    'unit_sales': 101000,
    'avg_unit_price': 260
}

# ---- Base Assumptions for Each Alternative ----
assumptions_gen = {
    'sales_growth': -0.02,         # -2% overall annual sales growth due to maturity of klamath line
    'unit_sales_growth': -0.02,     # -2% annual unit sales growth 
    'price_growth': -0.03,          # Average price decreases 3% per year
    'COGS_percent': 0.46,          # COGS at 46% of Sales, remains the same, as since price decreases -> COGS will increase as well, ofsetting manufacturer costs
    'sales_comm_rate': 0.05,       # 5% sales commissions
    'G_A_percent': 0.23            # G&A remains 23% of Sales
}
# Alternative 1: Titaluk Premium (high-end product)
baseline_alt1 = {
    'Sales': None,  # Not used directly; we focus on unit_sales and avg_unit_price
    'COGS': None,   # We'll calculate Sales from unit_sales * avg_unit_price
    'Sales_Commissions': None,
    'G_and_A': None,
    'EBITDA': None,
    'unit_sales': 7000,        # Starting volume for Titaluk rods
    'avg_unit_price': 800      # Starting premium retail price
}

assumptions_alt1 = {
    'sales_growth': 0.04,          # 4% overall annual sales growth
    'unit_sales_growth': 0.02,     # 2% annual unit sales growth (niche growth)
    'price_growth': 0.03,          # Average price increases 3% per year
    'COGS_percent': 0.46,          # COGS at 46% of Sales (improved cost efficiency)
    'sales_comm_rate': 0.05,       # 5% sales commissions
    'G_A_percent': 0.23            # G&A remains 23% of Sales
}

# Alternative 2: Klamath for Walmart (entry-level)
baseline_alt2 = {
    'Sales': None,
    'COGS': None,
    'Sales_Commissions': None,
    'G_and_A': None,
    'EBITDA': None,
    'unit_sales': 72000,       # Walmart opening order
    'avg_unit_price': 65       # Baseline wholesale price
}

assumptions_alt2 = {
    'sales_growth': 0.08,          # 8% overall annual sales growth (volume-driven)
    'unit_sales_growth': 0.10,     # 10% unit sales growth (high volume)
    'price_growth': -0.05,         # Average price declines 5% per year (discount pricing)
    'COGS_percent': 0.50,          # Higher COGS at 50% of Sales (lower margins)
    'sales_comm_rate': 0.04,       # 4% sales commissions
    'G_A_percent': 0.20            # G&A efficiency at 20% of Sales
}

# Alternative 3: Direct Expansion
assumptions_alt3 = {
    'sales_growth': 0.06,          # Moderate overall sales growth (6%)
    'unit_sales_growth': 0.05,     # 5% unit sales growth (steady improvement)
    'price_growth': 0.00,          # Average price remains stable
    'COGS_percent': 0.44,          # Lower COGS at 44% of Sales (cost savings)
    'sales_comm_rate': 0.035,      # 5% sales commissions only off of retailer sales, which will account for ~70% total sales. so 0.05*0.7 = 0.035
    'G_A_percent': 0.22            # G&A at 22% of Sales, reflecting moderate efficiency gains
}

# ---- Projection Function ----
def project_income_statement(baseline, assumptions, years=3):
    """
    Project an income statement over a given number of years.
    
    Uses baseline 2018 values and grows unit sales and average price based on provided assumptions.
    """
    projections = []
    last_year = baseline.copy()
    
    for i in range(1, years + 1):
        projection = {}
        projection['Year'] = 2018 + i
        # Update unit sales and average price if present:
        if 'unit_sales' in last_year and 'avg_unit_price' in last_year:
            projection['unit_sales'] = last_year['unit_sales'] * (1 + assumptions.get('unit_sales_growth', assumptions['sales_growth']))
            projection['avg_unit_price'] = last_year['avg_unit_price'] * (1 + assumptions.get('price_growth', 0))
            projection['Sales'] = projection['unit_sales'] * projection['avg_unit_price']
        else:
            projection['Sales'] = last_year['Sales'] * (1 + assumptions['sales_growth'])
        
        # Calculate COGS, Gross Profit and other expenses as percentages of Sales
        projection['COGS'] = projection['Sales'] * assumptions.get('COGS_percent', last_year['COGS'] / last_year['Sales'])
        projection['Gross_Profit'] = projection['Sales'] - projection['COGS']
        projection['Sales_Commissions'] = projection['Sales'] * assumptions.get('sales_comm_rate', last_year['Sales_Commissions'] / last_year['Sales'])
        projection['G_and_A'] = projection['Sales'] * assumptions.get('G_A_percent', last_year['G_and_A'] / last_year['Sales'])
        projection['EBITDA'] = projection['Gross_Profit'] - projection['Sales_Commissions'] - projection['G_and_A']
        
        projections.append(projection)
        last_year = projection.copy()  # Chain projections to next year
    return pd.DataFrame(projections)

# ---- Monte Carlo Simulation Function ----
def monte_carlo_simulation(baseline, base_assumptions, iterations=10000):
    """
    Run a Monte Carlo simulation to project cumulative EBITDA over 3 years,
    applying random noise to the assumption parameters.
    """
    cumulative_EBITDA = []
    for j in range(iterations):
        # Introduce random variation (noise) for key assumptions:
        noise = {
            'sales_growth': np.random.normal(loc=base_assumptions['sales_growth'], scale=0.005),
            'unit_sales_growth': np.random.normal(loc=base_assumptions['unit_sales_growth'], scale=0.005),
            'price_growth': np.random.normal(loc=base_assumptions['price_growth'], scale=0.005),
            'COGS_percent': np.random.normal(loc=base_assumptions['COGS_percent'], scale=0.005),
            'sales_comm_rate': np.random.normal(loc=base_assumptions['sales_comm_rate'], scale=0.002),
            'G_A_percent': np.random.normal(loc=base_assumptions['G_A_percent'], scale=0.005)
        }
        # Run the income projection with these randomized assumptions
        proj = project_income_statement(baseline, noise, years=3)
        # Sum the EBITDA over the 3-year period as the metric for net profit
        cum_EBITDA = proj['EBITDA'].sum()
        cumulative_EBITDA.append(cum_EBITDA)
        
    return np.array(cumulative_EBITDA)

# ---- Run Simulations for Each Alternative ----
iterations = 100000
results_alt1 = monte_carlo_simulation(baseline_2018, assumptions_alt1, iterations=iterations)
results_alt2 = monte_carlo_simulation(baseline_2018, assumptions_alt2, iterations=iterations)
results_alt3 = monte_carlo_simulation(baseline_2018, assumptions_alt3, iterations=iterations)

# ---- Plot the Monte Carlo Results ----


plt.figure(figsize=(12, 8))
plt.hist(results_alt1, bins=200, alpha=0.5, label='Alternative 1: Titaluk Premium')
plt.hist(results_alt2, bins=200, alpha=0.5, label='Alternative 2: Walmart Entry-Level')
plt.hist(results_alt3, bins=200, alpha=0.5, label='Alternative 3: Direct Expansion')
plt.xlabel('Average EBITDA over 3 Years ($)')
plt.ylabel('Frequency')
plt.title('Monte Carlo Simulation: 3-Year Avg. EBITDA Distribution')
plt.legend()
plt.grid(True)

# Save the plot as a PDF
plt.savefig('3_year_EBITDA_simulation.pdf')
plt.show()
