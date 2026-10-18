"""``gridcode.data.maps.map``"""

from ...cells import Cell, Offset

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

    def get(self, key1: str, key2: str, *more_keys: str) -> tuple[Value, ...]:
        """``map.get(key, key, ...)``"""
        return tuple(self[key] for key in (key1, key2, *more_keys))

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
