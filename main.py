from simulation import gen_env, define_rogers_agents, initate_innovation, run_simulation, animate_diffusion

#Initialization Phase
'''
WIP - Monte carlo

This is Work in progress part of Monte Carlo simulation.
For now it looks for the best possible outcome of simulation to plot it
'''
past = []
best_G = None

for i in range(1000):
    if i % 100 == 0:
        print(f"{i} simulations made")

    G_sim, culture = gen_env()
    G_sim = define_rogers_agents(G_sim)
    G_sim, innovator = initate_innovation(G_sim)
    history = run_simulation(G_sim, innovator)

    if len(history) > len(past):
        past = history
        best_G = G_sim

final_adopter_count = len(past[-1])
total_nodes = len(best_G.nodes())
adoption_percentage = (final_adopter_count / total_nodes) * 100

print("-" * 30)
print(f"Longest streak of innovation: {len(past)} steps")
print(f"Final Adoption: {final_adopter_count}/{total_nodes} ({adoption_percentage:.2f}%)")
print("-" * 30)

animate_diffusion(best_G, past)

'''
Functionalities yet to be implemented

- assign_seniority(G): Distributing seniority across the graph that will influence threshold

- changing threshold in comparison to seniority.

- changing adoption ratio to a weighted sum (based on seniority)

- functionality to save history as CSV for PowerBI analysis

- changing the model to either stochastic_block_model or fractal barabasi-ravasz

- adding graphs and more functionalities to plots

- change approach to "frontier one"

- un-hardcode culture and size
'''