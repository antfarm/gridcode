"""``gridcode.runtime``"""

from ..cells import Cell
from ..grid import Grid
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
        self._print_inspection("setup")

    def step(self) -> None:
        """``runtime.step()``"""
        self.program_class.update(self.grid)
        self.tick += 1
        self._print_inspection("update")

    def key_press(self, key: str) -> None:
        """``runtime.key_press(key)``"""
        self.program_class.on_key_press(self.grid, key)
        self._print_inspection(f"on_key_press {key}")

    def cell_click(self, x: int, y: int) -> None:
        """``runtime.cell_click(x, y)``"""
        self.program_class.on_cell_click(self.grid, Cell(x, y))
        self._print_inspection(f"on_cell_click ({x}, {y})")

    def start_inspection(self, x: int, y: int) -> None:
        """``runtime.start_inspection(x, y)``"""
        self.inspected_cell = (x, y)
        self._print_inspection("inspect")

    def stop_inspection(self, x: int, y: int) -> None:
        """``runtime.stop_inspection(x, y)``"""
        self.inspected_cell = None

    def colors(self) -> list[Color]:
        """``runtime.colors()``"""
        return [self.program_class.color_for_cell(self.grid, Cell(x, y))
                for y in range(self.size)
                for x in range(self.size)]

    def _print_inspection(self, event: str) -> None:
        if self.inspected_cell is None:
            return

        x, y = self.inspected_cell
        print(f"tick {self.tick}, {event}: cell ({x}, {y})")
