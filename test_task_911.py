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

    def find_node(subtree: dict[Any, dict], target):
        if target in subtree:
            return subtree[target]

        for _, value in subtree.items():
            result = find_node(value, target)
            if result is not None:
                return result
        return None

    for parent, child in source:
        add_node(parent, child)

    return tree


source = [
    (None, "a"),
    (None, "b"),
    (None, "c"),
    ("a", "a1"),
    ("a", "a2"),
    ("a2", "a21"),
    ("a2", "a22"),
    ("b", "b1"),
    ("b1", "b11"),
    ("b11", "b111"),
    ("b", "b2"),
    ("c", "c1"),
]

expected = {
    "a": {"a1": {}, "a2": {"a21": {}, "a22": {}}},
    "b": {"b1": {"b11": {"b111": {}}}, "b2": {}},
    "c": {"c1": {}},
}

tree = build_tree(source)
print(tree)

print(tree == expected)
