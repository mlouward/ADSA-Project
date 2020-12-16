import numpy as np
from itertools import permutations


INF = float('inf')

def process(node_info: str):
    '''
    Returns a node name and its neighbours from
    a string with format <name: neigh1, neigh2, ...>
    '''
    a = node_info.split()
    return int(a[0]), int(a[1])

def load_graph(path: str):
    '''
    Returns a graph made from a text file
    in which each node lists its neighbours.
    '''
    with open(path) as f:
        data_list = map(str.strip, f.readlines())
    edges = [(i, j) for i, j in map(process, data_list)]
    
    adjacency_list = [[] for _ in range(np.max(edges))]
    for f, t in edges:
        adjacency_list[f - 1].append(t - 1)
        adjacency_list[t - 1].append(f - 1)

    return adjacency_list

if __name__ == "__main__":
    graph = load_graph(f"graph_all.txt")
    print(graph)