import spacy
from spacy.matcher import Matcher

# Load the small English model
nlp = spacy.load("en_core_web_sm")

# Custom mapping for specific entities to our labels
custom_mappings = {
    "California": "region",
    "New York": "region",
    "last week": "time",
    "yesterday": "time",
    # Add more mappings as needed
}

# Define a function to create custom entities
def create_custom_ner(text):
    # Initialize the matcher with the shared vocab
    matcher = Matcher(nlp.vocab)

    # Define patterns for matching custom entities including synonyms
    patterns = {
        "BRANCH": [{"LOWER": "branch"}, {"LOWER": "branches"}, {"LOWER": "office"}],
        "ATM": [{"LOWER": "atm"}],
        "CALL": [{"LOWER": "call"}, {"LOWER": "calls"}],
        "HIGH": [{"LOWER": "high"}, {"LOWER": "highest"}, {"LOWER": "top"}],
        "LOW": [{"LOWER": "low"}, {"LOWER": "lowest"}, {"LOWER": "bottom"}],
        "CTR": [{"LOWER": "ctr"}],
        "MIR": [{"LOWER": "mir"}],
        "SAR": [{"LOWER": "sar"}],
        "REGION_KEYWORDS": [{"LOWER": "region"}, {"LOWER": "r"}, {"LOWER": "east"}, {"LOWER": "west"}, {"LOWER": "north"}, {"LOWER": "south"}],
        "TIME_KEYWORDS": [{"LOWER": "time"}, {"LOWER": "period"}, {"LOWER": "month"}, {"LOWER": "year"}]
    }

    # Add patterns to the matcher
    for label, pattern_list in patterns.items():
        for pattern in pattern_list:
            matcher.add(label, [pattern])

    # Process the text with spaCy
    doc = nlp(text)

    # Apply the matcher to the doc
    matches = matcher(doc)

    # Initialize a list to hold the entities
    entities = []

    # Iterate over the matches
    for match_id, start, end in matches:
        # Get the matched span
        span = doc[start:end]
        # Append the span with its label to the entities list
        label = nlp.vocab.strings[match_id]
        entities.append((span.text, label))

    # Add entities detected by spaCy's built-in NER
    for ent in doc.ents:
        # Check if the entity is in the custom mappings
        if ent.text in custom_mappings:
            entities.append((ent.text, custom_mappings[ent.text]))
        else:
            entities.append((ent.text, ent.label_))

    return entities

# Function to label entities in a text
def label_entities(text):
    # Create custom entities
    entities = create_custom_ner(text)

    # Create a dictionary to hold the labels
    labeled_entities = {
        "branch/ATM/call": None,
        "high/low": None,
        "addon": None,
        "region": None,
        "time": None
    }

    # Label the entities
    for entity, label in entities:
        if label in ["BRANCH", "ATM", "CALL"]:
            labeled_entities["branch/ATM/call"] = entity.lower()
        elif label in ["HIGH", "LOW"]:
            labeled_entities["high/low"] = entity.lower()
        elif label in ["CTR", "MIR", "SAR"]:
            labeled_entities["addon"] = entity.lower()
        elif label == "REGION" or label == "GPE" or label == "REGION_KEYWORDS":
            labeled_entities["region"] = entity.lower()
        elif label == "TIME" or label == "TIME_KEYWORDS" or label == "DATE":
            labeled_entities["time"] = entity.lower()

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
