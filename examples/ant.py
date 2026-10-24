#!/usr/bin/env python3

"""Ant"""

import random

from gridcode import *


program = Program("Ant", size=32, frame_rate=10)


@program.setup
def setup(grid: Grid) -> None:
    grid.data.globals.set({"key_direction": random_direction(),
                           "key_idle_ticks": 0})

    cell = Cell(grid.cells.size // 2, grid.cells.size // 2)

    grid.data.add(cell, {"type": "ant"})

    grid.data.add(cell, {"type": "trail",
                         "concentration": 1.0})


@program.update
def update(grid: Grid) -> None:
    decay_trails(grid)
    randomize_direction(grid)
    move_ant(grid)


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
    direction = {"left": LEFT, "right": RIGHT, "up": UP, "down": DOWN}.get(key)

    if direction is not None:
        grid.data.globals["key_direction"] = direction
        grid.data.globals["key_idle_ticks"] = 0

    if key == "space":
        grid.data.clear()
        setup(grid)


def random_direction() -> Offset:
    return random.choice([LEFT, RIGHT, UP, DOWN])


def decay_trails(grid: Grid) -> None:
    evaporation_rate = 0.07

    for trail in grid.data.select(matches={"type": "trail"}):
        concentration = trail["concentration"]

        if concentration < 0.07:
            grid.data.delete(trail)
        else:
            trail["concentration"] = concentration * (1.0 - evaporation_rate)


def randomize_direction(grid: Grid) -> None:
    idle_ticks = grid.data.globals["key_idle_ticks"]

    if idle_ticks > 50 and random.randrange(100) < 3:
        grid.data.globals["key_idle_ticks"] = 0
        grid.data.globals["key_direction"] = random_direction()
    else:
        grid.data.globals["key_idle_ticks"] = idle_ticks + 1


def move_ant(grid: Grid) -> None:
    direction = grid.data.globals["key_direction"]

    for ant in grid.data.select(matches={"type": "ant"}):
        cell = grid.cells.wrap(ant.cell + direction)

        grid.data.move(ant, cell)

        trails = grid.data.select(matches={"type": "trail"}, at_cells={cell})
        if trails:
            for trail in trails:
                trail["concentration"] = trail["concentration"] + 1.0
        else:
            grid.data.add(cell, {"type": "trail",
                                 "concentration": 1.0})


if __name__ == "__main__":
    run(program)
