"""``gridcode.grid``"""

from .cells import Cell, Cells, Neighborhood, Offset
from .maps import CellMap, CellMapStore, Data, GlobalMap, GlobalMapStore, Map

__all__ = [
    # cells
    "Cell",
    "Cells",
    "Neighborhood",
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
