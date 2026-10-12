"""``gridcode.grid``"""

from .cells import (
    DOWN,
    HORIZONTAL,
    LEFT,
    MOORE,
    RIGHT,
    UP,
    VERTICAL,
    VON_NEUMANN,
    Cell,
    Cells,
    Neighborhood,
    Offset,
)
from .maps import CellMap, CellMapStore, Data, GlobalMap, GlobalMapStore, Map

__all__ = [
    # cells
    "DOWN",
    "LEFT",
    "RIGHT",
    "UP",
    "Cell",
    "Cells",
    "Neighborhood",
    "MOORE",
    "VON_NEUMANN",
    "HORIZONTAL",
    "VERTICAL",
    "Offset",
    # maps
    "Data",
    "Map",
    "CellMap",
    "CellMapStore",
    "GlobalMap",
    "GlobalMapStore",
    # grid
    "Grid",
]


class Grid:
    """``Grid``"""

    def __init__(self, size: int):
        self.cells = Cells(size)
        self.maps = CellMapStore()
        self.globals = GlobalMapStore()
