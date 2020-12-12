from itertools import combinations


def process(node_info: str):
    '''
    Returns a node name and its neighbours from
    a string with format <name: neigh1, neigh2, ...>
    '''
    a = node_info.split(':')
    name = int(a[0])
    neighbours = [int(i) for i in a[1].split(',')]
    return name, neighbours

def load_graph(path: str):
    '''
    Returns a graph made from a text file
    in which each node lists its neighbours.
    '''
    with open(path) as f:
        data_list = map(str.strip, f.readlines())
    adjacency_list = [(i, j) for i, j in map(process, data_list)]

    return adjacency_list

def dls(graph, root, max_depth):
    res = set()

    def _dls(graph, root, parent, max_depth):
        if max_depth == 0:
            res.update([(parent, root)])
            return

        if max_depth != 1:
            possible = graph[root][1]
        else:
            # At last step, we want those who didn't see the
            # impostors_combinations so we remove them of the suspects
            possible = [i for i in range(len(graph))
                        if i not in [root] + graph[root][1]]
        for child in possible:
            if child != parent:
                _dls(graph, child, root, max_depth - 1)

    _dls(graph, root, root, max_depth)
    return res

def probable_impostors(graph, dead_player: int):
    '''
    A graph is a list of adjacency lists for each node in the graph.
    This method returns a list of pairs of probable impostors
    knowing that dead_player is reported dead.
    '''
    # We go through the list of graph using Depth First Search
    # with limited depth and dead_player as root.
    # We want depth = 2 to find players who DIDN'T SEE one of the players
    # who SAW dead_player.
    impostors_combinations = dls(graph, dead_player, max_depth=2)

    # remove duplicates tuples. ((1, 3) and (3, 1) are the same for example)
    return set((a,b) if a<=b else (b,a) for a,b in impostors_combinations)

if __name__ == "__main__":
    graph = load_graph('graph.txt')
    print(graph)
    # Print the probable killers for dead_player = 0
    print(probable_impostors(graph, 0))