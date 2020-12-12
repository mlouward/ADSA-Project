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
            
    graph_size = np.max([[i[0] for i in edges] + [i[1] for i in edges]])
    print(graph_size)
    
    # in this list, the index + 1 is the node number,
    # and it contains a list of pairs (neighbour, distance)
    adj_list = [0 for i in range(graph_size)]
    for edge in edges:
        # Test if starting edge has already a neighbour
        if not adj_list[edge[0] - 1]:
            adj_list[edge[0] - 1] = [(edge[1], edge[2])]
        else:
            # Add the edge to the already existing list
            adj_list[edge[0] - 1].append((edge[1], edge[2]))
        # Because the graph is undirected, we gotta add the edges in 
        # both lists (edges contains the list of unique links)
        if not adj_list[edge[1] - 1]:
            adj_list[edge[1] - 1] = [(edge[0], edge[2])]
        else:
            adj_list[edge[1] - 1].append((edge[0], edge[2]))

    return np.array(adj_list)


if __name__ == "__main__":
    graph = load_graph('graph_all.txt', True)
    print(graph)