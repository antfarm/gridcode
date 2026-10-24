#!/usr/bin/env python3

"""Game of Life"""

from gridcode import *


program = Program("Game of Life", size=64, frame_rate=60)


@program.setup
def setup(grid: Grid) -> None:
    cells = grid.cells.all()

    for cell in cells:
        grid.data.add(cell, {})

    alive_cells = grid.cells.random(count=len(cells) * 20 // 100)
    for map in grid.data.select(at_cells=alive_cells):
        map.set({"alive": True, "age": 1})

    count_neighbors(grid, cells)


@program.update
def update(grid: Grid) -> None:
    for cell in grid.cells.all():
        for map in grid.data.select(at_cells={cell}):
            neighbor_count = map["neighbors"]
            if map.has("alive"):
                if neighbor_count == 2 or neighbor_count == 3:
                    map["age"] = map["age"] + 1
                else:
                    map.delete("alive", "age")
            else:
                if neighbor_count == 3:
                    map.set({"alive": True, "age": 1})

    count_neighbors(grid, grid.cells.all())


@program.color
def color(grid: Grid, cell: Cell) -> Color:
    for map in grid.data.select(at_cells={cell}):
        if map.has("alive"):
            opacity = (10 - min(map["age"], 6)) / 10.0
            return Color(1.0, 0.8, 0.2).with_opacity(opacity)

    return Color(0.0, 0.0, 0.0)


@program.on_click
def on_click(grid: Grid, cell: Cell) -> None:
    for map in grid.data.select(at_cells={cell}):
        if map.has("alive"):
            map.delete("alive", "age")
        else:
            map.set({"alive": True, "age": 1})

    affected_cells = grid.cells.neighbors(cell, kind=MOORE, wrap=True) | {cell}
    count_neighbors(grid, affected_cells)


@program.on_key
def on_key(grid: Grid, key: str) -> None:
    pass


def count_neighbors(grid: Grid, cells: set[Cell]) -> None:
    for cell in cells:
        for map in grid.data.select(at_cells={cell}):
            map["neighbors"] = neighbors_alive_count(grid, cell)


def neighbors_alive_count(grid: Grid, cell: Cell) -> int:
    neighbor_cells = grid.cells.neighbors(cell, kind=MOORE, wrap=True)
    return grid.data.count(has={"alive"}, at_cells=neighbor_cells)


if __name__ == "__main__":
    run(program)
