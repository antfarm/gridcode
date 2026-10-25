"""``gridcode.data.data``"""

from ..cells import Cell, CellGrid, CellStore, Offset
from .index import Index
from .map import Map, Value, check_deleted


class CellMap(Map):
    """``CellMap``"""

    __slots__ = ("_store",)

    def __init__(self, store: DataStore, data: dict[str, Value]):
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


class DataStore:
    """``DataStore``"""

    __slots__ = ("globals", "_grid", "_cell_store", "_map_locations", "_index")

    def __init__(self, grid: CellGrid, index: list[str] | Index.Fields | None = None):
        self.globals = Map({})
        self._grid = grid
        self._cell_store = CellStore[set[CellMap]](grid)
        self._map_locations: dict[CellMap, Cell] = {}
        self._index = Index(index) if index else None

    # Lifecycle

    def add(self, cell: Cell, data: dict[str, Value]) -> CellMap:
        """``grid.data.add(cell, data)``"""
        map = CellMap(self, data)
        self._place(cell, map)
        if self._has_index:
            self._index.add_map(map)
        return map

    def copy(self, map: CellMap, cell_or_offset: Cell | Offset) -> CellMap:
        """``grid.data.copy(map, cell)``

        ``grid.data.copy(map, offset)``
        """
        target_cell = (map.cell + cell_or_offset if isinstance(cell_or_offset, Offset)
                       else cell_or_offset)
        return self.add(target_cell, dict(map._data))

    def delete(self, map: CellMap) -> None:
        """``grid.data.delete(map)``"""
        self._remove(map)
        if self._has_index:
            self._index.remove_map(map)
        map._deleted = True

    def clear_cells(self) -> None:
        """``grid.data.clear_cells()``"""
        for map in self._map_locations:
            map._deleted = True
        self._cell_store.clear()
        self._map_locations.clear()
        if self._has_index:
            self._index.clear()

    def clear_globals(self) -> None:
        """``grid.data.clear_globals()``"""
        self.globals._data.clear()

    def clear(self) -> None:
        """``grid.data.clear()``"""
        self.clear_cells()
        self.clear_globals()

    # Movement

    def move(self, map: CellMap, cell_or_offset: Cell | Offset) -> None:
        """``grid.data.move(map, cell)``

        ``grid.data.move(map, offset)``
        """
        target_cell = (map.cell + cell_or_offset if isinstance(cell_or_offset, Offset)
                       else cell_or_offset)
        if not self._grid.contains(target_cell):
            raise IndexError(f"{target_cell} is outside the grid")

        if target_cell != map.cell:
            self._remove(map)
            self._place(target_cell, map)

    # Location

    def cell_of(self, map: CellMap) -> Cell:
        """``grid.data.cell_of(map)``"""
        cell = self._map_locations.get(map)
        if cell is None:
            raise KeyError(f"{map!r} is not in the grid")
        return cell

    # Querying

    def select(self, *,
               matches: dict[str, Value] | None = None,
               has: set[str] | None = None,
               at_cells: set[Cell] | None = None) -> set[CellMap]:
        """``grid.data.select(matches, has, at_cells)``"""
        if not self._has_index:
            candidate_sets, rest_matches, rest_has = [], matches or {}, has or set()
        else:
            candidate_sets, rest_matches, rest_has = self._index.sets_for(matches, has)
        if at_cells is not None:
            maps_at_cells = set()
            for cell in at_cells:
                maps_at_cells |= self._cell_store.item_at(cell) or set()
            candidate_sets.append(maps_at_cells)
        if not candidate_sets:
            candidate_sets.append(self._all_maps())

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
        """``grid.data.exists(matches, has, at_cells)``"""
        return bool(self.select(matches=matches, has=has, at_cells=at_cells))

    def count(self, *,
              matches: dict[str, Value] | None = None,
              has: set[str] | None = None,
              at_cells: set[Cell] | None = None) -> int:
        """``grid.data.count(matches, has, at_cells)``"""
        return len(self.select(matches=matches, has=has, at_cells=at_cells))

    def select_cells(self, *,
                     matches: dict[str, Value] | None = None,
                     has: set[str] | None = None,
                     at_cells: set[Cell] | None = None) -> set[Cell]:
        """``grid.data.select_cells(matches, has, at_cells)``"""
        return {map.cell
                for map in self.select(matches=matches, has=has, at_cells=at_cells)}

    # Internal

    @property
    def _has_index(self) -> bool:
        return self._index is not None

    def _reindexing(self, map: CellMap):
        return self._index.reindexing(map)

    def _all_maps(self) -> set[CellMap]:
        return set(self._map_locations)

    def _maps_at(self, cell: Cell) -> set[CellMap]:
        maps = self._cell_store.item_at(cell)
        if maps is None:
            maps = set()
            self._cell_store.set(cell, maps)
        return maps

    def _place(self, cell: Cell, map: CellMap) -> None:
        self._maps_at(cell).add(map)
        self._map_locations[map] = cell

    def _remove(self, map: CellMap) -> None:
        cell = self.cell_of(map)
        maps = self._cell_store.item_at(cell)
        maps.discard(map)
        if not maps:
            self._cell_store.delete(cell)
        del self._map_locations[map]
