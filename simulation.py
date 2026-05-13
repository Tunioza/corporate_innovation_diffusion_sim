import networkx as nx
import numpy as np

def gen_env():
    '''
    Function generates enviroment according to user input

    User defines culture according to Quinn-Cameron Theory,
    >Adhocracy, Market, Clan or Hierarchy
    and size
    >Small, Medium or Large
    Size is defined by random number between bounds stated in sizes dictionary
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
            return G, culture
        else:
            continue

G, culture = gen_env()

print(G)
print(culture)
