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

def probable_impostors(graph, dead_player: int):
    '''
    A graph is a list of adjacency lists for each node in the graph.
    This method returns a list of pairs of probable impostors
    knowing that dead_player is reported dead.
    '''
    # We build the first list of probable impostors from the adjacency
    # list of dead_player

    impostors_combinations = set()

    # We go through the list of players having seen dead_player
    for impostor in graph[dead_player][1]:
        # We can clear out from the impostor 2 the dead player,
        # the impostor 1 and the players imp1 has seen. We use a set
        # for the O(1) lookup time and to remove duplicates.
        clear = {dead_player, impostor, *graph[impostor][1]}
        suspects = [i for i in range(len(graph)) if i not in clear]
        for i, c in enumerate(combinations([impostor] + suspects, 2)):
            if i < len(suspects):
                print(tuple(c))
                impostors_combinations.add(tuple(c))
        
    # remove duplicates tuples ((1, 3) and (3, 1) are the same)
    return set((a,b) if a<=b else (b,a) for a,b in impostors_combinations)

if __name__ == "__main__":
    graph = load_graph('graph.txt')
    print(graph)
    # Print the probable killers for dead_player = 0
    print(probable_impostors(graph, 0))