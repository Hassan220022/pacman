#!/usr/bin/python3
from OpenGL import GL as gl

# Define constant colors using RGB values
COIN_COLOR = 0.9, 0.9, 0        # Light yellow color for a coin

SUPER_COIN_COLOR = 0.9, 0.3, 0  # Bright orange color for a super coin

FLOOR_COLOR = 0.15, 0.15, 0.15  # Dark gray color for the floor

CELING_COLOR = 0.1, 0.4, 0.9    # Light blue color for the ceiling

# Define constant levels for the ceiling and floor heights
CELLING_LEVEL = 0               # Height level for the ceiling
FLOOR_LEVEL = -1.0              # Height level for the floor

# Define movement directions
MOVES = "NSWE"                  # String representing the directions: North, South, West, East

# Define a dictionary to map each direction to its opposite
OPPOSITE_MOVES = {
    "N": "S",                   # North is opposite to South
    "S": "N",                   # South is opposite to North
    "W": "E",                   # West is opposite to East
    "E": "W"                    # East is opposite to West
}


def set_color(color):
    """Function sets the color."""
    r, g, b = color
    gl.glColor3f(r, g, b)