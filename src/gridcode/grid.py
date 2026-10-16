"""``gridcode.grid``"""

from .cells import Cells
from .maps import CellMapStore, GlobalMapStore


class Grid:
    """``Grid``"""

    def __init__(self, size: int):
        self.cells = Cells(size)
        self.maps = CellMapStore()
        self.globals = GlobalMapStore()
