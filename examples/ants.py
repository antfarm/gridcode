#!/usr/bin/env python3

"""Ants"""

import random

from gridcode import *


program = Program("Ants", size=64, frame_rate=10)


@program.setup
def setup(grid: Grid) -> None:
    for _ in range(100):
        grid.data.add(grid.cells.random(),
                      {"type": "ant",
                       "direction": random_direction()})


@program.update
def update(grid: Grid) -> None:
    evaporation_rate = 0.07

    for trail in grid.data.select(matches={"type": "trail"}):
        concentration = trail["concentration"]
        new_concentration = concentration * (1.0 - evaporation_rate)
        if new_concentration < evaporation_rate:
            grid.data.delete(trail)
        else:
            trail["concentration"] = new_concentration

    for ant in grid.data.select(matches={"type": "ant"}):
        cell = ant.cell
        trails = grid.data.select(matches={"type": "trail"}, at_cells={cell})
        if trails:
            for trail in trails:
                trail["concentration"] = trail["concentration"] + 1.0
        else:
            grid.data.add(cell, {"type": "trail", "concentration": 1.0})
        new_cell = grid.cells.wrap(cell + ant["direction"])
        grid.data.move(ant, new_cell)


@program.color
def color(grid: Grid, cell: Cell) -> Color:
    if grid.data.exists(matches={"type": "ant"}, at_cells={cell}):
        return Color(1.0, 0.8, 0.2)
    for trail in grid.data.select(matches={"type": "trail"}, at_cells={cell}):
        opacity = min(1.0, trail["concentration"] * 0.5)
        return Color(0.2, 0.9, 0.0, opacity)
    return Color(0.0, 0.0, 0.0)


@program.on_click
def on_click(grid: Grid, cell: Cell) -> None:
    pass


@program.on_key
def on_key(grid: Grid, key: str) -> None:
    pass


def random_direction() -> Offset:
    return Offset(random.choice([-1, 0, 1]), 1)


if __name__ == "__main__":
    run(program)
