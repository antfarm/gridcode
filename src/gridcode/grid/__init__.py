"""``gridcode.grid``"""

from .cells import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Cell,
    Cells,
    Neighborhood,
    Offset,
)
from .maps import ANY, Data, Map, Maps

__all__ = [
    # cells
    "DOWN",
    "LEFT",
    "RIGHT",
    "UP",
    "Cell",
    "Cells",
    "Neighborhood",
    "Offset",
    # maps
    "ANY",
    "Data",
    "Map",
    "Maps",
    # grid
    "Grid",
]


class Grid:
    """``Grid``"""

    def __init__(self, size: int):
        self.cells = Cells(size)
        self.maps = Maps()
