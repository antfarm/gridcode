"""``gridcode.runtime``"""

from ..grid import Cell, Grid
from .color import Color
from .program import Program, validate_program

__all__ = [
    "Runtime",
    "Program",
    "Color",
]


class Runtime:
    """``Runtime``"""

    def __init__(self, program_class: type[Program]):
        validate_program(program_class)

        self.program_class = program_class
        self.name = program_class.__name__
        self.size = program_class.size
        self.frame_rate = program_class.frame_rate
        self.inspected_cell = None
        self.reset()

    def reset(self) -> None:
        """``runtime.reset()``"""
        self.grid = Grid(self.size)
        self.program_class.setup(self.grid)
        self.tick = 0

    def step(self) -> None:
        """``runtime.step()``"""
        self.program_class.update(self.grid)
        self.tick += 1

        if self.inspected_cell is not None:
            x, y = self.inspected_cell
            print(f"tick {self.tick}: cell ({x}, {y})")

    def key_press(self, key: str) -> None:
        """``runtime.key_press(key)``"""
        self.program_class.on_key_press(self.grid, key)

    def cell_click(self, x: int, y: int) -> None:
        """``runtime.cell_click(x, y)``"""
        self.program_class.on_cell_click(self.grid, Cell(x, y))

    def start_inspection(self, x: int, y: int) -> None:
        """``runtime.start_inspection(x, y)``"""
        self.inspected_cell = (x, y)

    def stop_inspection(self, x: int, y: int) -> None:
        """``runtime.stop_inspection(x, y)``"""
        self.inspected_cell = None

    def colors(self) -> list[Color]:
        """``runtime.colors()``"""
        return [self.program_class.color_for_cell(self.grid, Cell(x, y))
                for y in range(self.size)
                for x in range(self.size)]
