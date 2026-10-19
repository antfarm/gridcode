"""``gridcode.maps.cell_maps``"""

from ..cells import Cell, CellGrid, CellStore, Offset
from .map import Data, Map, Value


class CellMap(Map):
    """``CellMap``"""

    __slots__ = ("_store",)

    def __init__(self, store: CellMapStore, data: dict[str, Value]):
        super().__init__(data)
        self._store = store

    @property
    def cell(self) -> Cell:
        """``map.cell``"""
        self._check_deleted()
        return self._store.cell_of(self)

    # TODO: override set, delete and __setitem__ to update the data index


class CellMapStore:
    """``CellMapStore``"""

    __slots__ = ("_cell_store",)

    def __init__(self, grid: CellGrid):
        self._cell_store = CellStore[CellMap](grid)

    def add(self, cell: Cell, data: dict[str, Value]) -> CellMap:
        """``grid.maps.add(cell, data)``"""
        map = CellMap(self, data)
        self._cell_store.add(cell, map)
        # TODO: update the data index
        return map

    def copy(self, map: CellMap, cell_or_offset: Cell | Offset) -> CellMap:
        """``grid.maps.copy(map, cell)``

        ``grid.maps.copy(map, offset)``
        """
        return self.add(self._target_cell(map, cell_or_offset), dict(map._data))

    def cell_of(self, map: CellMap) -> Cell:
        """``grid.maps.cell_of(map)``"""
        return self._cell_store.cell_of(map)

    def select(self, *,
               matches: dict[str, Value] | None = None,
               has: set[str] | None = None,
               at_cells: set[Cell] | None = None) -> set[CellMap]:
        """``grid.maps.select(matches, has, at_cells)``"""
        # TODO: read candidates for matches and has from the data index
        return {map for map in self._maps_at(at_cells)
                if (matches is None or map.matches(matches))
                and (not has or map.has(*has))}

    def exists(self, *,
               matches: dict[str, Value] | None = None,
               has: set[str] | None = None,
               at_cells: set[Cell] | None = None) -> bool:
        """``grid.maps.exists(matches, has, at_cells)``"""
        return bool(self.select(matches=matches, has=has, at_cells=at_cells))

    def count(self, *,
              matches: dict[str, Value] | None = None,
              has: set[str] | None = None,
              at_cells: set[Cell] | None = None) -> int:
        """``grid.maps.count(matches, has, at_cells)``"""
        return len(self.select(matches=matches, has=has, at_cells=at_cells))

    def select_cells(self, *,
                     matches: dict[str, Value] | None = None,
                     has: set[str] | None = None,
                     at_cells: set[Cell] | None = None) -> set[Cell]:
        """``grid.maps.select_cells(matches, has, at_cells)``"""
        return {map.cell
                for map in self.select(matches=matches, has=has, at_cells=at_cells)}

    def delete(self, map: CellMap) -> None:
        """``grid.maps.delete(map)``"""
        self._cell_store.delete(map)
        # TODO: update the data index
        map._mark_deleted()

    def clear(self) -> None:
        """``grid.maps.clear()``"""
        for map in self._cell_store.cells_by_item:
            map._mark_deleted()
        self._cell_store.clear()
        # TODO: clear the data index

    def move(self, map: CellMap, cell_or_offset: Cell | Offset) -> None:
        """``grid.maps.move(map, cell)``

        ``grid.maps.move(map, offset)``
        """
        self._cell_store.move(map, self._target_cell(map, cell_or_offset))

    def _maps_at(self, at_cells: set[Cell] | None) -> set[CellMap]:
        """``grid.maps._maps_at(at_cells)``"""
        if at_cells is None:
            return set(self._cell_store.cells_by_item)
        maps = set()
        for cell in at_cells:
            maps |= self._cell_store.items_at(cell)
        return maps

    def _target_cell(self, map: CellMap, cell_or_offset: Cell | Offset) -> Cell:
        """``grid.maps._target_cell(map, cell_or_offset)``"""
        if isinstance(cell_or_offset, Offset):
            return map.cell + cell_or_offset
        return cell_or_offset


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

