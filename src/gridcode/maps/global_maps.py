"""``gridcode.maps.global_maps``"""

from .map import Map, Value


class GlobalMap(Map):
    """``GlobalMap``"""

    __slots__ = ("_name",)

    def __init__(self, name: str, data: dict[str, Value]):
        super().__init__(data)
        self._name = name

    @property
    def name(self) -> str:
        """``map.name``"""
        return self._name

class GlobalMapStore:
    """``GlobalMapStore``"""

    __slots__ = ("_maps",)

    def __init__(self):
        self._maps: dict[str, GlobalMap] = {}

    def add(self, name: str, data: dict[str, Value]) -> GlobalMap:
        """``grid.globals.add(name, data)``"""
        map = GlobalMap(name, data)
        self._maps[name] = map
        return map

    def get(self, name: str) -> GlobalMap:
        """``grid.globals.get(name)``"""
        return self._maps[name]

    def exists(self, name: str) -> bool:
        """``grid.globals.exists(name)``"""
        return name in self._maps

    def delete(self, name: str) -> None:
        """``grid.globals.delete(name)``"""
        self._maps.pop(name)._mark_deleted()

    def clear(self) -> None:
        """``grid.globals.clear()``"""
        for map in self._maps.values():
            map._mark_deleted()
        self._maps.clear()
