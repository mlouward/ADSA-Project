import numpy as np
from itertools import permutations


INF = float('inf')

def floyd_warshall(graph):
    '''
    The graph is undirected and weighted (symmetric adjacency matrix)
    '''
    v = len(graph)
    # path reconstruction matrix
    p = np.zeros((v, v))
    for i in range(v):
        for j in range(v):
            p[i, j] = graph[i, j]

    for k in range(v):
        for j in range(v):
            for i in range(j):
                p[i, j] = min(p[i, j], p[i, k] + p[k, j])
                p[j, i] = p[i, j]

    return p

def load_graph(path, for_crewmates=True):
    edges = []
    with open(path, 'r') as f:
        for line in f:
            # Stop at empty line for crewmate map
            if not line.strip():
                if for_crewmates:
                    break
                else:
                    continue
            edges.append(list(map(int, line.strip().split())))

    # find max index of vertices in the graph = nb of vertices
    nb_vertices = np.max([[i[0] for i in edges] + [i[1] for i in edges]])

    # Initialize all values to INF
    matrix = [[INF for _ in range(nb_vertices)] for _ in range(nb_vertices)]
    # Set diagonal as 0
    for i in range(nb_vertices):
        matrix[i][i] = 0

    # Set weights in matrix
    for edge in edges:
        matrix[edge[0] - 1][edge[1] - 1] = edge[2]
        matrix[edge[1] - 1][edge[0] - 1] = edge[2]
    return np.array(matrix)

def travelling_salesman(graph, n, s):
    vertex = list(range(1, n))
    # store minimum weight Hamiltonian Cycle
    min_path = INF
    next_permutation = permutations(vertex)
    
    for i in next_permutation:
        current_pathweight = 0

        k = s
        for j in i:
            current_pathweight += graph[k][j]
            k = j
        current_pathweight += graph[k][s]
        if current_pathweight < min_path:
            min_path = current_pathweight
            path = i

    return min_path, path

if __name__ == "__main__":
    graph = load_graph(f"graph_all.txt")
    complete_graph = floyd_warshall(graph)
    print(complete_graph)
    print(travelling_salesman(complete_graph, 20, 10))