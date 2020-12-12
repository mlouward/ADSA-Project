import numpy as np
from itertools import product
from math import inf


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
            tmp = line.strip().split()
            reverse_tmp = [tmp[1], tmp[0], tmp[2]]
            # add edges in both directions
            edges.append(list(map(int, tmp)))
            edges.append(list(map(int, reverse_tmp)))

    graph_size = np.max([[i[0] for i in edges] + [i[1] for i in edges]])
    return graph_size, edges

def floyd_warshall(n, edge):
    rn = range(n)
    dist = [[inf] * n for i in rn]
    nxt  = [[0]   * n for i in rn]
    for i in rn:
        dist[i][i] = 0
    for u, v, w in edge:
        dist[u-1][v-1] = w
        nxt[u-1][v-1] = v-1
    for k, i, j in product(rn, repeat=3):
        sum_ik_kj = dist[i][k] + dist[k][j]
        if dist[i][j] > sum_ik_kj:
            dist[i][j] = sum_ik_kj
            nxt[i][j]  = nxt[i][k]
    print("  pair    dist")
    for i, j in product(rn, repeat=2):
        if i != j:
            print("%2d -> %2d  %4d" 
                  % (i + 1, j + 1, dist[i][j]))

if __name__ == "__main__":
    n, graph = load_graph('graph_all.txt', False)
    print(n, graph)
    floyd_warshall(n, graph)