"""``gridcode``"""

from .cells import Cell, Neighborhood, Offset
from .gridcode import run
from .maps import Fields
from .runtime import Color, Grid, Program

ALL = Fields.ALL

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
    "ALL",
    "UP",
    "DOWN",
    "LEFT",
    "RIGHT",
    "MOORE",
    "VON_NEUMANN",
    "HORIZONTAL",
    "VERTICAL",
]
