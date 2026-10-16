"""``gridcode.maps.cell_maps``"""

from ..cells import Cell, Offset
from .map import Data, Map, Value


class CellMap(Map):
    """``CellMap``"""

    __slots__ = ()

    @property
    def cell(self) -> Cell:
        """``map.cell``"""
        raise NotImplementedError


class CellMapStore:
    """``CellMapStore``"""

    def add(self, cell: Cell, data: dict[str, Value]) -> CellMap:
        """``grid.maps.add(cell, data)``"""
        raise NotImplementedError

    def copy(self, map: CellMap, cell_or_offset: Cell | Offset) -> CellMap:
        """``grid.maps.copy(map, cell)``

        ``grid.maps.copy(map, offset)``
        """
        raise NotImplementedError

    def select(self, *,
               matches: dict[str, Value] | None = None,
               has: set[str] | None = None,
               at_cells: set[Cell] | None = None) -> set[CellMap]:
        """``grid.maps.select(matches, has, at_cells)``"""
        raise NotImplementedError

    def exists(self, *,
               matches: dict[str, Value] | None = None,
               has: set[str] | None = None,
               at_cells: set[Cell] | None = None) -> bool:
        """``grid.maps.exists(matches, has, at_cells)``"""
        raise NotImplementedError

    def count(self, *,
              matches: dict[str, Value] | None = None,
              has: set[str] | None = None,
              at_cells: set[Cell] | None = None) -> int:
        """``grid.maps.count(matches, has, at_cells)``"""
        raise NotImplementedError

    def select_cells(self, *,
                     matches: dict[str, Value] | None = None,
                     has: set[str] | None = None,
                     at_cells: set[Cell] | None = None) -> set[Cell]:
        """``grid.maps.select_cells(matches, has, at_cells)``"""
        raise NotImplementedError

    def delete(self, map: CellMap) -> None:
        """``grid.maps.delete(map)``"""
        raise NotImplementedError

    def clear(self) -> None:
        """``grid.maps.clear()``"""
        raise NotImplementedError

    def move(self, map: CellMap, cell_or_offset: Cell | Offset) -> None:
        """``grid.maps.move(map, cell)``

        ``grid.maps.move(map, offset)``
        """
        raise NotImplementedError


class CellIndex:
    """``CellIndex``"""

    def insert(self, id: int, cell: Cell) -> None:
        """``cell_index.insert(id, cell)``"""
        raise NotImplementedError

    def remove(self, id: int) -> None:
        """``cell_index.remove(id)``"""
        raise NotImplementedError

    def ids_at(self, cell: Cell) -> set[int]:
        """``cell_index.ids_at(cell)``"""
        raise NotImplementedError


class DataIndex:
    """``DataIndex``"""

    def insert(self, id: int, data: Data) -> None:
        """``data_index.insert(id, data)``"""
        raise NotImplementedError

    def remove(self, id: int) -> None:
        """``data_index.remove(id)``"""
        raise NotImplementedError

    def ids_with_key(self, key: str) -> set[int]:
        """``data_index.ids_with_key(key)``"""
        raise NotImplementedError

    def ids_with_data(self, data: Data) -> set[int]:
        """``data_index.ids_with_data(data)``"""
        raise NotImplementedError

