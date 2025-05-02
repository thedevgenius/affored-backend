import random

def generate_random_color():
    """Generate and return a random hex color code."""
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))