"""``gridcode.runtime.grid``"""

from ..cells import CellGrid
from ..data import DataStore, Fields


class Grid:
    """``Grid``"""

    __slots__ = ("cells", "data")

    def __init__(self, size: int, index: list[str] | Fields | None = None):
        self.cells = CellGrid(size)
        self.data = DataStore(self.cells, index)
