"""``gridcode.grid.maps``"""

from .cells import Cell, Offset

type Value = bool | int | float | str | Cell | Offset
"""``Value``"""


class Data:
    """``Data(key=value)``"""

    __slots__ = ("items",)

    def __init__(self, **values: Value):
        for key, value in values.items():
            check_value(key, value)
        self.items = tuple(values.items())

    def __eq__(self, other) -> bool:
        return isinstance(other, Data) and self.items == other.items

    def __hash__(self) -> int:
        return hash(self.items)

    def __repr__(self) -> str:
        inside = ", ".join(f"{key}={value!r}" for key, value in self.items)
        return f"Data({inside})"


def check_value(key: str, value) -> None:
    """``check_value(key, value)``"""
    allowed = (bool, int, float, str, Cell, Offset)
    if not isinstance(value, allowed):
        raise TypeError(f"{key}: {type(value).__name__} is not a GridCode value")


class Map:
    """``Map``"""

    __slots__ = ("_id",)

    def __init__(self, id: int):
        self._id = id

    def __getitem__(self, key: str) -> Value:
        """``map[key]``"""
        raise NotImplementedError

    def __setitem__(self, key: str, value: Value) -> None:
        """``map[key] = value``"""
        self.set({key: value})

    def get(self, key: str, *more_keys: str) -> tuple[Value, ...]:
        """``map.get(key, key, ...)``"""
        return tuple(self[each_key] for each_key in (key, *more_keys))

    def set(self, data: dict[str, Value]) -> None:
        """``map.set(data)``"""
        raise NotImplementedError

    def delete(self, key: str, *more_keys: str) -> None:
        """``map.delete(key, key, ...)``"""
        raise NotImplementedError

    def has(self, key: str, *more_keys: str) -> bool:
        """``map.has(key, key, ...)``"""
        raise NotImplementedError

    def matches(self, data: dict[str, Value]) -> bool:
        """``map.matches(data)``"""
        raise NotImplementedError

    def __eq__(self, other) -> bool:
        return isinstance(other, Map) and self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

    def __repr__(self) -> str:
        return f"<map {self._id}>"


class CellMap(Map):
    """``CellMap``"""

    __slots__ = ()

    @property
    def cell(self) -> Cell:
        """``map.cell``"""
        raise NotImplementedError


class GlobalMap(Map):
    """``GlobalMap``"""

    __slots__ = ()

    @property
    def name(self) -> str:
        """``map.name``"""
        raise NotImplementedError


class CellMaps:
    """``CellMaps``"""

    def add(self, cell: Cell, data: dict[str, Value]) -> CellMap:
        """``grid.maps.add(cell, data)``"""
        raise NotImplementedError

    def copy(self, map: CellMap, target: Cell) -> CellMap:
        """``grid.maps.copy(map, cell)``"""
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

    def move(self, map: CellMap, target: Cell | Offset) -> None:
        """``grid.maps.move(map, cell)``

        ``grid.maps.move(map, offset)``
        """
        raise NotImplementedError


class GlobalMaps:
    """``GlobalMaps``"""

    def add(self, name: str, data: dict[str, Value]) -> GlobalMap:
        """``grid.globals.add(name, data)``"""
        raise NotImplementedError

    def get(self, name: str) -> GlobalMap | None:
        """``grid.globals.get(name)``"""
        raise NotImplementedError

    def exists(self, name: str) -> bool:
        """``grid.globals.exists(name)``"""
        raise NotImplementedError

    def delete(self, name: str) -> None:
        """``grid.globals.delete(name)``"""
        raise NotImplementedError

    def clear(self) -> None:
        """``grid.globals.clear()``"""
        raise NotImplementedError
