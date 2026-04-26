import networkx as nx
import random


def run_diffusion_poc():
    # 1. Create a simple network (20 employees)
    # Using Watts-Strogatz to simulate a realistic social "small world" network
    print("--- Initializing Company Network ---")
    G = nx.watts_strogatz_graph(n=20, k=4, p=0.2)

    # 2. Initialize basic agents
    for node in G.nodes():
        G.nodes[node]['state'] = 0  # 0 = Not adopted, 1 = Adopted
        # Assign a random adoption threshold between 10% and 50%
        G.nodes[node]['threshold'] = random.uniform(0.1, 0.5)

        # 3. Seed the innovation (Patient Zero)

    patient_zero = 0
    G.nodes[patient_zero]['state'] = 1
    G.nodes[patient_zero]['threshold'] = 0.0  # They already adopted it

    total_adopted = 1
    print(f"Tick 0: {total_adopted}/20 employees have adopted the new tech.\n")


    # 4. The Simulation Loop
    max_ticks = 15
    for tick in range(1, max_ticks + 1):
        new_adopters = []

        # Check every employee
        for node in G.nodes():
            if G.nodes[node]['state'] == 0:  # If they haven't adopted yet
                neighbors = list(G.neighbors(node))

                if len(neighbors) > 0:
                    # Calculate what percentage of their friends have adopted
                    adopted_neighbors = sum([1 for n in neighbors if G.nodes[n]['state'] == 1])
                    adoption_ratio = adopted_neighbors / len(neighbors)

                    # If peer pressure exceeds their threshold, they decide to adopt
                    if adoption_ratio >= G.nodes[node]['threshold']:
                        new_adopters.append(node)

        # Apply the changes at the end of the tick (so adoption happens simultaneously)
        for node in new_adopters:
            G.nodes[node]['state'] = 1

        total_adopted += len(new_adopters)
        print(f"Tick {tick}: {len(new_adopters)} new adopters. Total: {total_adopted}/20")

        # Stop early if everyone adopted
        if total_adopted == len(G.nodes()):
            print("\n🎉 100% Adoption reached!")
            break


if __name__ == "__main__":
    run_diffusion_poc()