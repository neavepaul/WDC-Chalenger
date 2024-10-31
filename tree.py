import json
from race_simulator import calculate_points, simulate_race_outcomes

class TreeNode:
    def __init__(self, max_points, lando_points, description=None, winning_path=False):
        self.max_points = max_points
        self.lando_points = lando_points
        self.description = description or {}
        self.winning_path = winning_path
        self.children = []

    def add_child(self, node):
        self.children.append(node)

def build_tree_stream(current_max_points, current_lando_points, remaining_races):
    """Recursively build a tree of race outcomes."""
    if not remaining_races:
        return TreeNode(current_max_points, current_lando_points)  # Leaf node

    next_race = remaining_races[0]
    root = TreeNode(current_max_points, current_lando_points, description={"race": next_race})

    for max_finish, lando_finish in simulate_race_outcomes():
        max_new_points = current_max_points + calculate_points(max_finish)
        lando_new_points = current_lando_points + calculate_points(lando_finish)

        # Create a new child node with updated points and positions
        child_node = TreeNode(
            max_new_points,
            lando_new_points,
            description={
                "race": next_race,
                "max_position": max_finish,
                "lando_position": lando_finish
            }
        )
        root.add_child(child_node)

        # Recursively build the rest of the tree
        child_tree = build_tree_stream(max_new_points, lando_new_points, remaining_races[1:])
        child_node.children = child_tree.children

    return root

def serialize_tree(node):
    """Convert the tree node to a JSON-serializable dictionary."""
    return {
        "max_points": node.max_points,
        "lando_points": node.lando_points,
        "description": node.description,
        "winning_path": node.winning_path,
        "children": [serialize_tree(child) for child in node.children]
    }

def deserialize_tree(data):
    """Convert a dictionary back into a TreeNode object."""
    node = TreeNode(
        max_points=data['max_points'],
        lando_points=data['lando_points'],
        description=data['description'],
        winning_path=data['winning_path']
    )
    for child_data in data['children']:
        node.add_child(deserialize_tree(child_data))
    return node
