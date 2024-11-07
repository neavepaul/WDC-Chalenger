import pickle
import random
from groq import Groq
from dotenv import load_dotenv

def generate_story(tree_node, probability_of_lando_winning):
    """Generate a story based on a random path leading to Lando's victory and save it to a text file."""
    story_lines = []

    def traverse(node, depth=0):
        if depth == 0:
            story_lines.append("This is a situation where Lando can win the WDC in F1...\nPoints as of Brazil GP are Max: 393, Lando: 331\n")
            story_lines.append(f"Probability of Lando winning the WDC is {probability_of_lando_winning:.2f}\n")
        
        race_desc = node.description.get("race", "unknown race")
        max_pos = node.description.get("max_position", "unknown")
        lando_pos = node.description.get("lando_position", "unknown")

        # Add details of the current race to the story
        story_lines.append(f"In {race_desc}, Max finished in position {max_pos}, while Lando was in position {lando_pos}. Points after race: Max: {node.max_points}, Lando: {node.lando_points}")

        # Randomly pick one child to traverse down the path
        if node.children:
            next_node = random.choice(node.children)
            traverse(next_node, depth + 1)

    traverse(tree_node)
    return "\n".join(story_lines)

def load_tree_from_pickle(filename="tree_node.pkl"):
    """Load the tree node from a pickle file."""
    with open(filename, 'rb') as file:
        return pickle.load(file)

def main():
    tree_node = load_tree_from_pickle()
    
    # read the probability of Lando winning from the text file
    with open("lando_prob.txt", "r") as file:
        probability_of_lando_winning = float(file.read().split()[-1])
    
    story = generate_story(tree_node, probability_of_lando_winning)
    
    load_dotenv()
    client = Groq()
    completion = client.chat.completions.create(
        model="llama-3.2-90b-vision-preview",
        messages=[
            {
                "role": "system",
                "content": "You are F1GPT, given context about season outcomes, create an enthralling story detailing the four races that led to Lando winning the WDC. Also, talk about strategies and events."
            },
            {
                "role": "user",
                "content": story
            },
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )

    # save the story to a markdown file
    with open("story.txt", "w") as file:
        file.write(completion.choices[0].message.content)

if __name__ == "__main__":
    main()