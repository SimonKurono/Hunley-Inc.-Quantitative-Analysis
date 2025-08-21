import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Demand Model Function ---
baseline_opt1 = {
    # Alternative 1: Titaluk Premium
    'unit_sales': 13403,          # Optimal quantity from elasticity sim
    'avg_unit_price': 400     # Optimal retail price
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



# For the simulation, Sales, COGS, etc. will be computed from unit_sales and avg_unit_price.
# We assume that in each alternative the price is fixed at the optimal price (price_growth = 0).

# -------------------------------
# 2. Define Assumptions for Each Alternative
# (Other than price, we allow unit sales to grow and vary other ratios with noise)
# -------------------------------
assumptions_alt1 = {
    'sales_growth': 0.04,          # Overall annual revenue growth from market expansion
    'unit_sales_growth': 0.02,     # 2% growth per year for niche expansion
    'price_growth': 0.00,          # Price remains fixed at the optimum
    'COGS_percent': 0.46,          # 46% of Sales as COGS
    'sales_comm_rate': 0.05,       # 5% commission on sales
    'G_A_percent': 0.23            # 23% of Sales on G&A expenses
}

assumptions_alt2 = {
    'sales_growth': 0.21,          # 5% overall revenue growth
    'unit_sales_growth': 0.15,     # 10% growth for volume-driven expansion in Walmart channel
    'price_growth': 0.02,          # Fixed optimal wholesale price
    'COGS_percent': 32.5/65.1,      # 32.5/62.51 of Sales as COGS (typical for low-margin items)
    'sales_comm_rate': 0.03,       # 4% commission (if applicable)
    'G_A_percent': 0.20            # 20% of Sales on G&A expenses
}

assumptions_alt3 = {
    'sales_growth': 0.13,          # % overall revenue growth
    'unit_sales_growth': 0.10,     # 3% annual growth for the direct channel
    'price_growth': 0.03,          # 3% price increase
    'COGS_percent': 0.45,          # Same COGS as 2018 with randomized noise
    'sales_comm_rate': 0.00,       # NO sales commission
    'G_A_percent': 0.22            # 22% of Sales for G&A expenses
}

# -------------------------------
# 3. Update the Projection Function
# (This function uses baseline unit_sales and avg_unit_price, then projects Sales and EBITDA over 3 years)
# -------------------------------
def project_income_statement(baseline, assumptions, years=3):
    """
    Projects an income statement over a given number of years.
    Uses the baseline unit_sales and avg_unit_price as starting points.
    Returns a DataFrame of yearly projections.
    """
    projections = []
    last_year = baseline.copy()
    
    for i in range(1, years + 1):
        projection = {}
        projection['Year'] = 2018 + i
        
        # Evolve unit_sales; avg_unit_price remains constant since price_growth = 0.
        projection['unit_sales'] = last_year['unit_sales'] * (1 + assumptions.get('unit_sales_growth', 0))
        projection['avg_unit_price'] = last_year['avg_unit_price'] * (1 + assumptions.get('price_growth', 0))
        projection['Sales'] = projection['unit_sales'] * projection['avg_unit_price']
        
        # Compute expenses based on given percentages.
        projection['COGS'] = projection['Sales'] * assumptions.get('COGS_percent', 0)
        projection['Gross_Profit'] = projection['Sales'] - projection['COGS']
        projection['Sales_Commissions'] = projection['Sales'] * assumptions.get('sales_comm_rate', 0)
        projection['G_and_A'] = projection['Sales'] * assumptions.get('G_A_percent', 0)
        projection['EBITDA'] = projection['Gross_Profit'] - projection['Sales_Commissions'] - projection['G_and_A']
        
        projections.append(projection)
        last_year = projection.copy()  # Set the current projection as the new baseline.
    
    return pd.DataFrame(projections)

# -------------------------------
# 4. Monte Carlo Simulation Function (Using the above projection function)
# -------------------------------
def monte_carlo_simulation(baseline, base_assumptions, years=3, iterations=100000):
    """
    Runs a Monte Carlo simulation to project cumulative EBITDA over 'years'.
    Applies random noise (using normal distribution) to the assumption parameters.
    Returns an array of cumulative EBITDA values over the projection period.
    """
    cumulative_EBITDA = []
    for j in range(iterations):
        # Random noise on key assumption parameters.
        noise = {
            'sales_growth': np.random.normal(loc=base_assumptions['sales_growth'], scale=0.01),
            'unit_sales_growth': np.random.normal(loc=base_assumptions['unit_sales_growth'], scale=0.01),
            'price_growth': np.random.normal(loc=base_assumptions['price_growth'], scale=0.01),
            'COGS_percent': np.random.normal(loc=base_assumptions['COGS_percent'], scale=0.01),
            'sales_comm_rate': np.random.normal(loc=base_assumptions['sales_comm_rate'], scale=0.005),
            'G_A_percent': np.random.normal(loc=base_assumptions['G_A_percent'], scale=0.01)
        }
        proj = project_income_statement(baseline, noise, years=years)
        cum_EBITDA = proj['EBITDA'].sum()
        cumulative_EBITDA.append(cum_EBITDA)
    return np.array(cumulative_EBITDA)

def monte_carlo_simulation3(baseline, base_assumptions, years=3, iterations=100000):
    """
    Runs a Monte Carlo simulation to project cumulative EBITDA over 'years'.
    Applies random noise (using normal distribution) to the assumption parameters.
    Returns an array of cumulative EBITDA values over the projection period.
    """
    cumulative_EBITDA = []
    for j in range(iterations):
        # Random noise on key assumption parameters.
        noise = {
            'sales_growth': np.random.normal(loc=base_assumptions['sales_growth'], scale=0.01),
            'unit_sales_growth': np.random.normal(loc=base_assumptions['unit_sales_growth'], scale=0.01),
            'price_growth': np.random.normal(loc=base_assumptions['price_growth'], scale=0.01),
            'COGS_percent': np.random.normal(loc=base_assumptions['COGS_percent'], scale=0.01),
            'sales_comm_rate': np.random.normal(loc=base_assumptions['sales_comm_rate'], scale=0.005),
            'G_A_percent': np.random.normal(loc=base_assumptions['G_A_percent'], scale=0.01)
        }
        proj = project_income_statement(baseline, noise, years=years)
        cum_EBITDA = proj['EBITDA'].sum()-500000
        cumulative_EBITDA.append(cum_EBITDA)
    return np.array(cumulative_EBITDA)

# -------------------------------
# 5. Run Monte Carlo Simulations for Each Alternative Using Their Optimal Baselines
# -------------------------------
iterations = 100000

results_alt1 = monte_carlo_simulation(baseline_opt1, assumptions_alt1, years=4, iterations=iterations)
results_alt2 = monte_carlo_simulation(baseline_opt2, assumptions_alt2, years=4, iterations=iterations)
results_alt3 = monte_carlo_simulation(baseline_opt3, assumptions_alt3, years=4, iterations=iterations)

# -------------------------------
# 6. Plot the EBITDA Distributions & Save the Graph as a PDF
# -------------------------------

plt.figure(figsize=(12, 8))
plt.xlim(4000000, 9900000)  # Set the x-axis range from 200 to 800
plt.hist(results_alt1, bins=400, alpha=0.5, label='Alt 1: Titaluk Premium')
plt.hist(results_alt2, bins=400, alpha=0.5, label='Alt 2: Walmart Entry-Level')
plt.hist(results_alt3, bins=400, alpha=0.5, label='Alt 3: Direct Expansion')
plt.xlabel('Cumulative EBITDA over 3 Years ($)')
plt.ylabel('Frequency')
plt.title('Monte Carlo Simulation: 3-Year Cumulative EBITDA Distribution of Hunley Inc\'s Alternatives (From 2018E Baseline)')
plt.legend()
plt.grid(True)

# Save the plot as a PDF file
plt.savefig('projected_EBITDA_distribution.pdf')
plt.show()

# -------------------------------
# 7. Print Summary Statistics for Each Alternative
# -------------------------------
print("Cumulative 3-Year EBITDA (Monte Carlo Simulation):")
print(f"Alternative 1 (Titaluk Premium): Mean = ${results_alt1.mean():,.0f}, Std = ${results_alt1.std():,.0f}")
print(f"Alternative 2 (Walmart): Mean = ${results_alt2.mean():,.0f}, Std = ${results_alt2.std():,.0f}")
print(f"Alternative 3 (Direct Expansion): Mean = ${results_alt3.mean():,.0f}, Std = ${results_alt3.std():,.0f}")
