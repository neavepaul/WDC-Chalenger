import itertools

# Define points for each position
race_points = {1: 25, 2: 18, "no_points": 0}
# race_points = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1, "no_points": 0}

def calculate_points(finish_pos):
    """Calculate points for a given position."""
    return race_points.get(finish_pos, 0)

def simulate_race_outcomes():
    """Generate all possible outcomes for Max and Lando."""
    positions = [1, 2,"no_points"]  # Only 2 positions + "no points"

    # Generate all combinations of Max's and Lando's positions
    combinations = itertools.product(positions, repeat=2)

    # Filter out cases where Max and Lando finish in the same position
    valid_outcomes = [(max_pos, lando_pos) for max_pos, lando_pos in combinations if max_pos != lando_pos]

    return valid_outcomes
