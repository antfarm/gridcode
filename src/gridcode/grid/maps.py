"""``gridcode.grid.maps``"""

from .cells import Cell, Offset

type Value = bool | int | float | str | Cell | Offset
"""``Value``"""


class AnyValue:
    """``AnyValue``"""

    def __repr__(self) -> str:
        return "ANY"


ANY = AnyValue()
"""``ANY``"""

type Match = Value | AnyValue
"""``Match``"""


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

    def get(self, key: str):
        """``map.get(key)``"""
        raise NotImplementedError

    def set(self, data: dict[str, Value]) -> None:
        """``map.set({key: value})``"""
        raise NotImplementedError

    def delete(self, key: str) -> None:
        """``map.delete(key)``"""
        raise NotImplementedError

    def __getitem__(self, key: str):
        """``map[key]``"""
        return self.get(key)

    def __setitem__(self, key: str, value) -> None:
        """``map[key] = value``"""
        self.set({key: value})

    def has(self, data: dict[str, Match]) -> bool:
        """``map.has(data)``"""
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

    def add(self, cell: Cell, data: Data) -> CellMap:
        """``grid.maps.add(cell, Data(key=value))``"""
        raise NotImplementedError

    def get(self,
            data: dict[str, Match] | None = None,
            at_cells: list[Cell] | None = None) -> set[CellMap]:
        """``grid.maps.get(data, at_cells)``"""
        raise NotImplementedError

    def has(self,
            data: dict[str, Match] | None = None,
            at_cells: list[Cell] | None = None) -> bool:
        """``grid.maps.has(data, at_cells)``"""
        raise NotImplementedError

    def count(self,
              data: dict[str, Match] | None = None,
              at_cells: list[Cell] | None = None) -> int:
        """``grid.maps.count(data, at_cells)``"""
        # to be discussed
        raise NotImplementedError

    def cells_of(self,
                 data: dict[str, Match] | None = None,
                 at_cells: list[Cell] | None = None) -> set[Cell]:
        """``grid.maps.cells_of(data, at_cells)``"""
        # to be discussed
        raise NotImplementedError

    def delete(self, maps: CellMap | set[CellMap]) -> None:
        """``grid.maps.delete(map)``

        ``grid.maps.delete(maps)``
        """
        raise NotImplementedError

    def clear(self) -> None:
        """``grid.maps.clear()``"""
        raise NotImplementedError

    def move(self, map: CellMap, target: Cell | Offset) -> None:
        """``grid.maps.move(map, cell)``

        ``grid.maps.move(map, offset)``
        """
        raise NotImplementedError

    def copy(self, map: CellMap, target: Cell | Offset) -> CellMap:
        """``grid.maps.copy(map, cell)``

        ``grid.maps.copy(map, offset)``
        """
        raise NotImplementedError


class GlobalMaps:
    """``GlobalMaps``"""

    def add(self, name: str, data: Data) -> GlobalMap:
        """``grid.globals.add(name, Data(key=value))``"""
        raise NotImplementedError

    def get(self, name: str) -> GlobalMap | None:
        """``grid.globals.get(name)``"""
        raise NotImplementedError

    def has(self, name: str) -> bool:
        """``grid.globals.has(name)``"""
        raise NotImplementedError

    def delete(self, name: str) -> None:
        """``grid.globals.delete(name)``"""
        raise NotImplementedError

    def clear(self) -> None:
        """``grid.globals.clear()``"""
        raise NotImplementedError
