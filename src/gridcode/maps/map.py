"""``gridcode.maps.map``"""

import functools

from ..cells import Cell, Offset

type Value = bool | int | float | str | Cell | Offset
"""``Value``"""


def check_deleted(method):
    """``@check_deleted``"""
    @functools.wraps(method)
    def guarded(self, *args, **kwargs):
        if self._deleted:
            raise ValueError(f"{self!r} was deleted")
        return method(self, *args, **kwargs)
    return guarded


class Map:
    """``Map``"""

    __slots__ = ("_data", "_deleted")

    def __init__(self, data: dict[str, Value]):
        for key, value in data.items():
            _check_value_type(key, value)
        self._data = dict(data)
        self._deleted = False

    @check_deleted
    def __getitem__(self, key: str) -> Value:
        """``map[key]``"""
        return self._data[key]

    @check_deleted
    def __setitem__(self, key: str, value: Value) -> None:
        """``map[key] = value``"""
        self.set({key: value})

    @check_deleted
    def get(self, key1: str, key2: str, *more_keys: str) -> tuple[Value, ...]:
        """``map.get(key, key, ...)``"""
        return tuple(self[key] for key in (key1, key2, *more_keys))

    @check_deleted
    def set(self, data: dict[str, Value]) -> None:
        """``map.set(data)``"""
        for key, value in data.items():
            _check_value_type(key, value)
        self._data.update(data)

    @check_deleted
    def delete(self, key: str, *more_keys: str) -> None:
        """``map.delete(key, key, ...)``"""
        for deleted_key in (key, *more_keys):
            del self._data[deleted_key]

    @check_deleted
    def has(self, key: str, *more_keys: str) -> bool:
        """``map.has(key, key, ...)``"""
        return all(key in self._data for key in (key, *more_keys))

    @check_deleted
    def matches(self, data: dict[str, Value]) -> bool:
        """``map.matches(data)``"""
        return all(self._data.get(key) == value for key, value in data.items())

    def __repr__(self) -> str:
        inside = ", ".join(f"{key}={value!r}" for key, value in self._data.items())
        return f"<map {inside}>"


def _check_value_type(key: str, value) -> None:
    allowed = (bool, int, float, str, Cell, Offset)
    if not isinstance(value, allowed):
        raise TypeError(f"{key}: {type(value).__name__} is not a GridCode value")
