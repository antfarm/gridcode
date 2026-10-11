#!/usr/bin/env python3

"""Game of Life"""

from gridcode import *


class Life(Program, size=64, frame_rate=60):

    @staticmethod
    def setup(grid: Grid) -> None:
        for cell in grid.cells.all():
            grid.maps.add(cell, {"neighbors": 0})

        cells = grid.cells.all()
        alive_cells = grid.cells.random(count=len(cells) * 20 // 100)
        for map in grid.maps.get(at_cells=alive_cells):
            map.set({"alive": True, "age": 1})

    @staticmethod
    def update(grid: Grid) -> None:
        for cell in grid.cells.all():
            for map in grid.maps.get(at_cells={cell}):
                map["neighbors"] = Life.neighbors_alive_count(grid, cell)

        for cell in grid.cells.all():
            for map in grid.maps.get(at_cells={cell}):
                neighbor_count = map["neighbors"]
                if map.has("alive"):
                    if neighbor_count == 2 or neighbor_count == 3:
                        map["age"] = map["age"] + 1
                    else:
                        map.delete({"alive", "age"})
                else:
                    if neighbor_count == 3:
                        map.set({"alive": True, "age": 1})

    @staticmethod
    def color_for_cell(grid: Grid, cell: Cell) -> Color:
        for map in grid.maps.get(at_cells={cell}):
            if map.has("alive"):
                opacity = (10 - min(map["age"], 6)) / 10.0
                return Color(1.0, 0.8, 0.2).with_opacity(opacity)

        return Color(0.0, 0.0, 0.0)

    @staticmethod
    def on_cell_click(grid: Grid, cell: Cell) -> None:
        for map in grid.maps.get(at_cells={cell}):
            if map.has("alive"):
                map.delete({"alive", "age"})
            else:
                map.set({"alive": True, "age": 1})

    @staticmethod
    def on_key_press(grid: Grid, key: str) -> None:
        pass

    @staticmethod
    def neighbors_alive_count(grid: Grid, cell: Cell) -> int:
        neighbor_cells = grid.cells.wrap(grid.cells.neighbors(cell, kind=MOORE))
        return grid.maps.count(data={"alive": ANY}, at_cells=neighbor_cells)


if __name__ == "__main__":
    run(Life)
