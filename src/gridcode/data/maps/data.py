"""``gridcode.data.maps.data``"""

from ...grid import GridStore
from .cell_maps import CellMapStore
from .global_maps import GlobalMapStore


class MapsData:
    """``MapsData``"""

    __slots__ = ("store", "maps", "globals")

    def __init__(self, store: GridStore[int]):
        self.store = store
        self.maps = CellMapStore()
        self.globals = GlobalMapStore()
