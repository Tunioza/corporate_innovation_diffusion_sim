import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
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
        print("Choose organizational culture model")

        culture = input(f"{", ".join(cultures)}\n").lower()

        size = input(f"Define size of the company. Small, Medium or Large?\n").lower()

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

    :return:
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
        'Early Adopter': (0.1, 0.25),
        'Early Majority': (0.25, 0.45),
        'Late Majority': (0.45, 0.7),
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

    print(f"Agents initialized. Example Agent 0: {G.nodes[0]}")
    return G

def initate_innovation(G):
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
    print(f"Innovator in the simulation: {G.nodes[innovator]}")
    return G

def simulation_step(G):
    '''
    Runs a single time step in the simulation
    :param G:
    :return:
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

    for adopter in new_adopters:
        G.nodes()[adopter]["is_adopter"] = True

    return G