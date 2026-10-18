#!/usr/bin/env python3

"""Blink"""

from gridcode import *
from gridcode.data.maps import MapsData


class Blink(Program, data_class=MapsData, size=16, frame_rate=2):

    @staticmethod
    def setup(grid: Grid[MapsData]) -> None:
        for cell in grid.cells.all():
            if cell.x == cell.y:
                grid.data.maps.add(cell, {})

    @staticmethod
    def update(grid: Grid[MapsData]) -> None:
        for cell in grid.cells.all():
            Blink.toggle_cell(grid, cell)

    @staticmethod
    def color_for_cell(grid: Grid[MapsData], cell: Cell) -> Color:
        if grid.data.maps.exists(at_cells={cell}):
            return Color(1.0, 0.8, 0.2)
        return Color(0.0, 0.0, 0.0)

    @staticmethod
    def on_cell_click(grid: Grid[MapsData], cell: Cell) -> None:
        Blink.toggle_cell(grid, cell)

    @staticmethod
    def on_key_press(grid: Grid[MapsData], key: str) -> None:
        pass

    @staticmethod
    def toggle_cell(grid: Grid[MapsData], cell: Cell) -> None:
        maps = grid.data.maps.select(at_cells={cell})
        if maps:
            for map in maps:
                grid.data.maps.delete(map)
        else:
            grid.data.maps.add(cell, {})


if __name__ == "__main__":
    run(Blink)
