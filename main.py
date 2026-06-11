import numpy as np
import pandas as pd
from simulation import gen_env, define_rogers_agents, initate_innovation, run_simulation, animate_diffusion, assign_seniority, get_matchup_multiplier

# ==========================================
# 1. UI / USER INPUT PHASE (Runs Once)
# ==========================================
print("\n" + "=" * 50)
print("🏢 CORPORATE INNOVATION DIFFUSION SIMULATOR")
print("=" * 50)

cultures = ["adhocracy", "market", "clan", "hierarchy"]
sizes = {"small": (10, 79), "medium": (80, 250), "large": (250, 1500)}

while True:
    print("\nSelect Organizational Culture:")
    print(" - Clan       (Highly connected, dense informal networks)")
    print(" - Adhocracy  (Adaptable, dense, low resistance)")
    print(" - Market     (Siloed, competitive, fewer bridge links)")
    print(" - Hierarchy  (Strict silos, high resistance)")
    culture = input("\nEnter culture (clan/adhocracy/market/hierarchy): ").strip().lower()

    if culture in cultures:
        break
    print("❌ Invalid input. Please try again.")

while True:
    print("\nSelect Company Size:")
    print(" - Small  (10 - 79 employees)")
    print(" - Medium (80 - 250 employees)")
    print(" - Large  (250 - 1500 employees)")
    size_input = input("\nEnter size (small/medium/large) OR an exact integer (e.g., 250): ").strip().lower()

    if size_input in sizes:
        lower, upper = sizes[size_input]
        num_agents = np.random.randint(lower, upper + 1)
        break
    elif size_input.isdigit() and int(size_input) >= 10:
        num_agents = int(size_input)
        break
    print("❌ Invalid input. Please try again.")

while True:
    print("\nSelect Deployment Strategy:")
    print(" - Bottom-Up (Innovation is championed by Juniors and Mids)")
    print(" - Top-Down  (Innovation is mandated by Seniors)")

    strategy_input = input("\nEnter strategy (bottom-up/top-down): ").strip().lower()

    if strategy_input in ["bottom-up", "top-down"]:
        break
    print("❌ Invalid input. Please type 'bottom-up' or 'top-down'.")

print(
    f"\n⚙️ Running Monte Carlo Simulation for {culture.capitalize()} with {num_agents} agents via {strategy_input} deployment...")

# ==========================================
# 2. MONTE CARLO PHASE (Runs 1000 Times)
# ==========================================
past = []
best_G = None

mc_results = {
    'simulation_length': [],
    'final_adoption_pct': [],
    'total_nodes': []
}

iterations = 1000

for i in range(iterations):
    if i % 100 == 0:
        print(f"[{i}/{iterations}] Simulations completed...")

        G_sim = gen_env(culture, num_agents)
        G_sim = define_rogers_agents(G_sim, culture)

        G_sim = assign_seniority(G_sim)

        G_sim, taskforce = initate_innovation(G_sim, taskforce_size=5)
        history = run_simulation(G_sim, taskforce)

    final_adopters = len(history[-1])
    adoption_pct = (final_adopters / num_agents) * 100

    mc_results['simulation_length'].append(len(history))
    mc_results['final_adoption_pct'].append(adoption_pct)
    mc_results['total_nodes'].append(num_agents)

    if len(history) > len(past):
        past = history
        best_G = G_sim

# ==========================================
# 3. RESULTS & VISUALIZATION
# ==========================================
df_results = pd.DataFrame(mc_results)
mean_adoption = df_results['final_adoption_pct'].mean()
mean_length = df_results['simulation_length'].mean()

print("\n" + "=" * 40)
print(f"📊 MONTE CARLO MEAN RESULTS (n={iterations})")
print("=" * 40)
print(f"Mean Final Adoption:     {mean_adoption:.2f}%")
print(f"Mean Time to Saturation: {mean_length:.2f} steps")
print("=" * 40 + "\n")

if best_G is not None:
    animate_diffusion(best_G, past)