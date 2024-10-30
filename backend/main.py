import networkx as nx
import matplotlib.pyplot as plt
from tree import build_tree_stream, serialize_tree, deserialize_tree
import json


scores = {
    'max': 362,
    'lando': 315
}


def visualize_tree(tree_node):
    """Visualize the tree using networkx and matplotlib."""
    graph = nx.DiGraph()  # Directed graph

    # Traverse the tree and add nodes/edges to the graph
    def add_edges(graph, node, parent_description=None, parent_edge_label=None):
        # If no points, replace with an empty string
        current_description = f"M: {node.max_points}, L: {node.lando_points}"

        graph.add_node(current_description)

        if parent_description:
            graph.add_edge(parent_description, current_description, label=parent_edge_label)

        for child in node.children:
            max_pos_label = child.description['max_position'] if child.description['max_position'] != 'no_points' else ''
            lando_pos_label = child.description['lando_position'] if child.description['lando_position'] != 'no_points' else ''
            edge_label = f"M: {max_pos_label}, L: {lando_pos_label}"
            add_edges(graph, child, current_description, edge_label)

    add_edges(graph, tree_node)

    # Plot the graph
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(graph)
    edge_labels = nx.get_edge_attributes(graph, 'label')
    nx.draw(graph, pos, with_labels=True, node_color="lightblue", font_size=10, node_size=2000, font_weight="bold")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    plt.show()

def main():
    remaining_races = ["Simple Race", "2"]  # Only 2 race in this simplified example
    initial_max_points = scores['max']
    initial_lando_points = scores['lando']

    # Build the race outcome tree
    tree_root = build_tree_stream(initial_max_points, initial_lando_points, remaining_races)

    # Serialize and deserialize the tree for visualization
    tree_json = json.dumps(serialize_tree(tree_root))
    tree_node = deserialize_tree(json.loads(tree_json))

    # Visualize the race outcome tree
    visualize_tree(tree_node)

if __name__ == "__main__":
    main()
