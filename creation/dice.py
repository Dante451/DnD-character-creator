import random

def roll_dice(sides):
    """Roll a die with the given number of sides."""
    return random.randint(1, sides)

def roll_ability():
    """Roll 4d6 and drop the lowest roll, standard for abilities."""
    rolls = [roll_dice(6) for _ in range(4)]
    rolls.sort()
    return sum(rolls[1:])  # drop the lowest die
