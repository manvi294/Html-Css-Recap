import json

class RedirectionEngine:
    def __init__(self, tree):
        self.tree = tree

    def get_follow_up_tags(self, current_tag):
        """Return the follow-up tags for the given current tag."""
        return self.tree.get(current_tag, [])

def load_tree_from_json(file_path):
    """Load the tree structure from a JSON file."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    tree = {}
    for item in data:
        question_tag = item['Question_Tag']
        next_tree = item['Next_tree']
        # Parse the Next_tree string to get a list of follow-up tags
        follow_up_tags = [tag.strip('[] ') for tag in next_tree.split(',')]
        # Remove empty strings that may result from parsing
        follow_up_tags = [tag for tag in follow_up_tags if tag]
        tree[question_tag] = follow_up_tags
    
    return tree

# Load the tree from the JSON file
file_path = 'labeltointentmapping.json'
question_tree = load_tree_from_json(file_path)

# Initialize the RedirectionEngine with the tree
engine = RedirectionEngine(question_tree)

# Example usage
current_tag = 'AtmDetail'
follow_up_tags = engine.get_follow_up_tags(current_tag)
print(follow_up_tags)  # Output: ['AtmDeposit', 'AtmWithdrawal', 'AtmOverall', 'AtmTraffic']

# To demonstrate moving through the tree
def navigate_tree(engine, start_tag):
    current_tag = start_tag
    while True:
        follow_up_tags = engine.get_follow_up_tags(current_tag)
        if not follow_up_tags:
            print(f"No more follow-up questions from '{current_tag}'")
            break
        print(f"From '{current_tag}' you can go to {follow_up_tags}")
        # For the sake of this example, we'll just pick the first follow-up tag
        current_tag = follow_up_tags[0]

# Start navigating from the 'AtmDetail' tag
navigate_tree(engine, 'AtmDetail')
