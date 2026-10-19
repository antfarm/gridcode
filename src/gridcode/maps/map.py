"""``gridcode.maps.map``"""

from ..cells import Cell, Offset

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

    __slots__ = ("_data", "_deleted")

    def __init__(self, data: dict[str, Value]):
        for key, value in data.items():
            check_value(key, value)
        self._data = dict(data)
        self._deleted = False

    def __getitem__(self, key: str) -> Value:
        """``map[key]``"""
        self._check_deleted()
        return self._data[key]

    def __setitem__(self, key: str, value: Value) -> None:
        """``map[key] = value``"""
        self._check_deleted()
        self.set({key: value})

    def get(self, key1: str, key2: str, *more_keys: str) -> tuple[Value, ...]:
        """``map.get(key, key, ...)``"""
        self._check_deleted()
        return tuple(self[key] for key in (key1, key2, *more_keys))

    def set(self, data: dict[str, Value]) -> None:
        """``map.set(data)``"""
        self._check_deleted()
        for key, value in data.items():
            check_value(key, value)
        self._data.update(data)

    def delete(self, key: str, *more_keys: str) -> None:
        """``map.delete(key, key, ...)``"""
        self._check_deleted()
        for deleted_key in (key, *more_keys):
            del self._data[deleted_key]

    def has(self, key: str, *more_keys: str) -> bool:
        """``map.has(key, key, ...)``"""
        self._check_deleted()
        return all(key in self._data for key in (key, *more_keys))

    def matches(self, data: dict[str, Value]) -> bool:
        """``map.matches(data)``"""
        self._check_deleted()
        return all(self._data.get(key) == value for key, value in data.items())

    def _mark_deleted(self) -> None:
        """``map._mark_deleted()``"""
        self._deleted = True

    def _check_deleted(self) -> None:
        """``map._check_deleted()``"""
        if self._deleted:
            raise ValueError(f"{self!r} was deleted")

    def __repr__(self) -> str:
        inside = ", ".join(f"{key}={value!r}" for key, value in self._data.items())
        return f"<map {inside}>"
