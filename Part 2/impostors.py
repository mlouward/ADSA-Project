from node import Node

def process(node_info):
    '''
    Returns a node name and its neighbours from
    a string with format <name: neigh1, neigh2, ...>
    '''
    a = node_info.split(':')
    name = int(a[0])
    neighbours = [int(i) for i in a[1].split(',')]
    return name, neighbours

def load_graph(path):
    ''' Returns a graph made from a text file
    in which each node lists its neighbours.
    '''
    with open(path) as f:
        data_list = map(str.strip, f.readlines())
    adjacency_list = [Node(i, j) for i, j in map(process, data_list)]

    return adjacency_list

if __name__ == "__main__":
    print(load_graph('graph.txt'))