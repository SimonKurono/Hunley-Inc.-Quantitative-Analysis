import pandas as pd
import numpy as np

# -------------------------------
# 1. Define the Baseline for the Standard Klamath Line
# -------------------------------
baseline_klamath = {
    'unit_sales': 101000,      # 2018 units for Klamath line
    'avg_unit_price': 260      # 2018 average unit price in dollars
}

# -------------------------------
# 2. Define the Assumptions for the Standard Klamath Line
# -------------------------------
assumptions_klamath = {
    'sales_growth': -0.02,          # Overall revenue declines 2% per year
    'unit_sales_growth': 0.00,     # Unit sales decline 3% per year
    'price_growth': 0.00,          # Average unit price declines 1% per year
    'COGS_percent': 0.47,           # COGS is 47% of Sales
    'sales_comm_rate': 0.05,        # 5% sales commissions
    'G_A_percent': 0.25             # G&A expenses are 25% of Sales
}

# -------------------------------
# 3. Projection Function
# -------------------------------
def project_income_statement(baseline, assumptions, years=3):
    """
    Projects an income statement for a given number of years using the baseline values
    for unit sales and average unit price, applying percentage declines (or growth) based
    on the assumptions.
    
    Returns a DataFrame with projections for each year including:
      - Year
      - unit_sales
      - avg_unit_price
      - Sales (unit_sales * avg_unit_price)
      - COGS (as a percentage of Sales)
      - Gross Profit (Sales - COGS)
      - Sales Commissions (as a percentage of Sales)
      - G&A Expenses (as a percentage of Sales)
      - EBITDA (Gross Profit minus Sales Commissions and G&A)
    """
    projections = []
    last_year = baseline.copy()
    
    for i in range(1, years + 1):
        projection = {}
        projection['Year'] = 2018 + i
        
        # Update unit sales and average unit price
        projection['unit_sales'] = last_year['unit_sales'] * (1 + assumptions['unit_sales_growth'])
        projection['avg_unit_price'] = last_year['avg_unit_price'] * (1 + assumptions['price_growth'])
        
        # Calculate Sales
        projection['Sales'] = projection['unit_sales'] * projection['avg_unit_price']
        
        # Calculate expenses and profits
        projection['COGS'] = projection['Sales'] * assumptions['COGS_percent']
        projection['Gross_Profit'] = projection['Sales'] - projection['COGS']
        projection['Sales_Commissions'] = projection['Sales'] * assumptions['sales_comm_rate']
        projection['G_and_A'] = projection['Sales'] * assumptions['G_A_percent']
        projection['EBITDA'] = projection['Gross_Profit'] - projection['Sales_Commissions'] - projection['G_and_A']
        
        projections.append(projection)
        last_year = projection.copy()   # Use this year's projection as the baseline for the next year
    
    return pd.DataFrame(projections)

# -------------------------------
# 4. Run the Projection for the Standard Klamath Line
# -------------------------------
years_to_project = 3
projection_klamath = project_income_statement(baseline_klamath, assumptions_klamath, years=years_to_project)

# -------------------------------
# 5. Print the Detailed Sales Projection
# -------------------------------
print("Klamath Line 3-Year Sales Projection:")
print(projection_klamath[['Year', 'unit_sales', 'avg_unit_price', 'Sales', 'COGS', 'Gross_Profit', 'EBITDA']])
