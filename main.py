from creation.save_load import load_data  # Import load_data function
from creation.character import Character
from creation.dice import roll_dice, roll_ability
from creation.save_load import save_character

# Load data from JSON files
races = load_data('races.json')
classes = load_data('classes.json')
backgrounds = load_data('backgrounds.json')
abilities = load_data('abilities.json')

# Setup the main window
import tkinter as tk
from tkinter import ttk, messagebox

root = tk.Tk()
root.title("D&D Character Creator (v0.5.1)")

# Create a character object, passing races data
character = Character(races)

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
    
    if race in ["Half-Elf", "Variant Human"]:
        # Show the +1 ability selection boxes if race is Half-Elf or Variant Human
        racial_bonus1_combobox.grid(row=8 + len(abilities), column=1, padx=10, pady=5)
        racial_bonus2_combobox.grid(row=9 + len(abilities), column=1, padx=10, pady=5)
        racial_bonus1_label.grid(row=8 + len(abilities), column=0, padx=10, pady=5)
        racial_bonus2_label.grid(row=9 + len(abilities), column=0, padx=10, pady=5)
    else:
        # Hide the +1 ability selection boxes if race is not Half-Elf or Variant Human
        racial_bonus1_combobox.grid_forget()
        racial_bonus2_combobox.grid_forget()
        racial_bonus1_label.grid_forget()
        racial_bonus2_label.grid_forget()

    if subrace_options:  # If the race has subraces
        subrace_combobox['values'] = subrace_options
        subrace_combobox.grid(row=4, column=1, padx=10, pady=5)  # Show the subrace combobox
        subrace_label.grid(row=4, column=0, padx=10, pady=5)  # Display the label for subrace
    else:  # If no subraces, hide the subrace combobox
        subrace_combobox.grid_forget()
        subrace_label.grid_forget()

# Function to update selected character data (including name, race, subrace, etc.)
def update_character():
    # Fetch the character's name
    character_name = name_entry.get()  # Get the name from the entry field
    character.set_name(character_name)  # Set the character's name

    # Fetch race and subrace information
    race = race_combobox.get()
    subrace = subrace_combobox.get() if subrace_combobox.winfo_ismapped() else None  # Only fetch subrace if visible

    # Set the race and subrace
    character.set_race(race)
    character.set_subrace(subrace)  # Store the selected subrace
    
    # Set class and background
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
    
    # Set abilities based on user input
    character.set_abilities(selected_abilities)
    
    # If Half-Elf or Variant Human, apply the +1 bonuses to two abilities
    if race in ["Half-Elf", "Variant Human"]:
        bonus1 = racial_bonus1_combobox.get()
        bonus2 = racial_bonus2_combobox.get()

        if bonus1 and bonus2:  # Make sure both bonuses are selected
            character.abilities[bonus1] += 1
            character.abilities[bonus2] += 1
    
    # Now apply race bonuses to the abilities
    character.apply_race_bonus()
    
    # Print updated character info with bonuses applied
    print(character)



# Function to save the character to a file
def save_char():
    save_character(character, 'character.json')
    print("Character saved!")

# GUI Widgets
tk.Label(root, text="Enter Character Name").grid(row=0, column=0, padx=10, pady=5)
name_entry = tk.Entry(root)  # Create an entry widget for the character name
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Select Race").grid(row=1, column=0, padx=10, pady=5)
race_combobox = ttk.Combobox(root, values=list(races.keys()))
race_combobox.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Select Class").grid(row=2, column=0, padx=10, pady=5)
class_combobox = ttk.Combobox(root, values=list(classes.keys()))
class_combobox.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Select Background").grid(row=3, column=0, padx=10, pady=5)
background_combobox = ttk.Combobox(root, values=list(backgrounds.keys()))
background_combobox.grid(row=3, column=1, padx=10, pady=5)

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

# Initially hide the labels and ComboBoxes for +1 ability bonus selection
racial_bonus1_label = tk.Label(root, text="Select First Ability for +1")
racial_bonus1_combobox = ttk.Combobox(root, values=list(abilities.keys()))

racial_bonus2_label = tk.Label(root, text="Select Second Ability for +1")
racial_bonus2_combobox = ttk.Combobox(root, values=list(abilities.keys()))

# Initially hide them
racial_bonus1_label.grid_forget()  
racial_bonus1_combobox.grid_forget()

racial_bonus2_label.grid_forget()  
racial_bonus2_combobox.grid_forget()


# Buttons
update_button = tk.Button(root, text="Update Character", command=update_character)
update_button.grid(row=7 + len(abilities), column=0, padx=10, pady=10)

save_button = tk.Button(root, text="Save Character", command=save_char)
save_button.grid(row=7 + len(abilities), column=1, padx=10, pady=10)

root.mainloop()