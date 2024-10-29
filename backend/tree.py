from race_simulator import calculate_points, simulate_race_outcomes
import json

class TreeNode:
    def __init__(self, max_points, lando_points, description="", winning_path=False):
        self.max_points = max_points
        self.lando_points = lando_points
        self.description = description
        self.winning_path = winning_path
        self.children = []

    def add_child(self, node):
        self.children.append(node)

def build_tree_stream(current_max_points, current_lando_points, remaining_races):
    """Recursively build a tree of race outcomes and stream it in real-time."""
    if not remaining_races:
        node = TreeNode(current_max_points, current_lando_points)
        yield json.dumps(serialize_tree(node))  # Yield the root node
        return

    next_race = remaining_races[0]
    race_type = next_race.get('type', 'main')  # Get the race type (sprint or main)
    root = TreeNode(current_max_points, current_lando_points, description=next_race)

    for max_finish, lando_finish in simulate_race_outcomes(race_type):  
        max_new_points = current_max_points + calculate_points(max_finish, race_type)
        lando_new_points = current_lando_points + calculate_points(lando_finish, race_type)

        possible_fastest_lap = [(True, False), (False, True), (False, False)]
        for max_fastest_lap, lando_fastest_lap in possible_fastest_lap:
            max_adjusted_points = max_new_points + (1 if max_fastest_lap and max_finish != "no_points" else 0)
            lando_adjusted_points = lando_new_points + (1 if lando_fastest_lap and lando_finish != "no_points" else 0)

            # Recursively build the next tree layer
            child_node = TreeNode(max_adjusted_points, lando_adjusted_points, description=next_race)
            root.add_child(child_node)

            # Yield each node as it's created
            yield json.dumps(serialize_tree(root))

            if lando_adjusted_points > max_adjusted_points:
                child_node.winning_path = True

            # Continue building the tree with remaining races
            yield from build_tree_stream(max_adjusted_points, lando_adjusted_points, remaining_races[1:])

def serialize_tree(node):
    return {
        "max_points": node.max_points,
        "lando_points": node.lando_points,
        "description": node.description,
        "winning_path": node.winning_path,
        "children": [serialize_tree(child) for child in node.children]
    }


def print_winning_paths(node, path=[]):
    """Recursively print the paths where Lando finishes ahead."""
    path.append(f"Max: {node.max_points}, Lando: {node.lando_points}, Race: {node.description}")

    if not node.children:  # Leaf node
        if node.winning_path:
            print(" -> ".join(path))
    else:
        for child in node.children:
            print_winning_paths(child, path.copy())
