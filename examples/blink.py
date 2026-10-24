#!/usr/bin/env python3

"""Blink"""

from gridcode import *


program = Program("Blink", size=16, frame_rate=2)


@program.setup
def setup(grid: Grid) -> None:
    for cell in grid.cells.all():
        if cell.x == cell.y:
            grid.data.add(cell, {})


@program.update
def update(grid: Grid) -> None:
    for cell in grid.cells.all():
        toggle_cell(grid, cell)


@program.color
def color(grid: Grid, cell: Cell) -> Color:
    if grid.data.exists(at_cells={cell}):
        return Color(1.0, 0.8, 0.2)
    return Color(0.0, 0.0, 0.0)


@program.on_click
def on_click(grid: Grid, cell: Cell) -> None:
    toggle_cell(grid, cell)


@program.on_key
def on_key(grid: Grid, key: str) -> None:
    pass


def toggle_cell(grid: Grid, cell: Cell) -> None:
    maps = grid.data.select(at_cells={cell})
    if maps:
        for map in maps:
            grid.data.delete(map)
    else:
        grid.data.add(cell, {})


if __name__ == "__main__":
    run(program)
