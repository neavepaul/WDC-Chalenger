import itertools

main_race_points = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1, "no_points": 0}
sprint_race_points = {1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1, "no_points": 0}

race_schedule = {
    "Brazil": {"type": "sprint", "main_date": "2024-11-03", "sprint_date": "2024-11-02"},
    "Las Vegas": {"type": "main", "main_date": "2024-11-18"},
    "Qatar": {"type": "sprint", "main_date": "2024-12-01", "sprint_date": "2024-11-30"},
    "Abu Dhabi": {"type": "main", "main_date": "2024-12-08"}
}

def calculate_points(finish_pos, race_type="main"):
    """Calculate points for a given position and race type (main or sprint)."""
    if finish_pos == "no_points":
        return 0
    if race_type == "main":
        return main_race_points.get(finish_pos, 0)
    elif race_type == "sprint":
        return sprint_race_points.get(finish_pos, 0)
    return 0

def simulate_race_outcomes(race_type="main"):
    """Generate all possible outcomes for Max and Lando, avoiding same positions based on race type."""
    if race_type == "sprint":
        positions = list(range(1, 9)) + ["no_points"]  # Top 8 positions in sprint
    else:
        positions = list(range(1, 11)) + ["no_points"]  # Top 10 positions in main race

    # All valid (Max, Lando) pairs, ensuring they don't finish in the same position
    combinations = itertools.product(positions, repeat=2)
    
    # Filter out cases where Max and Lando finish in the same position
    valid_outcomes = [(max_pos, lando_pos) for max_pos, lando_pos in combinations if max_pos != lando_pos]

    # Append the case where both Max and Lando finish outside points
    valid_outcomes.append(("no_points", "no_points"))

    return valid_outcomes
