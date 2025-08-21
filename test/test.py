import numpy as np
import matplotlib.pyplot as plt

# --- Demand Model Function ---
def predicted_demand(Q0, P0, P, elasticity):
    """
    Compute predicted demand using: Q = Q0 * (P0 / P)^elasticity
    """
    return Q0 * (P0 / P)**(elasticity)

# --- Function to Adjust Baseline Using Market Analysis Data ---
def adjust_baseline(current_demand, current_share, target_share, capture_rate):
    """
    Adjust the baseline demand given market data.
    
    Parameters:
      current_demand: current units sold for a segment.
      current_share: current % share of that segment in total purchases (decimal).
      target_share: potential/target % share of that segment in the market (decimal).
      capture_rate: assumed fraction of the untapped potential that can be captured (decimal).
      
    Returns:
      Adjusted demand value.
    """
    f = target_share / current_share  # the full factor by which demand could increase.
    adjusted_demand = current_demand * (1 + capture_rate * (f - 1))
    return adjusted_demand

# --- Define Baseline Values for Each Alternative ---
# For Alternatives 1 and 2, use the optimal values from your elasticity sim.
current_share1 = 0.80
target_share1 = 0.435
capture_rate1 = 0.30  # assumed 20% capture of untapped potential

# Original baseline (from elasticity sim) for Alt3:
baseline_occ_original1 = 6956
# Adjusted baseline using market data:
adjusted_units_alt1 = adjust_baseline(baseline_occ_original1, current_share1, target_share1, capture_rate1)
baseline_opt1 = {
    'unit_sales': adjusted_units_alt1,          # Titaluk Premium baseline (optimal quantity)
    'avg_unit_price': 755.56     # Titaluk optimal retail price
}

current_share2 = 0.20
target_share2 = 0.565
capture_rate2 = 0.30  # assumed 20% capture of untapped potential

# Original baseline (from elasticity sim) for Alt3:
baseline_occ_original2 = 71777
# Adjusted baseline using market data:
adjusted_units_alt2 = adjust_baseline(baseline_occ_original2, current_share2, target_share2, capture_rate2)
baseline_opt2 = {
    'unit_sales': adjusted_units_alt2,         # Walmart baseline units
    'avg_unit_price': 65.10      # Walmart optimal wholesale price
}

# For Alternative 3 (Occasional Direct), start with the observed baseline.
# Let's say the previous optimal quantity was 12112 units.
# However, market analysis suggests that occasional buyers have only 18% of current purchases,
# but they represent 52.5% of the potential market.
current_share = 0.18
target_share = 0.525
capture_rate = 0.30  # assumed 60% capture of untapped potential

# Original baseline (from elasticity sim) for Alt3:
baseline_occ_original = 12112
# Adjusted baseline using market data:
adjusted_units_alt3 = adjust_baseline(baseline_occ_original, current_share, target_share, capture_rate)
baseline_opt3 = {
    'unit_sales': adjusted_units_alt3,    # Use adjusted units
    'avg_unit_price': 365.66                # Optimal retail price for occasional
}
print(f"Adjusted Baseline for Alternative 1 (Occasional): {adjusted_units_alt1:.0f} units")
print(f"Adjusted Baseline for Alternative 2 (Occasional): {adjusted_units_alt2:.0f} units")
print(f"Adjusted Baseline for Alternative 3 (Occasional): {adjusted_units_alt3:.0f} units")