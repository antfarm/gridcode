"""``gridcode.data.maps.global_maps``"""

from .map import Map, Value


class GlobalMap(Map):
    """``GlobalMap``"""

    __slots__ = ()

    @property
    def name(self) -> str:
        """``map.name``"""
        raise NotImplementedError

class GlobalMapStore:
    """``GlobalMapStore``"""

    def add(self, name: str, data: dict[str, Value]) -> GlobalMap:
        """``grid.globals.add(name, data)``"""
        raise NotImplementedError

    def get(self, name: str) -> GlobalMap:
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
