import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.chunk import tree2conlltags
import re

# Uncomment the following lines to download NLTK data files if not already downloaded
# nltk.download('punkt')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')
# nltk.download('averaged_perceptron_tagger')

# Define custom mappings for specific terms
custom_mappings = {
    "yesterday": "time",
    # Add more mappings as needed
}

# Define patterns for time extraction
time_pattern = re.compile(r'\b(\d{1,2}\s+\w+\s+\d{4}|\d{1,2}\s+\w+)\b')

# List of US states to be recognized as regions
us_states = {"Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida",
             "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine",
             "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska",
             "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
             "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas",
             "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"}

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
        elif word in custom_mappings:
            entities.append((word, custom_mappings[word]))
        elif word in us_states:
            entities.append((word, "region"))

    return entities

# Function to extract time periods
def extract_time_periods(text):
    times = re.findall(time_pattern, text)
    if len(times) == 2:
        return times[0], times[1]
    return None, None

# Function to label entities in a text
def label_entities(text):
    # Recognize entities using NLTK
    entities = recognize_entities(text)

    # Extract time periods
    time_start, time_end = extract_time_periods(text)

    # Create a dictionary to hold the labels
    labeled_entities = {
        "branch/ATM/call": None,
        "high/low": None,
        "addon": None,
        "region": None,
        "time_start": None,
        "time_end": None,
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

    # Add extracted time periods to the dictionary
    if time_start:
        labeled_entities["time_start"] = time_start
    if time_end:
        labeled_entities["time_end"] = time_end

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
