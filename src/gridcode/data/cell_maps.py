"""``gridcode.data.cell_maps``"""

from contextlib import contextmanager
from enum import StrEnum

from ..cells import Cell, CellGrid, CellStore, Offset
from .map import Map, Value, check_deleted


class CellMap(Map):
    """``CellMap``"""

    __slots__ = ("_store",)

    def __init__(self, store: CellMapStore, data: dict[str, Value]):
        super().__init__(data)
        self._store = store

    @property
    @check_deleted
    def cell(self) -> Cell:
        """``map.cell``"""
        return self._store.cell_of(self)

    @check_deleted
    def set(self, data: dict[str, Value]) -> None:
        """``map.set(data)``"""
        if not self._store._has_index:
            super().set(data)
        else:
            with self._store._reindexing(self):
                super().set(data)

    @check_deleted
    def delete(self, key: str, *more_keys: str) -> None:
        """``map.delete(key, key, ...)``"""
        if not self._store._has_index:
            super().delete(key, *more_keys)
        else:
            with self._store._reindexing(self):
                super().delete(key, *more_keys)


class CellMapStore:
    """``CellMapStore``"""

    __slots__ = ("_cell_store", "_index")

    def __init__(self, grid: CellGrid, index: list[str] | Index.Fields | None = None):
        self._cell_store = CellStore[CellMap](grid)
        self._index = Index(index) if index else None

    def add(self, cell: Cell, data: dict[str, Value]) -> CellMap:
        """``grid.maps.add(cell, data)``"""
        map = CellMap(self, data)
        self._cell_store.add(cell, map)
        if self._has_index:
            self._index.add_map(map)
        return map

    def copy(self, map: CellMap, cell_or_offset: Cell | Offset) -> CellMap:
        """``grid.maps.copy(map, cell)``

        ``grid.maps.copy(map, offset)``
        """
        target_cell = (map.cell + cell_or_offset if isinstance(cell_or_offset, Offset)
                       else cell_or_offset)
        return self.add(target_cell, dict(map._data))

    def delete(self, map: CellMap) -> None:
        """``grid.maps.delete(map)``"""
        self._cell_store.delete(map)
        if self._has_index:
            self._index.remove_map(map)
        map._deleted = True

    def clear(self) -> None:
        """``grid.maps.clear()``"""
        for map in self._cell_store.cells_by_item:
            map._deleted = True
        self._cell_store.clear()
        if self._has_index:
            self._index.clear()

    def move(self, map: CellMap, cell_or_offset: Cell | Offset) -> None:
        """``grid.maps.move(map, cell)``

        ``grid.maps.move(map, offset)``
        """
        target_cell = (map.cell + cell_or_offset if isinstance(cell_or_offset, Offset)
                       else cell_or_offset)
        self._cell_store.move(map, target_cell)

    def cell_of(self, map: CellMap) -> Cell:
        """``grid.maps.cell_of(map)``"""
        return self._cell_store.cell_of(map)

    def select(self, *,
               matches: dict[str, Value] | None = None,
               has: set[str] | None = None,
               at_cells: set[Cell] | None = None) -> set[CellMap]:
        """``grid.maps.select(matches, has, at_cells)``"""
        if not self._has_index:
            candidate_sets, rest_matches, rest_has = [], matches or {}, has or set()
        else:
            candidate_sets, rest_matches, rest_has = self._index.sets_for(matches, has)
        if at_cells is not None:
            maps_at_cells = set()
            for cell in at_cells:
                maps_at_cells |= self._cell_store.items_at(cell)
            candidate_sets.append(maps_at_cells)
        if not candidate_sets:
            candidate_sets.append(set(self._cell_store.cells_by_item))

        maps = (candidate_sets[0] if len(candidate_sets) == 1
                else set.intersection(*candidate_sets))
        if not rest_matches and not rest_has:
            return maps
        return {map for map in maps
                if (not rest_matches or map.matches(rest_matches))
                and (not rest_has or map.has(*rest_has))}

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

    @property
    def _has_index(self) -> bool:
                return self._index is not None

    def _reindexing(self, map: CellMap):
        return self._index.reindexing(map)


class Index:
    """``Index``"""

    class Fields(StrEnum):
        """``Index.Fields``"""

        ALL = "all"
        """``Index.Fields.ALL``"""

    __slots__ = ("indexed_keys", "maps_by_key", "maps_by_data")

    def __init__(self, index: list[str] | Fields):
        self.indexed_keys = (Index.Fields.ALL if index is Index.Fields.ALL
                             else frozenset(index))
        self.maps_by_key: dict[str, set[CellMap]] = {}
        self.maps_by_data: dict[tuple[str, Value], set[CellMap]] = {}

    def is_indexed(self, key: str) -> bool:
        """``index.is_indexed(key)``"""
        return self.indexed_keys is Index.Fields.ALL or key in self.indexed_keys

    @contextmanager
    def reindexing(self, map: CellMap):
        """``with index.reindexing(map): ...``"""
        self.remove_map(map)
        try:
            yield
        finally:
            self.add_map(map)

    def sets_for(self, matches: dict[str, Value] | None,
                 has: set[str] | None) -> tuple[list[set[CellMap]],
                                                dict[str, Value],
                                                set[str]]:
        """``index.sets_for(matches, has)``"""
        sets = []
        rest_matches = {}
        rest_has = set()

        for key, value in (matches or {}).items():
            if self.is_indexed(key):
                sets.append(self.maps_with_data(key, value))
            else:
                rest_matches[key] = value

        for key in has or ():
            if self.is_indexed(key):
                sets.append(self.maps_with_key(key))
            else:
                rest_has.add(key)

        return sets, rest_matches, rest_has

    def add_map(self, map: CellMap) -> None:
        """``index.add_map(map)``"""
        for key, value in map._data.items():
            if self.is_indexed(key):
                self._add(map, key, value)

    def remove_map(self, map: CellMap) -> None:
        """``index.remove_map(map)``"""
        for key, value in map._data.items():
            if self.is_indexed(key):
                self._remove(map, key, value)

    def maps_with_key(self, key: str) -> set[CellMap]:
        """``index.maps_with_key(key)``"""
        return set(self.maps_by_key.get(key, ()))

    def maps_with_data(self, key: str, value: Value) -> set[CellMap]:
        """``index.maps_with_data(key, value)``"""
        return set(self.maps_by_data.get((key, value), ()))

    def clear(self) -> None:
        """``index.clear()``"""
        self.maps_by_key.clear()
        self.maps_by_data.clear()

    def _add(self, map: CellMap, key: str, value: Value) -> None:
        self.maps_by_key.setdefault(key, set()).add(map)
        self.maps_by_data.setdefault((key, value), set()).add(map)

    def _remove(self, map: CellMap, key: str, value: Value) -> None:
        self._discard(self.maps_by_key, key, map)
        self._discard(self.maps_by_data, (key, value), map)

    def _discard(self, index: dict, index_key, map: CellMap) -> None:
        maps = index.get(index_key)
        if maps is None:
            return
        maps.discard(map)
        if not maps:
            del index[index_key]

