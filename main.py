from pyvis.network import Network
import networkx as nx
import json
from tree import build_tree_stream, serialize_tree, deserialize_tree

scores = {
    'max': 362,
    'lando': 315
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

    # Traverse the tree and add nodes/edges to the graph
    def add_edges(graph, node, parent_description=None, parent_edge_label=None, race_name=None):
        current_description = f"M: {node.max_points}, L: {node.lando_points}"

        # Add the current node
        graph.add_node(current_description)

        if parent_description:
            # Get the colour for the current race from the race_schedule dictionary
            race_info = race_schedule.get(race_name, {})
            edge_colour = race_info.get('colour', 'black')  # Default to black if race info is missing
            graph.add_edge(parent_description, current_description, label=parent_edge_label, color=edge_colour)

        # Recursively process the children
        if not node.children:
            # Color leaf nodes "papaya"
            graph.nodes[current_description]['color'] = '#FF8000'
        else:
            for child in node.children:
                max_pos_label = child.description['max_position'] if child.description['max_position'] != 'no_points' else ''
                lando_pos_label = child.description['lando_position'] if child.description['lando_position'] != 'no_points' else ''
                edge_label = f"M: {max_pos_label}, L: {lando_pos_label}"
                add_edges(graph, child, current_description, edge_label, race_name=child.description['race'])

    # Build the NetworkX graph
    add_edges(graph, tree_node)

    # Create a pyvis network object
    net = Network(notebook=True, height='750px', width='100%', directed=True)

    # Populate pyvis with nodes and edges from the networkx graph
    net.from_nx(graph)

    # Colour the root node lilac
    root_description = f"M: {tree_node.max_points}, L: {tree_node.lando_points}"
    net.get_node(root_description)['color'] = '#E0218a'

    # Save the interactive graph as an HTML file
    net.show(filename)


def prune_tree(node):
    """Recursively prune branches where Lando has fewer points than Max."""
    if not node.children:
        # If it's a leaf and Lando has fewer points than Max, return None to prune this branch
        if node.lando_points < node.max_points:
            return None
        else:
            return node

    # Recursively prune children
    pruned_children = []
    for child in node.children:
        pruned_child = prune_tree(child)
        if pruned_child:  # Only keep non-pruned children
            pruned_children.append(pruned_child)

    node.children = pruned_children
    return node if pruned_children or node.lando_points >= node.max_points else None

def main():
    remaining_races = ["Brazil", "Las Vegas", "Qatar", "Abu Dhabi"]
    initial_max_points = scores['max']
    initial_lando_points = scores['lando']

    # Build the race outcome tree
    tree_root = build_tree_stream(initial_max_points, initial_lando_points, remaining_races)

    # Serialize and deserialize the tree for visualization
    tree_json = json.dumps(serialize_tree(tree_root))
    tree_node = deserialize_tree(json.loads(tree_json))

    # Visualize and save the full race outcome tree
    visualize_tree_pyvis(tree_node, filename="full_race_outcome_tree.html", title="Full Race Outcome Tree")

    # Prune the tree to remove branches where Lando loses
    pruned_tree = prune_tree(tree_node)

    # Visualize and save the pruned race outcome tree
    visualize_tree_pyvis(pruned_tree, filename="pruned_race_outcome_tree.html", title="Pruned Race Outcome Tree")

if __name__ == "__main__":
    main()
