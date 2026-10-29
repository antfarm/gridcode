"""``gridcode.runtime.program``"""

from collections.abc import Callable

from ..cells import Cell
from ..data import Fields
from .color import Color
from .grid import Grid


CALLBACKS = ("setup", "update", "color", "on_click", "on_key")


class Program:
    """``Program(title, size, frame_rate, index)``"""

    __slots__ = ("title", "size", "frame_rate", "index",
                 "_setup", "_update", "_color", "_on_click", "_on_key")

    def __init__(self, title: str, *,
                 size: int,
                 frame_rate: float,
                 index: list[str] | Fields | None = None):
        self.title = title
        self.size = size
        self.frame_rate = frame_rate
        self.index = index

        for name in CALLBACKS:
            setattr(self, f"_{name}", None)

    # Decorators

    def setup(self, function: Callable[[Grid], None]) -> Callable[[Grid], None]:
        """``@program.setup``"""
        self._setup = function
        return function

    def update(self, function: Callable[[Grid], None]) -> Callable[[Grid], None]:
        """``@program.update``"""
        self._update = function
        return function

    def color(self, function: Callable[[Grid, Cell], Color]) -> Callable[[Grid, Cell], Color]:
        """``@program.color``"""
        self._color = function
        return function

    def on_click(self, function: Callable[[Grid, Cell], None]) -> Callable[[Grid, Cell], None]:
        """``@program.on_click``"""
        self._on_click = function
        return function

    def on_key(self, function: Callable[[Grid, str], None]) -> Callable[[Grid, str], None]:
        """``@program.on_key``"""
        self._on_key = function
        return function

    def check_complete(self) -> None:
        """``program.check_complete()``"""
        missing = [name for name in CALLBACKS if getattr(self, f"_{name}") is None]
        if missing:
            raise TypeError(f"{self.title} is missing {', '.join(missing)}")
