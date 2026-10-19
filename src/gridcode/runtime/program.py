"""``gridcode.runtime.program``"""

import inspect
from abc import ABC, abstractmethod
from annotationlib import Format

from ..cells import Cell
from .grid import Grid
from .color import Color


class Program(ABC):
    """``Program``"""

    size: int
    frame_rate: float

    def __init_subclass__(cls, size: int = 16, frame_rate: float = 8, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.size = size
        cls.frame_rate = frame_rate

        for name in ("setup", "update", "color_for_cell", "on_cell_click", "on_key_press"):
            function = cls.__dict__.get(name)
            if function is None:
                continue
            if not isinstance(function, staticmethod):
                raise TypeError(f"{cls.__name__}.{name} must be a @staticmethod")

            if inspect.signature(function.__func__) != inspect.signature(getattr(Program, name)):
                subclass_signature = inspect.signature(
                    function.__func__, annotation_format=Format.STRING)
                contract_signature = inspect.signature(
                    getattr(Program, name), annotation_format=Format.STRING)
                raise TypeError(
                    f"{cls.__name__}.{name}{subclass_signature}"
                    f" must match {name}{contract_signature}".replace("'", ""))

    @staticmethod
    @abstractmethod
    def setup(grid: Grid) -> None:
        """``setup(grid)``"""

    @staticmethod
    @abstractmethod
    def update(grid: Grid) -> None:
        """``update(grid)``"""

    @staticmethod
    @abstractmethod
    def color_for_cell(grid: Grid, cell: Cell) -> Color:
        """``color_for_cell(grid, cell)``"""

    @staticmethod
    @abstractmethod
    def on_cell_click(grid: Grid, cell: Cell) -> None:
        """``on_cell_click(grid, cell)``"""

    @staticmethod
    @abstractmethod
    def on_key_press(grid: Grid, key: str) -> None:
        """``on_key_press(grid, key)``"""


def validate_program(program_class: type[Program]) -> None:
    """``validate_program(program_class)``"""
    program_class()
