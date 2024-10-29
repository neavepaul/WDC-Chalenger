from backend.tree import build_tree, print_winning_paths

# Remaining races (sprint + normal races)
remaining_races = ["sprint", "main", "main", "main"]  # Brazil sprint, Las Vegas, Qatar sprint, Abu Dhabi

# Initial points for Max and Lando
initial_max_points = 200
initial_lando_points = 185

# Build tree of possibilities
root = build_tree(initial_max_points, initial_lando_points, remaining_races)

# Print winning paths for Lando
print("Winning paths for Lando:")
print_winning_paths(root)
