"""``gridcode.runtime``"""

from ..cells import Cell
from .color import Color
from .grid import Grid
from .program import Program

__all__ = [
    "Runtime",
    "Program",
    "Color",
    "Grid",
]


class Runtime:
    """``Runtime``"""

    def __init__(self, program: Program):
        program.check_complete()

        self.program = program
        self.inspected_cell = None
        self.reset()

    @property
    def name(self) -> str:
        """``runtime.name``"""
        return self.program.title

    @property
    def size(self) -> int:
        """``runtime.size``"""
        return self.program.size

    @property
    def frame_rate(self) -> float:
        """``runtime.frame_rate``"""
        return self.program.frame_rate

    def reset(self) -> None:
        """``runtime.reset()``"""
        self.grid = Grid(self.size, self.program.index)
        self.program._setup(self.grid)
        self.tick = 0
        self._print_inspection("setup")

    def step(self) -> None:
        """``runtime.step()``"""
        self.program._update(self.grid)
        self.tick += 1
        self._print_inspection("update")

    def key_press(self, key: str) -> None:
        """``runtime.key_press(key)``"""
        self.program._on_key(self.grid, key)
        self._print_inspection(f"on_key {key}")

    def cell_click(self, x: int, y: int) -> None:
        """``runtime.cell_click(x, y)``"""
        self.program._on_click(self.grid, Cell(x, y))
        self._print_inspection(f"on_click ({x}, {y})")

    def start_inspection(self, x: int, y: int) -> None:
        """``runtime.start_inspection(x, y)``"""
        self.inspected_cell = (x, y)
        self._print_inspection("inspect")

    def stop_inspection(self, x: int, y: int) -> None:
        """``runtime.stop_inspection(x, y)``"""
        self.inspected_cell = None

    def colors(self) -> list[Color]:
        """``runtime.colors()``"""
        return [self.program._color(self.grid, Cell(x, y))
                for y in range(self.size)
                for x in range(self.size)]

    def _print_inspection(self, event: str) -> None:
        if self.inspected_cell is None:
            return

        x, y = self.inspected_cell
        print(f"tick {self.tick}, {event}: cell ({x}, {y})")
