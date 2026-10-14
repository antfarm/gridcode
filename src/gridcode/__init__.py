"""``gridcode``"""

from .display import Color
from .grid import Cell, Grid, Neighborhood, Offset
from .gridcode import run
from .program import Program

UP = Offset.UP
DOWN = Offset.DOWN
LEFT = Offset.LEFT
RIGHT = Offset.RIGHT

MOORE = Neighborhood.MOORE
VON_NEUMANN = Neighborhood.VON_NEUMANN
HORIZONTAL = Neighborhood.HORIZONTAL
VERTICAL = Neighborhood.VERTICAL

__all__ = [
    "run",
    "Program",
    "Color",
    "Grid",
    "Cell",
    "Offset",
    "UP",
    "DOWN",
    "LEFT",
    "RIGHT",
    "MOORE",
    "VON_NEUMANN",
    "HORIZONTAL",
    "VERTICAL",
]
