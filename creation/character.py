class Character:
    def __init__(self):
        self.race = ""
        self.char_class = ""
        self.background = ""
        self.abilities = {}

    def set_race(self, race):
        self.race = race

    def set_class(self, char_class):
        self.char_class = char_class

    def set_background(self, background):
        self.background = background

    def set_abilities(self, abilities):
        self.abilities = abilities

    def __str__(self):
        return (f"Character:\nRace: {self.race}\nClass: {self.char_class}\nBackground: {self.background}\n"
                f"Abilities: {', '.join([f'{k}: {v}' for k, v in self.abilities.items()])}")

    def to_dict(self):
        return {
            "race": self.race,
            "class": self.char_class,
            "background": self.background,
            "abilities": self.abilities
        }
