class Node:
    def __init__(self, name, neighbours=[]):
        ''' initializes a node of a graph with a name and a list of neighbours
        (as an adjacency list). Each node is a player, and the neighbours
        is the list of other players seen by the player.
        '''
        self.name = name
        self.neighbours = neighbours

    def __repr__(self):
        return f"Node {self.name}: {self.neighbours}"