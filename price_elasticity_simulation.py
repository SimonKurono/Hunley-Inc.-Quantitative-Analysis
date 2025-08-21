import numpy as np
import matplotlib.pyplot as plt

def predicted_demand(Q0, P0, P, elasticity):
    """
    Compute predicted demand using the formula:
        Q = Q0 * (P0 / P)^elasticity
    """
    return Q0 * (P0 / P)**(elasticity)

# Set parameters for an example alternative (e.g., Alternative 3: Occasional Direct)
Q0_occasional = 101000 * 0.17  # baseline ~17,170 units from occasional segment
P0_occasional = 260            # baseline price ($)
# Instead of fixing elasticity, let’s sample it from a normal distribution
elasticity_mean = 1.5
elasticity_std = 0.2

price_range = np.linspace(200, 600, 100)

# Containers for recording optimal prices from each simulation run:
optimal_prices = []
iterations = 10000

for _ in range(iterations):
    # Sample elasticity for this iteration
    elasticity_sample = np.random.normal(elasticity_mean, elasticity_std)
    # Ensure elasticity remains positive:
    elasticity_sample = max(0.1, elasticity_sample)
    
    # Calculate demand and revenue using the sampled elasticity
    demand_sample = predicted_demand(Q0_occasional, P0_occasional, price_range, elasticity_sample)
    revenue_sample = price_range * demand_sample
    
    # Identify the price that maximizes revenue in this run
    idx_opt = np.argmax(revenue_sample)
    optimal_prices.append(price_range[idx_opt])

# Convert the optimal prices list to a numpy array
optimal_prices = np.array(optimal_prices)

# Plot the PDF of optimal prices
plt.figure(figsize=(10, 6))
plt.hist(optimal_prices, bins=50, density=True, alpha=0.6, label='Optimal Price Distribution')
plt.xlabel("Optimal Price ($)")
plt.ylabel("Probability Density")
plt.title("Distribution of Optimal Prices (Occasional Direct Channel) \nwith Elasticity as a Random Variable")
plt.legend()
plt.grid(True)
plt.show()

# Print summary statistics
print(f"Mean Optimal Price: ${optimal_prices.mean():.2f}")
print(f"Std. Dev. of Optimal Price: ${optimal_prices.std():.2f}")
