import json
import logging
import pickle  # Import pickle for saving/loading objects
from race_simulator import calculate_points, simulate_race_outcomes
from tqdm import tqdm  # Import tqdm for progress bar

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TreeNode:
    def __init__(self, max_points, lando_points, description=None, winning_path=False):
        self.max_points = max_points
        self.lando_points = lando_points
        self.description = description or {}
        self.winning_path = winning_path
        self.children = []

    def add_child(self, node):
        self.children.append(node)

# Memoization cache
memo_cache = {}

def build_tree_stream(current_max_points, current_lando_points, remaining_races):
    """Recursively build a tree of race outcomes."""
    cache_key = (current_max_points, current_lando_points, tuple(remaining_races))
    
    if cache_key in memo_cache:
        return memo_cache[cache_key]

    if not remaining_races:
        return TreeNode(current_max_points, current_lando_points)  # Leaf node

    next_race = remaining_races[0]
    root = TreeNode(current_max_points, current_lando_points, description={"race": next_race})

    # Track the total number of combinations
    combinations = simulate_race_outcomes()
    total_combinations = len(combinations)
    logging.info(f"Processing {next_race} with {total_combinations} combinations...")

    # Use tqdm to create a progress bar
    with tqdm(total=total_combinations, desc=f"Processing {next_race}") as pbar:
        for max_finish, lando_finish in combinations:
            max_new_points = current_max_points + calculate_points(max_finish)
            lando_new_points = current_lando_points + calculate_points(lando_finish)

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
            pbar.update(1)  # Update the progress bar for each processed combination

            # Recursively build the tree for the remaining races
            child_tree = build_tree_stream(max_new_points, lando_new_points, remaining_races[1:])
            child_node.children = child_tree.children  # Attach children to the current node

    memo_cache[cache_key] = root
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

def count_leaf_nodes(node):
    """Count the number of leaf nodes in the tree."""
    if not node.children:
        return 1
    return sum(count_leaf_nodes(child) for child in node.children)

def save_tree_to_pickle(tree_node, filename="tree_node.pkl"):
    """Save the tree node to a pickle file."""
    with open(filename, 'wb') as file:
        pickle.dump(tree_node, file)
    logging.info(f"Tree node saved to {filename}")

def load_tree_from_pickle(filename="tree_node.pkl"):
    """Load the tree node from a pickle file."""
    with open(filename, 'rb') as file:
        return pickle.load(file)

