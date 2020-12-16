import numpy as np
from itertools import permutations


INF = float('inf')

def process(node_info: str):
    '''
    Returns a node name, one of its neighbour and the distance 
    between them from a string with format "name neigh dist".
    '''
    a = node_info.split()
    return int(a[0]), int(a[1]), int(a[2])

def load_graph(path: str):
    '''
    Returns a graph made from a text file
    in which each node lists its neighbours.
    '''
    with open(path) as f:
        data_list = list(map(str.strip, f.readlines()))
    edges = [(i, j) for i, j, _ in map(process, data_list)]
    
    N = np.max(edges)
    adjacency_mat = [[INF for _ in range(N)] for _ in range(N)]

    for f, t, d in list(map(process, data_list)):
        adjacency_mat[f - 1][t - 1] = d
        adjacency_mat[t - 1][f - 1] = d
    
    adjacency_list = [[] for _ in range(N)]
    
    for f, t in edges:
        adjacency_list[f - 1].append(t - 1)
        adjacency_list[t - 1].append(f - 1)

    return adjacency_list, N, adjacency_mat

def hamilton_path(g, N):
    all_paths = []

    def _hamilton_path(g, v, visited, path, N):
        if len(path) == N:
            all_paths.append(path[:])

        for w in g[v]:
            if not visited[w]:
                visited[w] = True
                path.append(w)

                _hamilton_path(g, w, visited, path, N)

                visited[w] = False
                path.pop()

    # Compute all hamiltonian paths (from each starting vertex)
    for i in range(N):
        visited = [False for _ in range(N)]
        visited[i] = True
        path = [i]
        _hamilton_path(graph, i, visited, path, N)

    return all_paths

def get_length(path, mat):
    # Checks the total length of a path from the matrix
    res = 0
    for i in range(len(path) - 1):
        res += mat[path[i]][path[i + 1]]

    return res

if __name__ == "__main__":
    graph, N, mat = load_graph(f"graph_all.txt")
    all_hamiltonian_paths = hamilton_path(graph, N)
    # We check each of the path and keep the minimum distance one
    min_dist = INF
    min_path = []
    for path in all_hamiltonian_paths:
        new_dist = get_length(path, mat)
        if new_dist < min_dist and new_dist:
            min_dist = new_dist
            min_path = path
    # Print with i + 1 because our graph starts at 1
    print(min_dist, list(map(lambda i: i+1, min_path)))