#!/usr/bin/env python3

"""Game of Life"""

import random

from gridcode import *


program = Program("Game of Life", size=64, frame_rate=60)


@program.setup
def setup(grid: Grid) -> None:
    for cell in grid.cells.all():
        if random.randrange(100) < 20:
            grid.data.add(cell, {"alive": True, "age": 1})


@program.update
def update(grid: Grid) -> None:
    for cell in grid.cells.all():
        neighbor_cells = grid.cells.neighbors(cell, kind=MOORE, wrap=True)
        neighbor_count = grid.data.count(matches={"alive": True},
                                         at_cells=neighbor_cells)
        state = only(grid.data.select(at_cells={cell}), None)

        if state is None:
            if neighbor_count == 3:
                grid.data.add(cell, {"born": True})
        else:
            if neighbor_count not in (2, 3):
                state["dying"] = True

    for state in grid.data.select(has={"dying"}):
        grid.data.delete(state)

    for state in grid.data.select(matches={"alive": True}):
        state["age"] = state["age"] + 1

    for state in grid.data.select(has={"born"}):
        state.delete("born")
        state.set({"alive": True, "age": 1})


@program.color
def color(grid: Grid, cell: Cell) -> Color:
    state = only(grid.data.select(at_cells={cell}), None)

    if state is None:
        return Color(0.0, 0.0, 0.0)

    opacity = (10 - min(state["age"], 6)) / 10.0
    return Color(1.0, 0.8, 0.2).with_opacity(opacity)


@program.on_click
def on_click(grid: Grid, cell: Cell) -> None:
    state = only(grid.data.select(at_cells={cell}), None)

    if state is None:
        grid.data.add(cell, {"alive": True, "age": 1})
    else:
        grid.data.delete(state)


@program.on_key
def on_key(grid: Grid, key: str) -> None:
    pass


if __name__ == "__main__":
    run(program)
