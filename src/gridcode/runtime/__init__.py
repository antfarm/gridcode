"""``gridcode.runtime``"""

from ..grid import Cell, Grid
from .color import Color
from .program import Program

__all__ = [
    "Runtime",
    "Program",
    "Color",
]


class Runtime:
    """``Runtime``"""

    def __init__(self, grid: Grid, program: type[Program]):
        self.grid = grid
        self.name = program.__name__
        self.size = program.size
        self.frame_rate = program.frame_rate
        self.program = program()
        self.program.setup(self.grid)
        self.tick = 0

    def reset(self) -> None:
        """``runtime.reset()``"""
        self.grid.maps.clear()
        self.grid.globals.clear()
        self.program.setup(self.grid)
        self.tick = 0

    def step(self) -> None:
        """``runtime.step()``"""
        self.program.update(self.grid)
        self.tick += 1

    def key_press(self, key: str) -> None:
        """``runtime.key_press(key)``"""
        self.program.on_key_press(self.grid, key)

    def cell_click(self, x: int, y: int) -> None:
        """``runtime.cell_click(x, y)``"""
        self.program.on_cell_click(self.grid, Cell(x, y))

    def colors(self) -> list[Color]:
        """``runtime.colors()``"""
        return [self.program.color_for_cell(self.grid, Cell(x, y))
                for y in range(self.size)
                for x in range(self.size)]
