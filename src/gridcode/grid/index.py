"""``gridcode.grid.index``"""

from .cells import Cell
from .maps import Data


class Index:
    """``Index``"""

    def insert(self, id: int, where: Cell | str, data: Data) -> None:
        """``index.insert(id, where, data)``"""
        raise NotImplementedError

    def remove(self, id: int) -> None:
        """``index.remove(id)``"""
        raise NotImplementedError

    def ids_with_key(self, key: str) -> set[int]:
        """``index.ids_with_key(key)``"""
        raise NotImplementedError

    def ids_with_data(self, data: Data) -> set[int]:
        """``index.ids_with_data(data)``"""
        raise NotImplementedError

    def ids_at(self, cell: Cell) -> set[int]:
        """``index.ids_at(cell)``"""
        raise NotImplementedError

    def ids_named(self, name: str) -> set[int]:
        """``index.ids_named(name)``"""
        raise NotImplementedError
