#!/usr/bin/env python3

"""Blink"""

from gridcode import *


class Blink(Program, size=16, frame_rate=2):

    @staticmethod
    def setup(grid: Grid) -> None:
        for cell in grid.cells.all():
            if cell.x == cell.y:
                grid.maps.add(cell, {})

    @staticmethod
    def update(grid: Grid) -> None:
        for cell in grid.cells.all():
            Blink.toggle_cell(cell, grid)

    @staticmethod
    def color_for_cell(cell: Cell, grid: Grid) -> Color:
        if grid.maps.has(at_cells={cell}):
            return Color(1.0, 0.8, 0.2)
        return Color(0.0, 0.0, 0.0)

    @staticmethod
    def on_cell_click(cell: Cell, grid: Grid) -> None:
        Blink.toggle_cell(cell, grid)

    @staticmethod
    def on_key_press(key: str, grid: Grid) -> None:
        pass

    @staticmethod
    def toggle_cell(cell: Cell, grid: Grid) -> None:
        maps = grid.maps.get(at_cells={cell})
        if maps:
            grid.maps.delete(maps)
        else:
            grid.maps.add(cell, {})


if __name__ == "__main__":
    run(Blink)
