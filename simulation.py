import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

def gen_env():
    '''
    Function generates enviroment according to user input

    User defines culture according to Quinn-Cameron Theory,
    >Adhocracy, Market, Clan or Hierarchy
    and size
    >Small, Medium or Large
    Size is defined by random number between bounds stated in sizes dictionary

    return Graph, culture
    '''

    G = None
    cultures = ["adhocracy", "market", "clan", "hierarchy"]
    sizes = {
        "small": (10,79),
        "medium": (80,150),
        "large": (151,500)
    }

    while True:
        #print("Choose organizational culture model")

        #culture = input(f"{", ".join(cultures)}\n").lower()
        culture = "market"
        #size = input(f"Define size of the company. Small, Medium or Large?\n").lower()
        size = "large"
        if size in sizes:
            lower_bound, higher_bound = sizes[size]
            NUM_AGENTS = np.random.randint(lower_bound, higher_bound + 1)

        if culture == "exit":
            break

        if culture in ["market", "hierarchy"]:
            G = nx.barabasi_albert_graph(n=NUM_AGENTS, m=2)

        elif culture in ["adhocracy", "clan"]:
            G = nx.watts_strogatz_graph(n=NUM_AGENTS, k=4, p=0.1)

        else:
            print(f"Invalid input: {culture}\nPlease try again or leave by writing exit")

        if G != None:
            for node in G.nodes():
                G.nodes[node]["is_adopter"] = False
            return G, culture
        else:
            continue

def define_rogers_agents(G):
    '''
    Creates attribute adoption_threshold for nodes in accordance to Rogers' theory
    According to theory distribution looks like so

    Innovators (2.5%): Risk-takers who are eager to try new ideas.
    Early Adopters (13.5%): Opinion leaders who adopt early but cautiously.
    Early Majority (34%): Adopts before the average person.
    Late Majority (34%): Skeptical group that adopts after the average participant.
    Laggards (16%): Traditionalists, last to adopt.
    source = https://educationaltechnology.net/diffusion-of-innovations-theory/

    :param G: Graph
    :return Graph with named nodes:
    '''

    rogers_lookup = {
        0.025: 'Innovator',
        0.160: 'Early Adopter',  # 0.025 + 0.135
        0.500: 'Early Majority',  # 0.160 + 0.340
        0.840: 'Late Majority',  # 0.500 + 0.340
        1.000: 'Laggard'  # 0.840 + 0.160
    }

    threshold_map = {
        'Innovator': (0.0, 0.1),
        'Early Adopter': (0.1, 0.2),
        'Early Majority': (0.2, 0.3),
        'Late Majority': (0.3, 0.7),
        'Laggard': (0.7, 1.0)
    }

    for node in G.nodes():
        definer = np.random.random()
        for upper_bound, category in rogers_lookup.items():
            if definer <= upper_bound:
                rogers = category
                break

        G.nodes[node]['Rogers'] = rogers

        lower_bound, upper_bound = threshold_map[rogers]

        G.nodes[node]['Threshold'] = round(np.random.uniform(lower_bound,upper_bound),2)

    #print(f"Agents initialized. Example Agent 0: {G.nodes[0]}")
    #e.g Agents initialized. Example Agent 0: {'is_adopter': False, 'Rogers': 'Laggard', 'Threshold': 0.86}
    return G

def initate_innovation(G):
    '''
    This function looks for innovators and early adopters in Graph.
    Randomly chosen node is set to Is_adopter = True

    :param G: Graph
    :return: Graph and innovators' node_id
    '''
    potential_innovators = []

    for node in G.nodes():
        if G.nodes[node]["Rogers"] == "Innovator":
            potential_innovators.append(node)

    if len(potential_innovators) == 0:
        for node in G.nodes():
            if G.nodes[node]["Rogers"] == "Early Adopter":
                potential_innovators.append(node)

    innovator = random.choice(potential_innovators)
    G.nodes[innovator]["is_adopter"] = True
    #print(f"Innovator in the simulation: {G.nodes[innovator]}")
    #e.g Innovator in the simulation: {'is_adopter': True, 'Rogers': 'Innovator', 'Threshold': 0.07}
    return G, innovator

def simulation_step(G):
    '''
    Runs a single time step in the simulation
    It calculates the adoption_ratio based on neighbors present
    It compares adoption_ratio to adoption threshold

    :return: List of nodes that changes from Non-Adopters to Adopters
    '''

    new_adopters = []

    for node in G.nodes():
        if G.nodes[node]["is_adopter"] == True:
            continue

        neighbors = list(G.neighbors(node))
        if len(neighbors) == 0:
            continue

        adopt_neighbours = sum([1 for n in neighbors if G.nodes[n]['is_adopter'] == True])
        adoption_ratio = adopt_neighbours / len(neighbors)

        if adoption_ratio >= G.nodes[node]["Threshold"]:
            new_adopters.append(node)

    return new_adopters

def run_simulation(G, innovator, max_steps = 100):
    '''
    Runs simulation after initialization

    :param G: Graph
    :param innovator: Node that starts the innovation
    :param max_steps: Upper_bound of moves
    :return: history of nodes that adopted innovation
    '''
    current_adopters = set([innovator])
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

def animate_diffusion(G, history):
    '''
    Animates history to show how spread of innovation works.

    :param G: Graph
    :param history: history of nodes that adopted innovation
    :return: animated plot that shows how innovation spreading works
    '''
    fig, ax = plt.subplots(figsize=(10, 7))
    pos = nx.spring_layout(G, k=0.15, seed=42)

    def update(frame_idx):
        '''

        Supporting function that draws every frame. It clears last frame, and draws the next

        :param frame_idx: Frame tick, starts at 0
        :return: One frame of the plot
        '''
        ax.clear()
        adopters_at_step = history[frame_idx]

        colors = ['gold' if n in adopters_at_step else 'lightgrey' for n in G.nodes()]

        nx.draw_networkx(
            G, pos,
            node_color=colors,
            with_labels=False,
            node_size=100,
            edge_color='whitesmoke',
            ax=ax
        )
        ax.set_title(f"Diffusion Step: {frame_idx} | Total Adopters: {len(adopters_at_step)}")

    ani = FuncAnimation(fig, update, frames=len(history), interval=800, repeat=False)
    plt.show()
