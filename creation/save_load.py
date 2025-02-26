import json
import os

def save_character(character, filename):
    """Save the character data to a JSON file."""
    with open(filename, 'w') as file:
        json.dump(character.to_dict(), file, indent=4)

def load_character(filename):
    """Load character data from a JSON file."""
    with open(filename, 'r') as file:
        data = json.load(file)
        character = Character()
        character.set_race(data['race'])
        character.set_class(data['class'])
        character.set_background(data['background'])
        character.set_abilities(data['abilities'])
        return character

def load_data(filename):
    """Load data (races, classes, etc.) from a JSON file."""
    file_path = os.path.join('resources', filename)  # Ensure correct path to resources folder
    with open(file_path, 'r') as file:
        return json.load(file)
