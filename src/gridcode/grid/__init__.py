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
from .maps import Data, Map, Maps

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
    "Data",
    "Map",
    "Maps",
    # grid
    "Grid",
]


class Grid(Cells, Maps):
    """``Grid``"""

    def __init__(self, size: int):
        Cells.__init__(self, size)
        Maps.__init__(self)
