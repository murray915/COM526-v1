import random

directions = ["north", "east", "south", "west"]
random.shuffle(directions)

decision = f"random_{directions[0]}"


print(decision)