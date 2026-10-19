"""``gridcode.runtime.grid``"""

from ..cells import CellGrid
from ..maps import CellMapStore, GlobalMapStore


class Grid:
    """``Grid``"""

    def __init__(self, size: int):
        self.cells = CellGrid(size)
        self.maps = CellMapStore(self.cells)
        self.globals = GlobalMapStore()