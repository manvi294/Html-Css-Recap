import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.chunk import tree2conlltags

# Download necessary NLTK data files (this step needs to be done only once)
# nltk.download('punkt')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')
# nltk.download('averaged_perceptron_tagger')

# Define custom mappings for specific terms
custom_mappings = {
    "California": "region",
    "New York": "region",
    "last week": "time",
    "yesterday": "time",
    # Add more mappings as needed
}

# Define a function to recognize entities using NLTK
def recognize_entities(text):
    # Tokenize the text
    words = word_tokenize(text)

    # Perform part-of-speech tagging
    pos_tags = pos_tag(words)

    # Perform named entity recognition
    ne_tree = ne_chunk(pos_tags)

    # Convert the tree to IOB format
    iob_tagged = tree2conlltags(ne_tree)

    # Initialize a list to hold the entities
    entities = []

    # Iterate over the IOB tagged data
    for word, pos, ne in iob_tagged:
        if ne != 'O':  # 'O' means not an entity
            entities.append((word, ne))
        else:
            # Check for custom mappings
            if word in custom_mappings:
                entities.append((word, custom_mappings[word]))

    return entities

# Function to label entities in a text
def label_entities(text):
    # Recognize entities using NLTK
    entities = recognize_entities(text)

    # Create a dictionary to hold the labels
    labeled_entities = {
        "branch/ATM/call": None,
        "high/low": None,
        "addon": None,
        "region": None,
        "time": None
    }

    # Define keywords for custom labels
    keywords = {
        "BRANCH": ["branch", "branches", "office"],
        "ATM": ["atm"],
        "CALL": ["call", "calls"],
        "HIGH": ["high", "highest", "top"],
        "LOW": ["low", "lowest", "bottom"],
        "CTR": ["ctr"],
        "MIR": ["mir"],
        "SAR": ["sar"]
    }

    # Label the entities
    for entity, label in entities:
        entity_lower = entity.lower()
        if any(entity_lower in keywords[key] for key in ["BRANCH", "ATM", "CALL"]):
            labeled_entities["branch/ATM/call"] = entity_lower
        elif any(entity_lower in keywords[key] for key in ["HIGH", "LOW"]):
            labeled_entities["high/low"] = entity_lower
        elif any(entity_lower in keywords[key] for key in ["CTR", "MIR", "SAR"]):
            labeled_entities["addon"] = entity_lower
        elif label == "GPE" or label == "region":
            labeled_entities["region"] = entity_lower
        elif label == "DATE" or label == "time":
            labeled_entities["time"] = entity_lower

    # Remove None values
    labeled_entities = {k: v for k, v in labeled_entities.items() if v is not None}

    return labeled_entities

# Main function for manual input and entity extraction
def main():
    # Example input
    text = input("Enter your query: ")

    # Label the entities
    labeled_entities = label_entities(text)

    # Print the labeled entities
    for label, value in labeled_entities.items():
        print(f"({label}: {value})")

if __name__ == "__main__":
    main()
