from creation.character import Character
from creation.dice import roll_dice, roll_ability
from creation.save_load import load_data, save_character

# Load data from JSON files
races = load_data('races.json')
classes = load_data('classes.json')
backgrounds = load_data('backgrounds.json')
abilities = load_data('abilities.json')

# Setup the main window
import tkinter as tk
from tkinter import ttk, messagebox

root = tk.Tk()
root.title("D&D Character Creator")

# Create a character object
character = Character()

# Function to validate ability score input
def validate_ability_score(entry):
    try:
        value = int(entry.get())
        if value < 1 or value > 20:
            raise ValueError("Ability scores must be between 1 and 20.")
        return value
    except ValueError as e:
        messagebox.showerror("Invalid Input", f"Please enter a valid ability score between 1 and 20.\nError: {e}")
        return None

# Function to update selected character data
def update_character():
    character.set_race(race_combobox.get())
    character.set_class(class_combobox.get())
    character.set_background(background_combobox.get())
    
    # Validate and update ability scores
    selected_abilities = {}
    for ability, entry in ability_entries.items():
        score = validate_ability_score(entry)
        if score is not None:
            selected_abilities[ability] = score
        else:
            return  # Stop if any input is invalid
    
    character.set_abilities(selected_abilities)
    print(character)

# Function to save the character to a file
def save_char():
    save_character(character, 'character.json')
    print("Character saved!")

# GUI Widgets
tk.Label(root, text="Select Race").grid(row=0, column=0, padx=10, pady=5)
race_combobox = ttk.Combobox(root, values=list(races.keys()))
race_combobox.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Select Class").grid(row=1, column=0, padx=10, pady=5)
class_combobox = ttk.Combobox(root, values=list(classes.keys()))
class_combobox.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Select Background").grid(row=2, column=0, padx=10, pady=5)
background_combobox = ttk.Combobox(root, values=list(backgrounds.keys()))
background_combobox.grid(row=2, column=1, padx=10, pady=5)

# Ability Scores Input
tk.Label(root, text="Enter Ability Scores (1-20)").grid(row=3, column=0, padx=10, pady=5)
ability_entries = {}
for idx, ability in enumerate(abilities):
    tk.Label(root, text=ability).grid(row=4 + idx, column=0, padx=10, pady=5)
    ability_entries[ability] = tk.Entry(root)
    ability_entries[ability].grid(row=4 + idx, column=1, padx=10, pady=5)

# Ensure there's enough space for all rows by configuring row expansion
# Configure grid rows to allow them to expand dynamically
for i in range(3, 10):  # Rows 3 to 9 correspond to abilities and buttons
    root.grid_rowconfigure(i, weight=1)

# Configure grid to handle the layout properly
root.grid_rowconfigure(0, weight=0)  # Race label row
root.grid_rowconfigure(1, weight=0)  # Class label row
root.grid_rowconfigure(2, weight=0)  # Background label row

# Move the buttons to a higher row to prevent overlap
update_button = tk.Button(root, text="Update Character", command=update_character)
update_button.grid(row=10, column=0, padx=10, pady=10)

save_button = tk.Button(root, text="Save Character", command=save_char)
save_button.grid(row=10, column=1, padx=10, pady=10)

root.mainloop()
