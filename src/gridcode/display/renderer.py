"""``gridcode.display.renderer``"""

from ..grid import Cell, Grid
from .color import Color


class Renderer:
    """``Renderer``"""

    def __init__(self, grid: Grid, color_for_cell):
        self.grid = grid
        self.color_for_cell = color_for_cell

    @property
    def size(self) -> int:
        """``renderer.size``"""
        return self.grid.cells.size

    def render(self) -> list[Color]:
        """``renderer.render()``"""
        return [self.color_for_cell(Cell(x, y), self.grid)
                for y in range(self.size)
                for x in range(self.size)]
