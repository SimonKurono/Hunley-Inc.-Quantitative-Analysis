import numpy as np
import matplotlib.pyplot as plt

# ------- Demand Model -------
def predicted_demand(Q0, P0, P, elasticity):
    """
    Q = Q0 * (P0 / P)^elasticity
    """
    return Q0 * (P0 / P)**(elasticity)

# ------- ALTERNATIVE 1: Titaluk Premium -------
Q0_titaluk = 7000         # baseline units
P0_titaluk = 800           # baseline retail price
elasticity_titaluk = 2.25

price_range_titaluk = np.linspace(600, 1000, 100)
demand_titaluk = predicted_demand(Q0_titaluk, P0_titaluk, price_range_titaluk, elasticity_titaluk)

# Revenue for each price point is Price * Demand
revenue_titaluk = price_range_titaluk * demand_titaluk

# Find optimum for Alternative 1 (maximizing revenue)
opt_idx_titaluk = np.argmax(revenue_titaluk)
opt_price_titaluk = price_range_titaluk[opt_idx_titaluk]
opt_revenue_titaluk = revenue_titaluk[opt_idx_titaluk]
opt_quantity_titaluk = demand_titaluk[opt_idx_titaluk]

# ------- ALTERNATIVE 2: Walmart Rods -------
Q0_walmart = 72000         # baseline units
P0_walmart = 65            # baseline wholesale price
elasticity_walmart = 2.0

price_range_walmart = np.linspace(55, 80, 100)
demand_walmart = predicted_demand(Q0_walmart, P0_walmart, price_range_walmart, elasticity_walmart)

revenue_walmart = price_range_walmart * demand_walmart

# Find optimum for Alternative 2
opt_idx_walmart = np.argmax(revenue_walmart)
opt_price_walmart = price_range_walmart[opt_idx_walmart]
opt_revenue_walmart = revenue_walmart[opt_idx_walmart]
opt_quantity_walmart = demand_walmart[opt_idx_walmart]

# ------- ALTERNATIVE 3: Direct Expansion (Occasional) -------
Q0_occasional = 101000 * 0.20   # about 20,000 units (baseline)
P0_occasional = 260
elasticity_occasional = 1.5

price_range_occasional = np.linspace(200, 600, 100)
demand_occasional = predicted_demand(Q0_occasional, P0_occasional, price_range_occasional, elasticity_occasional)

revenue_occasional = price_range_occasional * demand_occasional

# Find optimum for Alternative 3
opt_idx_occasional = np.argmax(revenue_occasional)
opt_price_occasional = price_range_occasional[opt_idx_occasional]
opt_revenue_occasional = revenue_occasional[opt_idx_occasional]
opt_quantity_occasional = demand_occasional[opt_idx_occasional]

# ------- CREATE SUBPLOTS -------
fig, axs = plt.subplots(1, 3, figsize=(18, 6), sharey=False)

# --- Plot Alt 1 (Titaluk) ---
axs[0].plot(price_range_titaluk, revenue_titaluk, color='blue', label="Titaluk Revenue")
axs[0].axvline(opt_price_titaluk, color='blue', linestyle='--',
               label=f"Opt.Price=${opt_price_titaluk:.2f}")
axs[0].set_title("Alt 1: Titaluk Premium")
axs[0].set_xlabel("Price ($)")
axs[0].set_ylabel("Revenue ($)")
axs[0].grid(True)
axs[0].legend()

# --- Plot Alt 2 (Walmart) ---
axs[1].plot(price_range_walmart, revenue_walmart, color='orange', label="Walmart Revenue")
axs[1].axvline(opt_price_walmart, color='orange', linestyle='--',
               label=f"Opt.Price=${opt_price_walmart:.2f}")
axs[1].set_title("Alt 2: Walmart Rods")
axs[1].set_xlabel("Price ($)")
axs[1].grid(True)
axs[1].legend()

# --- Plot Alt 3 (Occasional) ---
axs[2].plot(price_range_occasional, revenue_occasional, color='green', label="Direct Sales Revenue")
axs[2].axvline(opt_price_occasional, color='green', linestyle='--',
               label=f"Opt.Price=${opt_price_occasional:.2f}")
axs[2].set_title("Alt 3: Direct Expansion")
axs[2].set_xlabel("Price ($)")
axs[2].grid(True)
axs[2].legend()

plt.tight_layout()
plt.show()

# Print optimum values along with optimal quantity and
