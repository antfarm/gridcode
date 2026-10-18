#!/usr/bin/env python3

"""Ant"""

import random

from gridcode import *
from gridcode.data.maps import MapsData


class Ant(Program, data_class=MapsData, size=32, frame_rate=10):

    @staticmethod
    def setup(grid: Grid[MapsData]) -> None:
        grid.data.globals.add("keyboard", {"direction": Ant.random_direction(),
                                      "idle_ticks": 0})

        cell = Cell(grid.cells.size // 2, grid.cells.size // 2)

        grid.data.maps.add(cell, {"type": "ant"})

        grid.data.maps.add(cell, {"type": "trail",
                             "concentration": 1.0})

    @staticmethod
    def update(grid: Grid[MapsData]) -> None:
        Ant.decay_trails(grid)
        Ant.randomize_direction(grid)
        Ant.move_ant(grid)

    @staticmethod
    def color_for_cell(grid: Grid[MapsData], cell: Cell) -> Color:
        if grid.data.maps.exists(matches={"type": "ant"}, at_cells={cell}):
            return Color(1.0, 0.8, 0.2)

        for trail in grid.data.maps.select(matches={"type": "trail"}, at_cells={cell}):
            opacity = min(1.0, trail["concentration"] * 0.5)
            return Color(0.2, 0.9, 0.0, opacity)

        return Color(0.0, 0.0, 0.0)

    @staticmethod
    def on_cell_click(grid: Grid[MapsData], cell: Cell) -> None:
        pass

    @staticmethod
    def on_key_press(grid: Grid[MapsData], key: str) -> None:
        direction = {"left": LEFT, "right": RIGHT, "up": UP, "down": DOWN}.get(key)

        if direction is not None:
            keyboard = grid.data.globals.get("keyboard")
            keyboard["direction"] = direction
            keyboard["idle_ticks"] = 0

        if key == "space":
            grid.data.maps.clear()
            grid.data.globals.clear()
            Ant.setup(grid)

    @staticmethod
    def random_direction() -> Offset:
        return random.choice([LEFT, RIGHT, UP, DOWN])

    @staticmethod
    def decay_trails(grid: Grid[MapsData]) -> None:
        evaporation_rate = 0.07

        for trail in grid.data.maps.select(matches={"type": "trail"}):
            concentration = trail["concentration"]

            if concentration < 0.07:
                grid.data.maps.delete(trail)
            else:
                trail["concentration"] = concentration * (1.0 - evaporation_rate)

    @staticmethod
    def randomize_direction(grid: Grid[MapsData]) -> None:
        keyboard = grid.data.globals.get("keyboard")
        idle_ticks = keyboard["idle_ticks"]

        if idle_ticks > 50 and random.randrange(100) < 3:
            keyboard["idle_ticks"] = 0
            keyboard["direction"] = Ant.random_direction()
        else:
            keyboard["idle_ticks"] = idle_ticks + 1

    @staticmethod
    def move_ant(grid: Grid[MapsData]) -> None:
        keyboard = grid.data.globals.get("keyboard")
        direction = keyboard["direction"]

        for ant in grid.data.maps.select(matches={"type": "ant"}):
            cell = grid.cells.wrap(ant.cell + direction)

            grid.data.maps.move(ant, cell)

            trails = grid.data.maps.select(matches={"type": "trail"}, at_cells={cell})
            if trails:
                for trail in trails:
                    trail["concentration"] = trail["concentration"] + 1.0
            else:
                grid.data.maps.add(cell, {"type": "trail",
                                     "concentration": 1.0})


if __name__ == "__main__":
    run(Ant)
