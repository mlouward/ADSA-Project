from player import Player

class Tournament:
    ''' an AVL tree used to represent a tournament, with each node being
    a player.
    '''
    def __init__(self, player=None):
        self.root = player

    def _get_height(self, root: Player):
        if not root:
            return 0
        else:
            return root.height

    def insert(self, key: Player):
        self.root = self._insert(self.root, key, key.score)

    def _insert(self, root: Player, key: Player, val: int):
        if not root:
            return Player(key.name, val, role=key.role)
        elif key.score < root.score:
            root.left = self._insert(root.left, key, key.score)
        else:
            root.right = self._insert(root.right, key, key.score)

        root.height = 1 + max(self._get_height(root.left),
                              self._get_height(root.right))

        balance = self.get_balance(root)

        # Case 1 - Left Left
        if balance > 1 and key.score <= root.left.score:
            return self.rotate_right(root)

        # Case 2 - Right Right
        if balance < -1 and key.score >= root.right.score:
            return self.rotate_left(root)

        # Case 3 - Left Right
        if balance > 1 and key.score > root.left.score:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)

        # Case 4 - Right Left
        if balance < -1 and key.score < root.right.score:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

    def rotate_right(self, z: Player):
        y = z.left
        tmp = y.right
        y.right = z
        z.left = tmp

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def rotate_left(self, z):
        y = z.right
        tmp = y.left
        y.left = z
        z.right = tmp

        z.height = 1 + max(self._get_height(z.right), self._get_height(z.left))
        y.height = 1 + max(self._get_height(y.right), self._get_height(y.left))

        return y

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, root, key):
        if not root:
            return root

        if key < root.score:
            root.left = self._delete(root.left, key)

        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp

            elif root.right is None:
                temp = root.left
                root = None
                return temp

            temp = self.get_min_val_node(root.right)
            root.score = temp.score
            root.right = self._delete(root.right, temp.score)

        if root is None:
            return root

        root.height = 1 + max(self._get_height(root.left),
                                self._get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.rotate_right(root)

        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.rotate_left(root)

        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)

        if balance < -1 and self.get_balance(root.right) < 0:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

    def get_min_val_node(self, root):
        if root is None or root.left is None:
            return root
        return self.get_min_val_node(root.left)

    def get_balance(self, root):
        if not root:
            return 0
        return self._get_height(root.left) - self._get_height(root.right)

def inorder(root):
    '''Returns a list of Player, sorted by their score (ascending).'''
    rep = []
    def _inorder(root):
        if root:
            _inorder(root.left)
            rep.append(root)
            _inorder(root.right)
    _inorder(root)
    return rep

def inorder_names(root):
    '''Returns a list of the names of the players, sorted by score.'''
    rep = []
    def _inorder_s(root):
        if root:
            _inorder_s(root.left)
            rep.append(f"{root.name} ({root.score})")
            _inorder_s(root.right)
    _inorder_s(root)
    return rep