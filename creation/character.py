class Character:
    def __init__(self):
        self.race = ""
        self.subrace = None  # Initialize subrace as None
        self.char_class = ""
        self.background = ""
        self.abilities = {}

    def set_race(self, race):
        self.race = race

    def set_subrace(self, subrace):
        self.subrace = subrace  # Store subrace information

    def set_class(self, char_class):
        self.char_class = char_class

    def set_background(self, background):
        self.background = background

    def set_abilities(self, abilities):
        self.abilities = abilities

    def __str__(self):
        # Print race and subrace if subrace exists
        return (f"Character:\nRace: {self.race} {f'({self.subrace})' if self.subrace else ''}\n"
                f"Class: {self.char_class}\nBackground: {self.background}\n"
                f"Abilities: {', '.join([f'{k}: {v}' for k, v in self.abilities.items()])}")

    def to_dict(self):
        # Include subrace in the dictionary when saving the character
        return {
            "race": self.race,
            "subrace": self.subrace,  # Save subrace to JSON
            "class": self.char_class,
            "background": self.background,
            "abilities": self.abilities
        }
