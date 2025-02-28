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
root.title("D&D Character Creator (v0.2)")

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

# Function to update the subrace Combobox based on the selected race
def update_subrace_options():
    race = race_combobox.get()
    subrace_options = races.get(race, {}).get('subraces', [])
    
    if subrace_options:  # If the race has subraces
        subrace_combobox['values'] = subrace_options
        subrace_combobox.grid(row=4, column=1, padx=10, pady=5)  # Show the subrace combobox
        subrace_label.grid(row=4, column=0, padx=10, pady=5)  # Display the label for subrace
    else:  # If no subraces, hide the subrace combobox
        subrace_combobox.grid_forget()
        subrace_label.grid_forget()

# Function to update selected character data (including subrace)
def update_character():
    race = race_combobox.get()
    subrace = subrace_combobox.get() if subrace_combobox.winfo_ismapped() else None  # Only fetch subrace if visible
    character.set_race(race)
    character.set_subrace(subrace)  # Store the selected subrace
    
    # Continue with the rest of the character setup
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

# Subrace Selection Widgets (before the ability scores)
subrace_label = tk.Label(root, text="Select Subrace (if applicable)")
subrace_combobox = ttk.Combobox(root, values=[])
subrace_combobox.grid_forget()  # Hide it initially

# Ability Scores Input
tk.Label(root, text="Enter Ability Scores (1-20)").grid(row=5, column=0, padx=10, pady=5)
ability_entries = {}
for idx, ability in enumerate(abilities):
    tk.Label(root, text=ability).grid(row=6 + idx, column=0, padx=10, pady=5)
    ability_entries[ability] = tk.Entry(root)
    ability_entries[ability].grid(row=6 + idx, column=1, padx=10, pady=5)

# Bind event to update subrace options when race changes
race_combobox.bind("<<ComboboxSelected>>", lambda event: update_subrace_options())

# Ensure enough space for rows and dynamic widgets
root.grid_rowconfigure(0, weight=0)  # Race label row
root.grid_rowconfigure(1, weight=0)  # Class label row
root.grid_rowconfigure(2, weight=0)  # Background label row

# Ability Scores
root.grid_rowconfigure(5, weight=0)  # Ability Scores label
for i in range(6, 6 + len(abilities)):  # Ability scores inputs
    root.grid_rowconfigure(i, weight=0)

# Subrace
root.grid_rowconfigure(4, weight=0)  # Make space for subrace row

# Buttons
update_button = tk.Button(root, text="Update Character", command=update_character)
update_button.grid(row=7 + len(abilities), column=0, padx=10, pady=10)

save_button = tk.Button(root, text="Save Character", command=save_char)
save_button.grid(row=7 + len(abilities), column=1, padx=10, pady=10)

root.mainloop()
