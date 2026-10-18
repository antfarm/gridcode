"""``gridcode.runtime.program``"""

import inspect
from abc import ABC, abstractmethod
from annotationlib import Format

from ..cells import Cell
from ..grid import Grid
from .color import Color


class Program(ABC):
    """``Program``"""

    size: int
    frame_rate: float
    data_class: type

    def __init_subclass__(cls, size: int = 16, frame_rate: float = 8,
                          data_class: type | None = None, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.size = size
        cls.frame_rate = frame_rate
        if data_class is not None:
            cls.data_class = data_class

        for name in ("setup", "update", "color_for_cell", "on_cell_click", "on_key_press"):
            function = cls.__dict__.get(name)
            if function is None:
                continue
            if not isinstance(function, staticmethod):
                raise TypeError(f"{cls.__name__}.{name} must be a @staticmethod")

            if inspect.signature(function.__func__) != contract_signature(cls, name):
                subclass_text = inspect.signature(
                    function.__func__, annotation_format=Format.STRING)
                contract_text = inspect.signature(
                    getattr(Program, name), annotation_format=Format.STRING)
                raise TypeError(
                    f"{cls.__name__}.{name}{subclass_text}"
                    f" must match {name}{contract_text}".replace("'", ""))

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


def contract_signature(program_class: type[Program], name: str) -> inspect.Signature:
    """``contract_signature(program_class, name)``"""
    signature = inspect.signature(getattr(Program, name))
    parameters = list(signature.parameters.values())
    parameters[0] = parameters[0].replace(annotation=Grid[program_class.data_class])
    return signature.replace(parameters=parameters)


def validate_program(program_class: type[Program]) -> None:
    """``validate_program(program_class)``"""
    program_class()
