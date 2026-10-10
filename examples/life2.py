#!/usr/bin/env python3

"""Game of Life"""

import random

from gridcode import *


class Life2(Program, size=64, frame_rate=60):

    @staticmethod
    def neighbors_alive_count(cell: Cell, grid: Grid) -> int:
        neighbor_cells = grid.cells.wrap(grid.cells.neighbors(cell, kind=MOORE))
        return grid.maps.count(data={"alive": ANY}, at_cells=neighbor_cells)

    @staticmethod
    def count_neighbors(cells: set[Cell], grid: Grid) -> None:
        for cell in cells:
            for map in grid.maps.get(at_cells={cell}):
                map["neighbors"] = Life2.neighbors_alive_count(cell, grid)

    @staticmethod
    def setup(grid: Grid) -> None:
        cells = grid.cells.all()

        for cell in cells:
            grid.maps.add(cell, {})

        alive_cells = set(random.sample(list(cells), k=len(cells) * 20 // 100))
        for map in grid.maps.get(at_cells=alive_cells):
            map.set({"alive": True, "age": 1})

        Life2.count_neighbors(cells, grid)

    @staticmethod
    def update(grid: Grid) -> None:
        for cell in grid.cells.all():
            for map in grid.maps.get(at_cells={cell}):
                neighbor_count = map["neighbors"]
                if map.has({"alive": ANY}):
                    if neighbor_count == 2 or neighbor_count == 3:
                        map["age"] = map["age"] + 1
                    else:
                        map.delete({"alive", "age"})
                else:
                    if neighbor_count == 3:
                        map.set({"alive": True, "age": 1})

        Life2.count_neighbors(grid.cells.all(), grid)

    @staticmethod
    def color_for_cell(cell: Cell, grid: Grid) -> Color:
        for map in grid.maps.get(at_cells={cell}):
            if map.has({"alive": ANY}):
                opacity = (10 - min(map["age"], 6)) / 10.0
                return Color(1.0, 0.8, 0.2).with_opacity(opacity)

        return Color(0.0, 0.0, 0.0)

    @staticmethod
    def on_cell_click(cell: Cell, grid: Grid) -> None:
        for map in grid.maps.get(at_cells={cell}):
            if map.has({"alive": ANY}):
                map.delete({"alive", "age"})
            else:
                map.set({"alive": True, "age": 1})

        affected_cells = grid.cells.wrap(grid.cells.neighbors(cell, kind=MOORE)) | {cell}
        Life2.count_neighbors(affected_cells, grid)

    @staticmethod
    def on_key_press(key: str, grid: Grid) -> None:
        pass


if __name__ == "__main__":
    run(Life2)
