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
        '''
        root: root of the tree to insert into (Player)
        key: Player object
        val: score of key
        '''
        if not root:
            return Player(key.name, val, bf=0, role=key.role)
        if val < root.score:
            left_sub_root = self._insert(root.left, key, val)  # insert and update left subroot
            root.left = left_sub_root
            left_sub_root.parent = root  # assign the parent
        else:
            right_sub_root = self._insert(root.right, key, val)  # insert and update right subroot
            root.right = right_sub_root
            right_sub_root.parent = root

        # finally, update heights and bf's of current root after insertion
        # completed (postorder processing)
        root.height = max(self._get_height(root.left), self._get_height(root.right)) + 1
        root.balance = self._get_height(root.left) - self._get_height(root.right)
        return self.rebalance(root)  # RE-BALANCE CURRENT ROOT (if required)

    def rebalance(self, root: Player):
        if root.bf == 2:
            if root.left.bf < 0:  # L-R rotation
                root.left = self.rotate_left(root.left)
                return self.rotate_right(root)
            else:  # L-L rotation
                return self.rotate_right(root)
        elif root.bf == -2:
            if root.right.bf > 0:  # R-L rotation
                root.right = self.rotate_right(root.right)
                return self.rotate_left(root)
            else:  # R-R rotation
                return self.rotate_left(root)
        else:
            return root  # no rebalancing

    def rotate_right(self, root: Player):
        pivot = root.left
        tmp = pivot.right

        pivot.right = root
        pivot.parent = root.parent
        root.parent = pivot

        root.left = tmp
        if tmp:
            tmp.parent = root

        if pivot.parent:
            if pivot.parent.left == root:
                pivot.parent.left = pivot
            else:
                pivot.parent.right = pivot

        root.height = max(self._get_height(root.left), self._get_height(root.right)) + 1
        root.bf = self._get_height(root.left) - self._get_height(root.right)
        pivot.height = max(self._get_height(pivot.left), self._get_height(pivot.right)) + 1
        pivot.bf = self._get_height(pivot.left) - self._get_height(pivot.right)
        return pivot  # return root of new tree

    def rotate_left(self, root: Player):
        pivot = root.right
        tmp = pivot.left

        pivot.left = root
        pivot.parent = root.parent
        root.parent = pivot

        root.right = tmp
        if tmp:
            tmp.parent = root

        if pivot.parent:
            if pivot.parent.left == root:
                pivot.parent.left = pivot
            else:
                pivot.parent.right = pivot

        root.height = max(self._get_height(root.left), self._get_height(root.right)) + 1
        root.bf = self._get_height(root.left) - self._get_height(root.right)
        pivot.height = max(self._get_height(pivot.left), self._get_height(pivot.right)) + 1
        pivot.bf = self._get_height(pivot.left) - self._get_height(pivot.right)
        return pivot  # return root of new tree

    def delete(self, player):
        self.root = self._delete(self.root, player.score, player.name)

    def _delete(self, root, key, name):
        if not root:
            return root

        if key < root.score:
            root.left = self._delete(root.left, key, name)

        elif key > root.score:
            root.right = self._delete(root.right, key, name)

        else:
            if root.name != name:
                if root.left is None:
                    root.right = self._delete(root.right, key, name)

                elif root.right is None:
                    root.left = self._delete(root.left, key, name)

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
                root.right = self._delete(root.right, temp.score, temp.name)

        #If the tree has a single node return node
        if root is None:
            return root

        #update the height of the tree
        root.height = 1 + max(self._get_height(root.left),
                                self._get_height(root.right))
        #find the balance factor
        balance = self._get_height(root.left) - self._get_height(root.right)

        #Left Left
        if balance > 1 and root.left.balance >= 0:
            return self.rotate_right(root)
        #Right Right
        if balance < -1 and root.right.balance <= 0:
            return self.rotate_left(root)
        #Left Right
        if balance > 1 and root.left.balance < 0:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)
        #Right Left
        if balance < -1 and root.right.balance < 0:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)
        return root

    def delete_batch(self, batch):
        for player in batch:
            self.delete(player)

    def get_min_val_node(self, root):
        if root is None or root.left is None:
            return root
        return self.get_min_val_node(root.left)

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