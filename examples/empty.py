#!/usr/bin/env python3

"""Empty"""

from gridcode import *


program = Program("Empty", size=16, frame_rate=8)


@program.setup
def setup(grid: Grid) -> None:
    pass


@program.update
def update(grid: Grid) -> None:
    pass


@program.color
def color(grid: Grid, cell: Cell) -> Color:
    return Color(1.0, 1.0, 1.0)


@program.on_click
def on_click(grid: Grid, cell: Cell) -> None:
    pass


@program.on_key
def on_key(grid: Grid, key: str) -> None:
    pass


if __name__ == "__main__":
    run(program)
