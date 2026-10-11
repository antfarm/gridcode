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
            Blink.toggle_cell(grid, cell)

    @staticmethod
    def color_for_cell(grid: Grid, cell: Cell) -> Color:
        if grid.maps.exists(at_cells={cell}):
            return Color(1.0, 0.8, 0.2)
        return Color(0.0, 0.0, 0.0)

    @staticmethod
    def on_cell_click(grid: Grid, cell: Cell) -> None:
        Blink.toggle_cell(grid, cell)

    @staticmethod
    def on_key_press(grid: Grid, key: str) -> None:
        pass

    @staticmethod
    def toggle_cell(grid: Grid, cell: Cell) -> None:
        maps = grid.maps.select(at_cells={cell})
        if maps:
            for map in maps:
                grid.maps.delete(map)
        else:
            grid.maps.add(cell, {})


if __name__ == "__main__":
    run(Blink)
