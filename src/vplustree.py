import bisect

# -------------------------------------------------
# Node definition (V+-tree enabled)
# -------------------------------------------------
class Node:
    def __init__(self, order, is_leaf=False):
        self.order = order
        self.is_leaf = is_leaf

        # B+ tree fields
        self.keys = []
        self.children = []
        self.values = []      # used only for leaves
        self.next = None      # leaf linkage
        self.parent = None

        # V+-tree fields (internal/root only)
        self.lpc = None
        self.rpc = None
        self.cp  = None

    def __repr__(self):
        if self.is_leaf:
            return f"<Leaf {self.keys}>"
        return f"<Internal {self.keys}>"


# -------------------------------------------------
# V+-Tree (insert + search only)
# -------------------------------------------------
class VPlusTree:
    def __init__(self, order):
        self.order = order
        self.root = Node(order, is_leaf=True)

    # Search: returns leaf node
    def search(self, key):
        node = self.root
        while not node.is_leaf:
            idx = bisect.bisect_left(node.keys, key)
            node = node.children[idx]
        return node

    # Insert key–value
    def insert(self, key, value):
        leaf = self.search(key)
        idx = bisect.bisect_left(leaf.keys, key)

        leaf.keys.insert(idx, key)
        leaf.values.insert(idx, value)

        if len(leaf.keys) > self.order:
            self._split_leaf(leaf)

    # Leaf split
    def _split_leaf(self, leaf):
        mid = len(leaf.keys) // 2

        new_leaf = Node(self.order, is_leaf=True)
        new_leaf.keys = leaf.keys[mid:]
        new_leaf.values = leaf.values[mid:]
        new_leaf.next = leaf.next

        leaf.keys = leaf.keys[:mid]
        leaf.values = leaf.values[:mid]
        leaf.next = new_leaf

        if leaf.parent is None:
            self._create_new_root(leaf, new_leaf, new_leaf.keys[0])
        else:
            self._insert_internal(leaf.parent, new_leaf.keys[0], new_leaf)

    # Insert into internal node
    def _insert_internal(self, parent, key, child):
        idx = bisect.bisect_left(parent.keys, key)
        parent.keys.insert(idx, key)
        parent.children.insert(idx + 1, child)
        child.parent = parent

        self._update_commitments(parent)

        if len(parent.keys) > self.order:
            self._split_internal(parent)

    # Internal node split
    def _split_internal(self, node):
        mid = len(node.keys) // 2
        promote = node.keys[mid]

        right = Node(self.order, is_leaf=False)
        right.keys = node.keys[mid + 1:]
        right.children = node.children[mid + 1:]

        for c in right.children:
            c.parent = right

        node.keys = node.keys[:mid]
        node.children = node.children[:mid + 1]

        if node.parent is None:
            self._create_new_root(node, right, promote)
        else:
            self._insert_internal(node.parent, promote, right)

        self._update_commitments(node)
        self._update_commitments(right)

    # Create new root
    def _create_new_root(self, left, right, key):
        root = Node(self.order, is_leaf=False)
        root.keys = [key]
        root.children = [left, right]

        left.parent = root
        right.parent = root
        self.root = root

        self._update_commitments(root)

    # -------------------------------------------------
    # Commitment placeholders (V+-tree logic)
    # -------------------------------------------------
    def _update_commitments(self, node):
        if node.is_leaf:
            return
        node.lpc = self._commit(node.children[0].keys)
        node.rpc = self._commit(node.children[-1].keys)

    def _commit(self, keys):
        h = 0
        for k in keys:
            h = (h * 31 + k) % (10**9 + 7)
        return h


# -------------------------------------------------
# Demo
# -------------------------------------------------
if __name__ == "__main__":
    t = VPlusTree(order=3)
    for k in [2, 4, 6, 7, 8, 9, 13, 15]:
        t.insert(k, str(k))

    leaf = t.search(7)
    print("Leaf:", leaf)
    print("Root LPC:", t.root.lpc)
    print("Root RPC:", t.root.rpc)

