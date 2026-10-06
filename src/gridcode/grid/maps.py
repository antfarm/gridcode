"""``gridcode.grid.maps``"""

from dataclasses import dataclass

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

    __slots__ = ("id",)

    def __init__(self, id: int):
        self.id = id

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

    def has(self, what: dict[str, Value] | str) -> bool:
        """``map.has({key: value})``

        ``map.has(key)``
        """
        raise NotImplementedError

    @property
    def cell(self) -> Cell | None:
        """``map.cell``"""
        raise NotImplementedError

    def __eq__(self, other) -> bool:
        return isinstance(other, Map) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"<map {self.id}>"


@dataclass(frozen=True)
class HasData:
    """``HasData``"""

    data: Data


@dataclass(frozen=True)
class HasKey:
    """``HasKey``"""

    key: str


@dataclass(frozen=True)
class At:
    """``At``"""

    cells: tuple


type Criterion = HasData | HasKey | At


def has(what: dict[str, Value] | str) -> HasData | HasKey:
    """``has({key: value})``

    ``has(key)``
    """
    if isinstance(what, str):
        return HasKey(what)
    return HasData(Data(**what))


def at(where) -> At:
    """``at(cell)``

    ``at(cells)``
    """
    if isinstance(where, Cell):
        return At((where,))
    return At(tuple(where))


class Maps:
    """``Maps``"""

    def add(self, where: Cell | str, data: Data) -> Map:
        """``grid.add(cell, Data(key=value))``

        ``grid.add(name, Data(key=value))``
        """
        raise NotImplementedError

    def get(self, name: str) -> Map | None:
        """``grid.get(name)``"""
        raise NotImplementedError

    def select(self, *criteria: Criterion) -> set[Map]:
        """``grid.select(criteria)``"""
        raise NotImplementedError

    def exists(self, *criteria: Criterion) -> bool:
        """``grid.exists(criteria)``"""
        raise NotImplementedError

    def delete(self, maps: Map | set[Map]) -> None:
        """``grid.delete(map)``

        ``grid.delete(maps)``
        """
        raise NotImplementedError

    def clear(self) -> None:
        """``grid.clear()``"""
        self.delete(self.select())

    def move(self, map: Map, target: Cell | Offset) -> None:
        """``grid.move(map, cell)``

        ``grid.move(map, offset)``
        """
        raise NotImplementedError

    def copy(self, map: Map, target: Cell) -> Map:
        """``grid.copy(map, cell)``"""
        raise NotImplementedError
