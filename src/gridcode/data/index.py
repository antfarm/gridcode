"""``gridcode.data.index``"""

from contextlib import contextmanager
from enum import StrEnum

from .map import Map, Value


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
        self.maps_by_key: dict[str, set[Map]] = {}
        self.maps_by_data: dict[tuple[str, Value], set[Map]] = {}

    def is_indexed(self, key: str) -> bool:
        """``index.is_indexed(key)``"""
        return self.indexed_keys is Index.Fields.ALL or key in self.indexed_keys

    @contextmanager
    def reindexing(self, map: Map):
        """``with index.reindexing(map): ...``"""
        self.remove_map(map)
        try:
            yield
        finally:
            self.add_map(map)

    def sets_for(self, matches: dict[str, Value] | None,
                 has: set[str] | None) -> tuple[list[set[Map]],
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

    def add_map(self, map: Map) -> None:
        """``index.add_map(map)``"""
        for key, value in map._data.items():
            if self.is_indexed(key):
                self._add(map, key, value)

    def remove_map(self, map: Map) -> None:
        """``index.remove_map(map)``"""
        for key, value in map._data.items():
            if self.is_indexed(key):
                self._remove(map, key, value)

    def maps_with_key(self, key: str) -> set[Map]:
        """``index.maps_with_key(key)``"""
        return set(self.maps_by_key.get(key, ()))

    def maps_with_data(self, key: str, value: Value) -> set[Map]:
        """``index.maps_with_data(key, value)``"""
        return set(self.maps_by_data.get((key, value), ()))

    def clear(self) -> None:
        """``index.clear()``"""
        self.maps_by_key.clear()
        self.maps_by_data.clear()

    def _add(self, map: Map, key: str, value: Value) -> None:
        self.maps_by_key.setdefault(key, set()).add(map)
        self.maps_by_data.setdefault((key, value), set()).add(map)

    def _remove(self, map: Map, key: str, value: Value) -> None:
        self._discard(self.maps_by_key, key, map)
        self._discard(self.maps_by_data, (key, value), map)

    def _discard(self, index: dict, index_key, map: Map) -> None:
        maps = index.get(index_key)
        if maps is None:
            return
        maps.discard(map)
        if not maps:
            del index[index_key]
