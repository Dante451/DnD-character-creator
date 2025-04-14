class Character:
    def __init__(self, races, backgrounds):
        self.name = ""  # Add name attribute
        self.race = ""
        self.subrace = None  # Initialize subrace as None
        self.char_class = ""
        self.backgrounds = backgrounds
        self.previous_background = None
        self.abilities = {}
        self.races = races  # Store the races data to reference race bonuses
        self.inventory = []  # Initialize an empty inventory
        self.background_items = []

    def reset_class_related_attributes(self):
        """Resets only the class-specific attributes."""
        self.items = []  # Reset class-specific starting items
        self.abilities.clear()  # Clear class-specific abilities (if needed)
        print("Class-related attributes reset.")

    def set_name(self, name):
        self.name = name  # Set the name for the character

    def set_race(self, race):
        """Set the character's race."""
        self.race = race
        print(f"Race set to: {self.race}")

    def set_subrace(self, subrace):
        self.subrace = subrace  # Store subrace information

    def set_class(self, char_class):
        self.char_class = char_class

    def set_background(self, background):
        self.background = background

    def set_abilities(self, abilities):
        self.abilities = abilities

    def apply_race_bonus(self):
        """Apply race-specific ability bonuses to the entered ability scores."""
        
        race_data = self.races.get(self.race, {})
        print(f"Applying race bonus for {self.race} - Subrace: {self.subrace}")
        
        # Dwarf
        if self.race == "Dwarf":
            if self.subrace == "Hill Dwarf":
                self.abilities["Constitution"] += 2  # Hill Dwarf gets +2 Constitution
                self.abilities["Wisdom"] += 1  # Hill Dwarf gets +1 Wisdom
            elif self.subrace == "Mountain Dwarf":
                self.abilities["Strength"] += 2  # Mountain Dwarf gets +2 Strength
                self.abilities["Constitution"] += 2  # Mountain Dwarf gets +2 Constitution
            else:
                self.abilities["Constitution"] += 2  # Default Dwarf bonus
        
        # Elf
        elif self.race == "Elf":
            if self.subrace == "High Elf":
                self.abilities["Dexterity"] += 2  # High Elf gets +2 Dexterity
                self.abilities["Intelligence"] += 1  # High Elf gets +1 Intelligence
            elif self.subrace == "Wood Elf":
                self.abilities["Dexterity"] += 2  # Wood Elf gets +2 Dexterity
                self.abilities["Wisdom"] += 1  # Wood Elf gets +1 Wisdom
            elif self.subrace == "Dark Elf (Drow)":
                self.abilities["Dexterity"] += 2  # Drow gets +2 Dexterity
                self.abilities["Charisma"] += 1  # Drow gets +1 Charisma
            else:
                self.abilities["Dexterity"] += 2  # Default Elf bonus
        
        # Halfling
        elif self.race == "Halfling":
            if self.subrace == "Lightfoot Halfling":
                self.abilities["Dexterity"] += 2  # Lightfoot Halfling gets +2 Dexterity
                self.abilities["Charisma"] += 1  # Lightfoot Halfling gets +1 Charisma
            elif self.subrace == "Stout Halfling":
                self.abilities["Dexterity"] += 2  # Stout Halfling gets +2 Dexterity
                self.abilities["Constitution"] += 1  # Stout Halfling gets +1 Constitution
            else:
                self.abilities["Dexterity"] += 2  # Default Halfling bonus
        
        # Human
        elif self.race == "Human":
            if hasattr(self, "variant_human_bonus_abilities"):  # Ensure it's set
                for ability in self.racial_bonus_abilities:
                    self.abilities[ability] += 1
            else:
                self.abilities["Strength"] += 1  # Human gets +1 to all abilities
                self.abilities["Dexterity"] += 1
                self.abilities["Constitution"] += 1
                self.abilities["Intelligence"] += 1
                self.abilities["Wisdom"] += 1
                self.abilities["Charisma"] += 1
        
        # Dragonborn
        elif self.race == "Dragonborn":
            self.abilities["Charisma"] += 2  # Dragonborn gets +2 Charisma
            self.abilities["Strength"] += 2  # Dragonborn gets +2 Strength
        
        # Gnome
        elif self.race == "Gnome":
            if self.subrace == "Forest Gnome":
                self.abilities["Intelligence"] += 2  # Forest Gnome gets +2 Intelligence
                self.abilities["Dexterity"] += 1  # Forest Gnome gets +1 Dexterity
            elif self.subrace == "Rock Gnome":
                self.abilities["Intelligence"] += 2  # Rock Gnome gets +2 Intelligence
                self.abilities["Constitution"] += 1  # Rock Gnome gets +1 Constitution
            else:
                self.abilities["Intelligence"] += 2  # Default Gnome bonus
        
        # Half-Elf
        elif self.race == "Half-Elf":
            self.abilities["Charisma"] += 2
        # Apply +1 to selected abilities
            if hasattr(self, "half_elf_bonus_abilities"):  # Ensure it's set
                for ability in self.racial_bonus_abilities:
                    self.abilities[ability] += 1
        
        # Half-Orc
        elif self.race == "Half-Orc":
            self.abilities["Strength"] += 2  # Half-Orc gets +2 Strength
            self.abilities["Constitution"] += 1  # Half-Orc gets +1 Constitution
        
        # Tiefling
        elif self.race == "Tiefling":
            self.abilities["Charisma"] += 2  # Tiefling gets +2 Charisma
            self.abilities["Intelligence"] += 1  # Tiefling gets +1 Intelligence
        
        # Aarakocra
        elif self.race == "Aarakocra":
            self.abilities["Dexterity"] += 2  # Aarakocra gets +2 Dexterity
            self.abilities["Wisdom"] += 1  # Aarakocra gets +1 Wisdom
        
        # Genasi
        elif self.race == "Genasi":
            if self.subrace == "Air Genasi":
                self.abilities["Dexterity"] += 2  # Air Genasi gets +2 Dexterity
                self.abilities["Intelligence"] += 1  # Air Genasi gets +1 Intelligence
            elif self.subrace == "Earth Genasi":
                self.abilities["Constitution"] += 2  # Earth Genasi gets +2 Constitution
                self.abilities["Strength"] += 1  # Earth Genasi gets +1 Strength
            elif self.subrace == "Fire Genasi":
                self.abilities["Intelligence"] += 2  # Fire Genasi gets +2 Intelligence
                self.abilities["Charisma"] += 1  # Fire Genasi gets +1 Charisma
            elif self.subrace == "Water Genasi":
                self.abilities["Constitution"] += 2  # Water Genasi gets +2 Constitution
                self.abilities["Wisdom"] += 1  # Water Genasi gets +1 Wisdom
        
        # Githyanki
        elif self.race == "Githyanki":
            self.abilities["Intelligence"] += 2  # Githyanki gets +2 Intelligence
            self.abilities["Strength"] += 1  # Githyanki gets +1 Strength
        
        # Githzerai
        elif self.race == "Githzerai":
            self.abilities["Intelligence"] += 2  # Githzerai gets +2 Intelligence
            self.abilities["Wisdom"] += 1  # Githzerai gets +1 Wisdom
        
        # Tabaxi
        elif self.race == "Tabaxi":
            self.abilities["Dexterity"] += 2  # Tabaxi gets +2 Dexterity
            self.abilities["Charisma"] += 1  # Tabaxi gets +1 Charisma
        
        # Triton
        elif self.race == "Triton":
            self.abilities["Strength"] += 1  # Triton gets +1 Strength
            self.abilities["Constitution"] += 1  # Triton gets +1 Constitution
            self.abilities["Wisdom"] += 1  # Triton gets +1 Wisdom
        
        # Firbolg
        elif self.race == "Firbolg":
            self.abilities["Strength"] += 2  # Firbolg gets +2 Strength
            self.abilities["Wisdom"] += 1  # Firbolg gets +1 Wisdom
        
        # Kenku
        elif self.race == "Kenku":
            self.abilities["Dexterity"] += 2  # Kenku gets +2 Dexterity
            self.abilities["Wisdom"] += 1  # Kenku gets +1 Wisdom
        
        # Lizardfolk
        elif self.race == "Lizardfolk":
            self.abilities["Constitution"] += 2  # Lizardfolk gets +2 Constitution
            self.abilities["Dexterity"] += 1  # Lizardfolk gets +1 Dexterity
        
        # Hobgoblin
        elif self.race == "Hobgoblin":
            self.abilities["Constitution"] += 2  # Hobgoblin gets +2 Constitution
            self.abilities["Intelligence"] += 1  # Hobgoblin gets +1 Intelligence
        
        # Yuan-Ti Pureblood
        elif self.race == "Yuan-Ti Pureblood":
            self.abilities["Charisma"] += 2  # Yuan-Ti Pureblood gets +2 Charisma
            self.abilities["Intelligence"] += 1  # Yuan-Ti Pureblood gets +1 Intelligence
        
        # Changeling
        elif self.race == "Changeling":
            self.abilities["Charisma"] += 2  # Changeling gets +2 Charisma
            self.abilities["Dexterity"] += 1  # Changeling gets +1 Dexterity
        
        # Kalashtar
        elif self.race == "Kalashtar":
            self.abilities["Wisdom"] += 2  # Kalashtar gets +2 Wisdom
            self.abilities["Charisma"] += 1  # Kalashtar gets +1 Charisma
        
        # Shifter
        elif self.race == "Shifter":
            self.abilities["Dexterity"] += 2  # Shifter gets +2 Dexterity
            self.abilities["Constitution"] += 1  # Shifter gets +1 Constitution
        
        # Warforged
        elif self.race == "Warforged":
            self.abilities["Constitution"] += 2  # Warforged gets +2 Constitution
            self.abilities["Strength"] += 1  # Warforged gets +1 Strength
        
        # Vedalken
        elif self.race == "Vedalken":
            self.abilities["Intelligence"] += 2  # Vedalken gets +2 Intelligence
            self.abilities["Wisdom"] += 1  # Vedalken gets +1 Wisdom
        
        print(f"Updated abilities after race bonus: {self.abilities}")

    def apply_starting_items(self):
        """Add starting items to inventory, only if background has changed."""
        if self.background != self.previous_background:
            starting_items = self.backgrounds.get(self.background, {}).get("items", [])
            self.inventory.extend(starting_items)
            self.previous_background = self.background  # Update tracker
            print(f"Added starting items for new background '{self.background}': {starting_items}")
        else:
            print(f"Background '{self.background}' already applied. No items added.")

    
    def add_item_to_inventory(self, item):
        """Add an item to the character's inventory."""
        self.inventory.append(item)
        print(f"Added {item} to inventory.")

    def remove_item_from_inventory(self, item):
        """Remove an item from the character's inventory."""
        if item in self.inventory:
            self.inventory.remove(item)
            print(f"Removed {item} from inventory.")
        else:
            print(f"{item} not found in inventory.")

    def view_inventory(self):
        """Display all items in the character's inventory."""
        if self.inventory:
            print("Inventory:")
            for item in self.inventory:
                print(f"- {item}")
        else:
            print("Inventory is empty.")

    def __str__(self):
        # Print race and subrace if subrace exists
        return (f"Character:\nRace: {self.race} {f'({self.subrace})' if self.subrace else ''}\n"
                f"Class: {self.char_class}\nBackground: {self.background}\n"
                f"Abilities: {', '.join([f'{k}: {v}' for k, v in self.abilities.items()])}\n"
                f"Inventory: {', '.join(self.inventory) if self.inventory else 'No items'}")

    def to_dict(self):
        """Return the character data as a dictionary, including name, abilities, and inventory."""
        return {
            "name": self.name,  
            "race": self.race,
            "subrace": self.subrace,  
            "class": self.char_class,
            "background": self.background,
            "abilities": self.abilities,
            "inventory": self.inventory  
        }