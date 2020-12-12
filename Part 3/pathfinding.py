import numpy as np


INF = float('inf')

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

    matrix = [[INF for _ in range(len(edges))] for _ in range(len(edges))]
    for edge in edges:
        matrix[edge[0] - 1][edge[1] - 1] = edge[2]
        matrix[edge[1] - 1][edge[0] - 1] = edge[2]

    return np.array(matrix)


if __name__ == "__main__":
    graph = load_graph('graph_all.txt', False)
    print(graph)