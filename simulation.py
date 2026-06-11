import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
import seaborn as sns


def gen_env(culture, num_agents):
    '''
    Generates environment exclusively using Watts-Strogatz Small World model.
    Takes culture and num_agents as arguments.
    '''
    if culture in ["market", "hierarchy"]:
        k_param = 6
        p_param = 0.1
    elif culture in ["adhocracy", "clan"]:
        k_param = 10
        p_param = 0.25
    else:
        k_param = 6
        p_param = 0.1

    G = nx.watts_strogatz_graph(n=num_agents, k=k_param, p=p_param)

    for node in G.nodes():
        G.nodes[node]["is_adopter"] = False

    return G


def define_rogers_agents(G, culture):
    '''
    Assigns Rogers categories and dynamically shifts adoption thresholds
    based on the organizational culture.
    '''
    rogers_lookup = {
        0.025: 'Innovator',
        0.160: 'Early Adopter',
        0.500: 'Early Majority',
        0.840: 'Late Majority',
        1.000: 'Laggard'
    }

    threshold_map = {
        'Innovator':        (0.0, 0.05),    # Will jump at the slightest spark
        'Early Adopter':    (0.05, 0.15),     # Needs just 1 peer to adopt
        'Early Majority':   (0.15, 0.25),     # Needs a small, visible minority (e.g., 2 out of 8)
        'Late Majority':    (0.25, 0.50),     # Flips once a strong trend is established
        'Laggard':          (0.50, 0.80)      # Stubborn, but will cave when half the team uses it
    }

    culture_shifts = {
        "hierarchy":    0.05,  # High resistance, shifts thresholds UP
        "clan":         0.00,  # Moderate resistance, relies on dense peer consensus
        "market":      -0.05,  # Competitive, slightly lower thresholds
        "adhocracy":   -0.10   # Highly adaptable, shifts thresholds heavily DOWN
    }

    shift = culture_shifts.get(culture, 0.0)

    for node in G.nodes():
        definer = np.random.random()
        for upper_bound, category in rogers_lookup.items():
            if definer <= upper_bound:
                rogers = category
                break

        G.nodes[node]['Rogers'] = rogers

        # Calculate base threshold
        lower_bound, upper_bound = threshold_map[rogers]
        base_threshold = np.random.uniform(lower_bound, upper_bound)

        shifted_threshold = base_threshold + shift
        shifted_threshold = max(0.0, min(1.0, shifted_threshold))

        G.nodes[node]['Threshold'] = round(shifted_threshold, 2)

    return G


def assign_seniority(G):
    '''
    Assigns Junior, Mid, or Senior rank to each agent based on a corporate pyramid.
    '''
    for node in G.nodes():
        rand = np.random.random()
        if rand <= 0.30:
            G.nodes[node]['Seniority'] = 'Junior'
        elif rand <= 0.85:
            G.nodes[node]['Seniority'] = 'Mid'
        else:
            G.nodes[node]['Seniority'] = 'Senior'
    return G


def get_matchup_multiplier(source_rank, target_rank):
    '''
    Calculates influence multiplier based on seniority matchups.
    Source is the adopted neighbor trying to influence the Target (evaluating node).
    '''
    if source_rank == 'Junior':
        if target_rank == 'Senior': return 0.25  # Not very effective...
        if target_rank == 'Mid': return 0.5
    elif source_rank == 'Mid':
        if target_rank == 'Junior': return 2.0  # Super effective!
        if target_rank == 'Senior': return 0.5
    elif source_rank == 'Senior':
        if target_rank == 'Junior': return 4.0  # Extremely effective!
        if target_rank == 'Mid': return 2.0

    return 1.0  # Same rank (e.g., Mid vs Mid) deals normal 1.0x influence


def initate_innovation(G, deployment_strategy="bottom-up", taskforce_size=5):
    '''
    Initiates innovation based on the deployment strategy.
    Bottom-Up: Only recruits Juniors and Mids.
    Top-Down: Only recruits Seniors.
    '''

    if deployment_strategy == "bottom-up":
        valid_nodes = [n for n in G.nodes() if G.nodes[n]['Seniority'] in ['Junior', 'Mid']]
    else:  # top-down
        valid_nodes = [n for n in G.nodes() if G.nodes[n]['Seniority'] == 'Senior']

    potential_starts = [n for n in valid_nodes if G.nodes[n]["Rogers"] in ["Innovator", "Early Adopter"]]

    if not potential_starts:
        potential_starts = valid_nodes

    actual_target_size = min(taskforce_size, len(valid_nodes))

    taskforce = []
    queue = []

    while len(taskforce) < actual_target_size:

        if not queue:
            available_starts = [n for n in potential_starts if n not in taskforce]
            if not available_starts:
                available_starts = [n for n in valid_nodes if n not in taskforce]

            start_node = random.choice(available_starts)
            taskforce.append(start_node)
            queue.append(start_node)

        if len(taskforce) >= actual_target_size:
            break

        current = queue.pop(0)

        for neighbor in G.neighbors(current):
            if neighbor not in taskforce and neighbor in valid_nodes:
                taskforce.append(neighbor)
                queue.append(neighbor)
                if len(taskforce) >= actual_target_size:
                    break

    for node in taskforce:
        G.nodes[node]["is_adopter"] = True

    return G, taskforce


def run_simulation(G, taskforce, max_steps=100):
    '''
    Runs simulation after initialization.

    :param G: Graph
    :param taskforce: List of nodes that start the innovation (the movement)
    :param max_steps: Upper_bound of moves
    :return: history of nodes that adopted innovation
    '''

    current_adopters = set(taskforce)
    history = [set(current_adopters)]

    for _ in range(max_steps):

        to_add = simulation_step(G)

        if not to_add:
            break

        for node in to_add:
            G.nodes[node]["is_adopter"] = True
            current_adopters.add(node)

        history.append(set(current_adopters))

    return history


def simulation_step(G):
    '''
    Runs a single time step in the simulation.
    Calculates adoption ratio dynamically using Seniority Matchup multipliers.
    '''
    new_adopters = []

    for node in G.nodes():
        # Skip if already an adopter
        if G.nodes[node]["is_adopter"]:
            continue

        neighbors = list(G.neighbors(node))
        if len(neighbors) == 0:
            continue

        target_rank = G.nodes[node]['Seniority']

        total_influence_pressure = 0.0
        max_possible_pressure = 0.0

        for peer in neighbors:
            source_rank = G.nodes[peer]['Seniority']

            multiplier = get_matchup_multiplier(source_rank, target_rank)

            max_possible_pressure += multiplier

            if G.nodes[peer]['is_adopter']:
                total_influence_pressure += multiplier

        if max_possible_pressure > 0:
            adoption_ratio = total_influence_pressure / max_possible_pressure
        else:
            adoption_ratio = 0.0

        if adoption_ratio >= G.nodes[node]["Threshold"]:
            new_adopters.append(node)

    return new_adopters


def animate_diffusion(G, history):
    '''
    Animates history to show how spread of innovation works.
    Includes a live-updating line graph tracking adoption percentage.

    :param G: Graph
    :param history: history of nodes that adopted innovation
    :return: animated plot that shows how innovation spreading works
    '''
    fig, (ax_line, ax_net) = plt.subplots(1, 2, figsize=(15, 7), gridspec_kw={'width_ratios': [1, 2.5]})
    pos = nx.spring_layout(G, k=0.15, seed=42)
    sns.set_style("white")
    total_nodes = len(G.nodes())
    max_steps = len(history)

    adoption_pcts = [(len(step_adopters) / total_nodes) * 100 for step_adopters in history]

    def update(frame_idx):
        '''
        Supporting function that draws every frame.
        Clears the last frame, and draws both the line graph and the network.
        '''
        ax_line.clear()
        ax_net.clear()

        # -----------------------------------------
        # 1. Update Network Graph (Right Side)
        # -----------------------------------------
        adopters_at_step = history[frame_idx]
        colors = ['gold' if n in adopters_at_step else 'lightgrey' for n in G.nodes()]

        nx.draw_networkx(
            G, pos,
            ax=ax_net,
            node_color=colors,
            with_labels=False,
            node_size=60,
            edge_color='gainsboro'
        )
        ax_net.set_title(f"Network Diffusion (Step {frame_idx})", fontsize=14)
        ax_net.axis('off')

        # -----------------------------------------
        # 2. Update Adoption Line Graph (Left Side)
        # -----------------------------------------
        current_steps = list(range(frame_idx + 1))
        current_pcts = adoption_pcts[:frame_idx + 1]

        ax_line.plot(current_steps, current_pcts, color='dodgerblue', linewidth=2.5, marker='o', markersize=4)

        ax_line.set_xlim(0, max(1, max_steps - 1))
        ax_line.set_ylim(0, 105)

        ax_line.set_title('Adoption Curve', fontsize=14)
        ax_line.set_xlabel('Simulation Step', fontsize=12)
        ax_line.set_ylabel('Adoption (%)', fontsize=12)
        ax_line.grid(True, linestyle='--', alpha=0.6)

        current_val = current_pcts[-1]
        ax_line.text(0.05, 0.95, f'Current: {current_val:.1f}%',
                     transform=ax_line.transAxes, fontsize=11,
                     verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ani = FuncAnimation(fig, update, frames=len(history), interval=400, repeat=False)

    plt.tight_layout()
    plt.show()