"""``gridcode.program.runner``"""

from ..grid import Cell, Grid
from .program import Program


class Runner:
    """``Runner``"""

    def __init__(self, grid: Grid, program: type[Program]):
        self.grid = grid
        self.program = program()
        self.program.setup(self.grid)
        self.tick = 0

    def reset(self) -> None:
        """``runner.reset()``"""
        self.grid.maps.clear()
        self.grid.globals.clear()
        self.program.setup(self.grid)
        self.tick = 0

    def step(self) -> None:
        """``runner.step()``"""
        self.program.update(self.grid)
        self.tick += 1

    def key_press(self, key: str) -> None:
        """``runner.key_press(key)``"""
        self.program.on_key_press(key, self.grid)

    def cell_click(self, cell: Cell) -> None:
        """``runner.cell_click(cell)``"""
        self.program.on_cell_click(cell, self.grid)
