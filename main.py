# main.py
import json
import logging
from pyvis.network import Network
import networkx as nx
import matplotlib.pyplot as plt
from tree import build_tree_stream, serialize_tree, deserialize_tree, count_leaf_nodes, save_tree_to_pickle

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

scores = {
    'max': 367,
    'lando': 323
}

race_schedule = {
    "Brazil": {"colour": "green", "type": "sprint", "main_date": "2024-11-03", "sprint_date": "2024-11-02"},
    "Las Vegas": {"colour": "red", "type": "main", "main_date": "2024-11-18"},
    "Qatar": {"colour": "purple", "type": "sprint", "main_date": "2024-12-01", "sprint_date": "2024-11-30"},
    "Abu Dhabi": {"colour": "blue", "type": "main", "main_date": "2024-12-08"}
}

def visualize_tree_pyvis(tree_node, filename="tree_visualization.html", title="Tree Visualization"):
    """Visualize the tree using pyvis and save it to an HTML file."""
    graph = nx.DiGraph()  # Directed graph

    def add_edges(graph, node, parent_description=None, parent_edge_label=None, race_name=None):
        current_description = f"M: {node.max_points}, L: {node.lando_points}"

        graph.add_node(current_description)

        if parent_description:
            race_info = race_schedule.get(race_name, {})
            edge_colour = race_info.get('colour', 'black')  # Default to black if race info is missing
            graph.add_edge(parent_description, current_description, label=parent_edge_label, color=edge_colour)

        if not node.children:
            graph.nodes[current_description]['color'] = '#FF8000'
        else:
            for child in node.children:
                max_pos_label = child.description['max_position'] if child.description['max_position'] != 'no_points' else ''
                lando_pos_label = child.description['lando_position'] if child.description['lando_position'] != 'no_points' else ''
                edge_label = f"M: {max_pos_label}, L: {lando_pos_label}"
                add_edges(graph, child, current_description, edge_label, race_name=child.description['race'])

    add_edges(graph, tree_node)

    net = Network(notebook=True, height='750px', width='100%', directed=True)
    net.from_nx(graph)

    root_description = f"M: {tree_node.max_points}, L: {tree_node.lando_points}"
    net.get_node(root_description)['color'] = '#E0218a'

    net.show(filename)

def visualize_tree_networkx(tree_node, filename="pruned_race_outcome_tree.png"):
    """Render the tree using NetworkX with matplotlib and save it as an image."""
    graph = nx.DiGraph()

    def add_edges(graph, node, parent_description=None, parent_edge_label=None, race_name=None):
        current_description = f"M: {node.max_points}, L: {node.lando_points}"
        graph.add_node(current_description)

        if parent_description:
            race_info = race_schedule.get(race_name, {})
            edge_colour = race_info.get('colour', 'black')  # Default to black if race info is missing
            graph.add_edge(parent_description, current_description, label=parent_edge_label, color=edge_colour)

        if not node.children:
            graph.nodes[current_description]['color'] = '#FF8000'
        else:
            for child in node.children:
                max_pos_label = child.description['max_position'] if child.description['max_position'] != 'no_points' else ''
                lando_pos_label = child.description['lando_position'] if child.description['lando_position'] != 'no_points' else ''
                edge_label = f"M: {max_pos_label}, L: {lando_pos_label}"
                add_edges(graph, child, current_description, edge_label, race_name=child.description['race'])

    add_edges(graph, tree_node)

    pos = nx.spring_layout(graph, seed=42)
    edge_colors = [graph[u][v]['color'] for u, v in graph.edges]
    node_colors = [graph.nodes[node].get('color', '#A0CBE2') for node in graph]

    plt.figure(figsize=(12, 8))
    nx.draw(graph, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, node_size=500, font_size=8, font_color="black", arrows=True)
    edge_labels = nx.get_edge_attributes(graph, 'label')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=7)

    plt.title("Pruned Race Outcome Tree")
    plt.savefig(filename)
    plt.close()

def prune_tree(node):
    """Recursively prune branches where Lando has fewer points than Max."""
    if not node.children:
        if node.lando_points < node.max_points:
            return None
        else:
            return node

    pruned_children = []
    for child in node.children:
        pruned_child = prune_tree(child)
        if pruned_child:
            pruned_children.append(pruned_child)

    node.children = pruned_children
    return node if pruned_children or node.lando_points > node.max_points else None

def main():
    remaining_races = ["Brazil", "Las Vegas", "Qatar", "Abu Dhabi"]
    initial_max_points = scores['max']
    initial_lando_points = scores['lando']

    logging.info("Starting race outcome tree construction...")
    tree_node = build_tree_stream(initial_max_points, initial_lando_points, remaining_races)
    logging.info("Race outcome tree construction completed.")

    logging.info("Counting leaf nodes before pruning...")
    total_leaf_nodes_before_pruning = count_leaf_nodes(tree_node)
    logging.info(f"Total leaf nodes before pruning: {total_leaf_nodes_before_pruning}")

    logging.info("Pruning the tree to remove branches where Lando loses...")
    pruned_tree = prune_tree(tree_node)

    # Save the tree node to a pickle file
    save_tree_to_pickle(tree_node)

    # Save the pruned tree as an HTML file
    logging.info("Visualizing the pruned race outcome tree...")
    visualize_tree_pyvis(pruned_tree, filename="pruned_race_outcome_tree.html", title="Pruned Race Outcome Tree")

    # Save the pruned tree as an image using NetworkX and matplotlib
    logging.info("Saving the pruned race outcome tree as an image...")
    visualize_tree_networkx(pruned_tree, filename="pruned_race_outcome_tree.png")

    logging.info("Counting leaf nodes after pruning...")
    total_leaf_nodes_after_pruning = count_leaf_nodes(pruned_tree)
    logging.info(f"Total leaf nodes after pruning: {total_leaf_nodes_after_pruning}")

    # Calculate probability of Lando winning the WDC
    probability_of_lando_winning = total_leaf_nodes_after_pruning / total_leaf_nodes_before_pruning if total_leaf_nodes_before_pruning > 0 else 0
    logging.info(f"Probability of Lando winning the WDC: {probability_of_lando_winning*100:.2f}%")

    # Save probability of Lando winning the WDC to a text file  
    with open("lando_prob.txt", "w") as file:
        file.write(f"Probability of Lando winning the WDC: {probability_of_lando_winning:.2f}")

if __name__ == "__main__":
    main()
