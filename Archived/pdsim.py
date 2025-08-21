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
P0_titaluk = 800        # baseline retail price
elasticity_titaluk = 2.25

price_range_titaluk = np.linspace(600, 1000, 100)
demand_titaluk = predicted_demand(Q0_titaluk, P0_titaluk, price_range_titaluk, elasticity_titaluk)

# Cost per rod assumed $400, plus 5% commission on price
profit_per_unit_titaluk = 0.95 * price_range_titaluk - 400
profit_titaluk = profit_per_unit_titaluk * demand_titaluk

# Find optimum for Alternative 1
opt_idx_titaluk = np.argmax(profit_titaluk)
opt_price_titaluk = price_range_titaluk[opt_idx_titaluk]
opt_profit_titaluk = profit_titaluk[opt_idx_titaluk]
opt_quantity_titaluk = demand_titaluk[opt_idx_titaluk]

# ------- ALTERNATIVE 2: Walmart Rods -------
Q0_walmart = 72000        # baseline units
P0_walmart = 65            # baseline wholesale price
elasticity_walmart = 2.0

price_range_walmart = np.linspace(55, 80, 100)
demand_walmart = predicted_demand(Q0_walmart, P0_walmart, price_range_walmart, elasticity_walmart)

# Cost per rod assumed $32.50, no commission
profit_per_unit_walmart = price_range_walmart - 32.5
profit_walmart = profit_per_unit_walmart * demand_walmart

# Find optimum for Alternative 2
opt_idx_walmart = np.argmax(profit_walmart)
opt_price_walmart = price_range_walmart[opt_idx_walmart]
opt_profit_walmart = profit_walmart[opt_idx_walmart]
opt_quantity_walmart = demand_walmart[opt_idx_walmart]

# ------- ALTERNATIVE 3: Direct Expansion (Occasional) -------
Q0_occasional = 101000 * 0.20   # about 20,000 units
P0_occasional = 260
elasticity_occasional = 1.5
COGS_total_2018 = 12342200.00
unit_sales_2018 = 101000
cost_per_unit = COGS_total_2018 / unit_sales_2018  # baseline cost per unit

price_range_occasional = np.linspace(200, 600, 100)
demand_occasional = predicted_demand(Q0_occasional, P0_occasional, price_range_occasional, elasticity_occasional)

# Assume 47% cost/rod, i.e., cost = ~122.2 ($260*0.47) for comparison
# Alternatively, using a given cost per unit: we use 122.2 for profit calculation.
profit_per_unit_occasional = price_range_occasional - 122.2
profit_occasional = profit_per_unit_occasional * demand_occasional

# Find optimum for Alternative 3
opt_idx_occasional = np.argmax(profit_occasional)
opt_price_occasional = price_range_occasional[opt_idx_occasional]
opt_profit_occasional = profit_occasional[opt_idx_occasional]
opt_quantity_occasional = demand_occasional[opt_idx_occasional]

# ------- CREATE SUBPLOTS -------
fig, axs = plt.subplots(1, 3, figsize=(18, 6), sharey=False)

# --- Plot Alt 1 (Titaluk) ---
axs[0].plot(price_range_titaluk, profit_titaluk, color='blue', label="Titaluk Profit")
axs[0].axvline(opt_price_titaluk, color='blue', linestyle='--',
               label=f"Opt.Price=${opt_price_titaluk:.2f}")
axs[0].set_title("Alt 1: Titaluk Premium")
axs[0].set_xlabel("Price ($)")
axs[0].set_ylabel("Total Profit ($)")
axs[0].grid(True)
axs[0].legend()

# --- Plot Alt 2 (Walmart) ---
axs[1].plot(price_range_walmart, profit_walmart, color='orange', label="Walmart Profit")
axs[1].axvline(opt_price_walmart, color='orange', linestyle='--',
               label=f"Opt.Price=${opt_price_walmart:.2f}")
axs[1].set_title("Alt 2: Walmart Rods")
axs[1].set_xlabel("Price ($)")
axs[1].grid(True)
axs[1].legend()

# --- Plot Alt 3 (Occasional) ---
axs[2].plot(price_range_occasional, profit_occasional, color='green', label="Direct Profit")
axs[2].axvline(opt_price_occasional, color='green', linestyle='--',
               label=f"Opt.Price=${opt_price_occasional:.2f}")
axs[2].set_title("Alt 3: Direct Sales")
axs[2].set_xlabel("Price ($)")
axs[2].grid(True)
axs[2].legend()

plt.tight_layout()
plt.show()

# Print optimum values along with optimal quantity
print("Optimal Pricing, Quantity & Profit:")
print(f"Alt 1 (Titaluk): Price=${opt_price_titaluk:.2f}, Quantity={opt_quantity_titaluk:.0f} units, Profit=${opt_profit_titaluk:,.0f}")
print(f"Alt 2 (Walmart): Price=${opt_price_walmart:.2f}, Quantity={opt_quantity_walmart:.0f} units, Profit=${opt_profit_walmart:,.0f}")
print(f"Alt 3 (Occasional): Price=${opt_price_occasional:.2f}, Quantity={opt_quantity_occasional:.0f} units, Profit=${opt_profit_occasional:,.0f}")
