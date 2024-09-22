from typing import Any, Hashable


def build_tree(source: list[tuple[Hashable | None, Any]]):
    tree: dict[Hashable, dict] = {}

    def add_node(parent, child):
        if parent is None:
            tree[child] = {}
            return

        node = find_node(tree, parent)
        if node is not None:
            node[child] = {}

    def find_node(subtree: dict, target):
        if target in subtree:
            return subtree[target]

        for _, value in subtree.items():
            result = find_node(value, target)
            if result is not None:
                return result
        return None

    while source:
        remaining = []
        for parent, child in source:
            if parent is None or find_node(tree, parent) is not None:
                add_node(parent, child)
            else:
                remaining.append((parent, child))
        if len(remaining) == len(source):
            raise ValueError("Unable to build the tree, there might be a cyclic or disconnected reference.")
        source = remaining

    return tree

source = [
    ('a2', 'a22'),
    (None, 'c'),
    ('a', 'a2'),
    ('b11', 'b111'),
    ('c', 'c1'),
    (None, 'b'),
    ('b', 'b2'),
    ('a', 'a1'),
    ('b1', 'b11'),
    ('a2', 'a21'),
    (None, 'a'),
    ('b', 'b1'),
]

expected = {
    'a': {'a1': {}, 'a2': {'a21': {}, 'a22': {}}},
    'b': {'b1': {'b11': {'b111': {}}}, 'b2': {}},
    'c': {'c1': {}},
}

tree = build_tree(source)
print(tree)

print(tree == expected)
