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
root.title("D&D Character Creator (v0.7)")

# Create a character object, passing races data
character = Character(races, backgrounds)

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
    selected_class = class_combobox.get()
    
    # Check if the class has changed before resetting related items
    if character.char_class != selected_class:
        # Reset class-related attributes (items, abilities, etc.)
        character.reset_class_related_attributes()
        
    character.set_class(selected_class)
    character.set_background(background_combobox.get())
    character.apply_starting_items()
    
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

# Function to view inventory
def view_inventory():
    character.view_inventory()

# Function to add an item to inventory
def add_item():
    item = item_entry.get()
    if item:
        character.add_item_to_inventory(item)
    else:
        messagebox.showwarning("Invalid Input", "Please enter an item name.")

# Function to remove an item from inventory
def remove_item():
    item = item_entry.get()
    if item:
        character.remove_item_from_inventory(item)
    else:
        messagebox.showwarning("Invalid Input", "Please enter an item name.")

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
tk.Label(root, text="Enter Ability Scores (1-20) - Standard Array: 15, 14, 13, 12, 10, 8").grid(row=5, column=0, columnspan=2, padx=10, pady=5)
ability_entries = {}
for idx, ability in enumerate(abilities):
    tk.Label(root, text=ability).grid(row=6 + idx, column=0, padx=10, pady=5)
    ability_entries[ability] = tk.Entry(root)
    ability_entries[ability].grid(row=6 + idx, column=1, padx=10, pady=5)

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

# Widgets for Inventory Section (initially placed in default position)
view_button = tk.Button(root, text="View Inventory", command=view_inventory)
add_button = tk.Button(root, text="Add Item to Inventory", command=add_item)
remove_button = tk.Button(root, text="Remove Item from Inventory", command=remove_item)
item_entry = tk.Entry(root)

# Default position for inventory
view_button.grid(row=6 + len(abilities) + 1, column=0, padx=10, pady=5)
item_entry.grid(row=6 + len(abilities) + 1, column=1, padx=10, pady=5)
add_button.grid(row=6 + len(abilities) + 3, column=0, padx=10, pady=5)
remove_button.grid(row=6 + len(abilities) + 4, column=0, padx=10, pady=5)

# Buttons for Update/Save Character (placed after the inventory section)
update_button = tk.Button(root, text="Update Character", command=update_character)
update_button.grid(row=6 + len(abilities) + 5, column=0, padx=10, pady=10)

save_button = tk.Button(root, text="Save Character", command=save_char)
save_button.grid(row=6 + len(abilities) + 5, column=1, padx=10, pady=10)

# Bind event to update subrace options when race changes
def on_race_selected(event):
    selected_race = race_combobox.get()

    # First hide the subrace components
    subrace_label.grid_forget()
    subrace_combobox.grid_forget()

    # Get subraces directly from the races dictionary
    subrace_list = races.get(selected_race, {}).get('subraces', [])

    if subrace_list:  # If subraces exist for the selected race
        subrace_combobox['values'] = subrace_list
        subrace_label.grid(row=4, column=0, padx=10, pady=5)
        subrace_combobox.grid(row=4, column=1, padx=10, pady=5)

    # If Variant Human or Half-Elf, show ability bonus selectors
    if selected_race in ["Variant Human", "Half-Elf"]:
        racial_bonus1_label.grid(row=6 + len(abilities) + 6, column=0, padx=10, pady=5)
        racial_bonus1_combobox.grid(row=6 + len(abilities) + 6, column=1, padx=10, pady=5)

        racial_bonus2_label.grid(row=6 + len(abilities) + 7, column=0, padx=10, pady=5)
        racial_bonus2_combobox.grid(row=6 + len(abilities) + 7, column=1, padx=10, pady=5)

        # Move inventory section lower
        view_button.grid(row=6 + len(abilities) + 9, column=0, padx=10, pady=5)
        item_entry.grid(row=6 + len(abilities) + 9, column=1, padx=10, pady=5)
        add_button.grid(row=6 + len(abilities) + 11, column=0, padx=10, pady=5)
        remove_button.grid(row=6 + len(abilities) + 12, column=0, padx=10, pady=5)

        update_button.grid(row=6 + len(abilities) + 13, column=0, padx=10, pady=10)
        save_button.grid(row=6 + len(abilities) + 13, column=1, padx=10, pady=10)
    else:
        # Reset positions if not Half-Elf or Variant Human
        racial_bonus1_label.grid_forget()
        racial_bonus1_combobox.grid_forget()
        racial_bonus2_label.grid_forget()
        racial_bonus2_combobox.grid_forget()

        view_button.grid(row=6 + len(abilities) + 1, column=0, padx=10, pady=5)
        item_entry.grid(row=6 + len(abilities) + 1, column=1, padx=10, pady=5)
        add_button.grid(row=6 + len(abilities) + 3, column=0, padx=10, pady=5)
        remove_button.grid(row=6 + len(abilities) + 4, column=0, padx=10, pady=5)

        update_button.grid(row=6 + len(abilities) + 5, column=0, padx=10, pady=10)
        save_button.grid(row=6 + len(abilities) + 5, column=1, padx=10, pady=10)

# List of races that have subraces (you can modify this list based on your data)
races_with_subraces = ['Elf', 'Dwarf', 'Halfling']  # Example, add your races that have subraces

# Bind race change event to on_race_selected
race_combobox.bind("<<ComboboxSelected>>", on_race_selected)

root.mainloop()