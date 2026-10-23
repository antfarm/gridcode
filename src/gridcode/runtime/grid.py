"""``gridcode.runtime.grid``"""

from ..cells import CellGrid
from ..data import CellMapStore, Fields, GlobalMapStore


class Grid:
    """``Grid``"""

    def __init__(self, size: int, index: list[str] | Fields | None = None):
        self.cells = CellGrid(size)
        self.maps = CellMapStore(self.cells, index)
        self.globals = GlobalMapStore()
