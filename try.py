# To keep track of whether the drill question has been asked
drill_asked = False

def handle_redirection(scenario_tag, follow_up):
    global drill_asked

    # Check for the next follow-up question
    next_follow_up = follow_up + 1
    
    # Find the next follow-up in the tags
    next_entry = next((entry for entry in tags if entry['Scenario Tag'] == scenario_tag and entry['Follow Up'] == next_follow_up), None)
    
    if next_entry:
        # Return the next follow-up question
        return next_entry['Question Tag']
    else:
        if not drill_asked:
            # If no next follow-up exists, return the drill question
            drill_entry = next((entry for entry in tags if entry['Scenario Tag'] == 'drill' and entry['Follow Up'] == 100), None)
            drill_asked = True  # Set flag to indicate drill question has been asked
            
            if drill_entry:
                return drill_entry['Question Tag']
            else:
                return "Thanks for your input!"
        else:
            return "Thanks for your input!"

# Main function for manual input and entity extraction
def main():
    global drill_asked

    # Reset drill_asked flag for each new input
    drill_asked = False

    # Example input
    text = input("Enter your query: ")

    # Label the entities
    labeled_entities = label_entities(text)

    # Print the labeled entities
    for label, value in labeled_entities.items():
        print(f"({label}: {value})")

    # Determine initial scenario tag and follow-up
    scenario_tag, follow_up = map_entities_to_tag(labeled_entities)
    
    if scenario_tag is None or follow_up is None:
        print("Could not determine scenario tag or follow-up.")
        return

    # Handle redirection based on the scenario tag and follow-up
    response = handle_redirection(scenario_tag, follow_up)
    print(response)

if __name__ == "__main__":
    main()
