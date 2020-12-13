class Player:
    ''' A node for the AVL tree used by the tournament. It represents
    a player, with its name, score, role, height and right/left subtrees.
    '''
    def __init__(self, name, score=0, role=False):
        self.name = name
        self.score = score
        self.role = role
        self.left = None
        self.right = None
        self.parent = None
        self.height = 1

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        role = "Imp" if self.role else "Crew"
        return f"{self.name}: {self.score} ({role})"