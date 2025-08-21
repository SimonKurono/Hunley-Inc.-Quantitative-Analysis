import pandas as pd
import numpy as np

def project_income_statement(baseline, assumptions, years=3):
    """
    Projects an income statement over a given number of years.
    Returns a DataFrame of yearly metrics.
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
        
        # Compute expenses and EBITDA
        projection['COGS'] = projection['Sales'] * assumptions.get('COGS_percent', last_year['COGS'] / last_year['Sales'])
        projection['Gross_Profit'] = projection['Sales'] - projection['COGS']
        projection['Sales_Commissions'] = projection['Sales'] * assumptions.get('sales_comm_rate', last_year['Sales_Commissions'] / last_year['Sales'])
        projection['G_and_A'] = projection['Sales'] * assumptions.get('G_A_percent', last_year['G_and_A'] / last_year['Sales'])
        projection['EBITDA'] = projection['Gross_Profit'] - projection['Sales_Commissions'] - projection['G_and_A']
        
        projections.append(projection)
        last_year = projection.copy()  # For chaining the projections into the next year
    
    return pd.DataFrame(projections)

def monte_carlo_simulation_by_year(baseline, base_assumptions, iterations=100000, years=3):
    """
    Runs a Monte Carlo simulation for a given number of iterations.
    Instead of returning a cumulative total, this function stores the projected metrics for each year of each iteration.
    
    Returns:
        A DataFrame with one row per simulation iteration per year, with columns for Year and the income statement metrics.
    """
    # List to collect simulation results for every iteration and every year
    simulation_results = []
    
    # Loop over iterations
    for _ in range(iterations):
        # Apply random variation to the assumptions:
        noise = {
            'sales_growth': np.random.normal(loc=base_assumptions['sales_growth'], scale=0.005),
            'unit_sales_growth': np.random.normal(loc=base_assumptions['unit_sales_growth'], scale=0.005),
            'price_growth': np.random.normal(loc=base_assumptions['price_growth'], scale=0.005),
            'COGS_percent': np.random.normal(loc=base_assumptions['COGS_percent'], scale=0.005),
            'sales_comm_rate': np.random.normal(loc=base_assumptions['sales_comm_rate'], scale=0.002),
            'G_A_percent': np.random.normal(loc=base_assumptions['G_A_percent'], scale=0.005)
        }
        # Get the projected income statement for this iteration
        proj = project_income_statement(baseline, noise, years=years)
        # Add an iteration identifier (if needed)
        proj['Iteration'] = _
        simulation_results.append(proj)
        
    # Combine all iterations into one DataFrame
    all_results = pd.concat(simulation_results, ignore_index=True)
    return all_results

baseline_alt1 = {
    'Sales': None,  # Not used directly; we focus on unit_sales and avg_unit_price
    'COGS': None,   # We'll calculate Sales from unit_sales * avg_unit_price
    'Sales_Commissions': None,
    'G_and_A': None,
    'EBITDA': None,
    'unit_sales': 7000,        # Starting volume for Titaluk rods
    'avg_unit_price': 800      # Starting premium retail price
}

# Sample assumptions for one alternative (you would have similar dictionaries for Alt2 and Alt3)
# Alternative 3: Direct Expansion
assumptions_alt1 = {
    'sales_growth': 0.04,          # 4% overall annual sales growth
    'unit_sales_growth': 0.02,     # 2% annual unit sales growth (niche growth)
    'price_growth': 0.03,          # Average price increases 3% per year
    'COGS_percent': 0.46,          # COGS at 46% of Sales (improved cost efficiency)
    'sales_comm_rate': 0.05,       # 5% sales commissions
    'G_A_percent': 0.23            # G&A remains 23% of Sales
}
# Run the simulation with 10,000 iterations (returns a long DataFrame with year-by-year results)
results = monte_carlo_simulation_by_year(baseline_2018, assumptions_gen, iterations=100000, years=3)

# To get the expected (mean) metrics for each specific year, group by Year and calculate the average.
expected_metrics_by_year = results.groupby('Year').mean().reset_index()

print("Expected Metrics for Each Year (based on 10,000 iterations):")
print(expected_metrics_by_year[['Year', 'Sales', 'COGS', 'Gross_Profit', 'Sales_Commissions', 'G_and_A', 'EBITDA','unit_sales','avg_unit_price']])
