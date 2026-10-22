#!/usr/bin/env python3

"""RGB"""

import random

from gridcode import *


program = Program("RGB", size=16, frame_rate=100)


@program.setup
def setup(grid: Grid) -> None:
    for cell in grid.cells.all():
        grid.maps.add(cell, {"type": "counts",
                             "r": 0,
                             "g": 0,
                             "b": 0})

        grid.maps.add(cell, {"type": "channels",
                             "red": 0,
                             "green": 0,
                             "blue": 0})


@program.update
def update(grid: Grid) -> None:
    counts = random.choice(list(grid.maps.select(matches={"type": "counts"})))

    channel = random.choice(["r", "g", "b"])
    counts[channel] = counts[channel] + 1

    r, g, b = counts.get("r", "g", "b")
    brightest = max(r, g, b) * 1.0

    for channels in grid.maps.select(at_cells={counts.cell}, matches={"type": "channels"}):
        channels.set({"red": r / brightest,
                      "green": g / brightest,
                      "blue": b / brightest})


@program.color
def color(grid: Grid, cell: Cell) -> Color:
    for channels in grid.maps.select(at_cells={cell}, matches={"type": "channels"}):
        return Color(channels["red"], channels["green"], channels["blue"])

    return Color(0, 0, 0)


@program.on_click
def on_click(grid: Grid, cell: Cell) -> None:
    pass


@program.on_key
def on_key(grid: Grid, key: str) -> None:
    pass


if __name__ == "__main__":
    run(program)
