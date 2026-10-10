#!/usr/bin/env python3

"""Ant"""

import random

from gridcode import *


class Ant(Program, size=32, frame_rate=10):

    @staticmethod
    def setup(grid: Grid) -> None:
        grid.globals.add("keyboard", {"direction": Ant.random_direction(),
                                      "idle_ticks": 0})

        cell = Cell(grid.cells.size // 2, grid.cells.size // 2)

        grid.maps.add(cell, {"type": "ant"})

        grid.maps.add(cell, {"type": "trail",
                             "concentration": 1.0})

    @staticmethod
    def update(grid: Grid) -> None:
        Ant.decay_trails(grid)
        Ant.randomize_direction(grid)
        Ant.move_ant(grid)

    @staticmethod
    def color_for_cell(grid: Grid, cell: Cell) -> Color:
        if grid.maps.has(data={"type": "ant"}, at_cells={cell}):
            return Color(1.0, 0.8, 0.2)

        for trail in grid.maps.get(data={"type": "trail"}, at_cells={cell}):
            opacity = min(1.0, trail["concentration"] * 0.5)
            return Color(0.2, 0.9, 0.0, opacity)

        return Color(0.0, 0.0, 0.0)

    @staticmethod
    def on_cell_click(grid: Grid, cell: Cell) -> None:
        pass

    @staticmethod
    def on_key_press(grid: Grid, key: str) -> None:
        direction = {"left": LEFT, "right": RIGHT, "up": UP, "down": DOWN}.get(key)

        if direction is not None:
            keyboard = grid.globals.get("keyboard")
            keyboard["direction"] = direction
            keyboard["idle_ticks"] = 0

        if key == "space":
            grid.maps.clear()
            grid.globals.clear()
            Ant.setup(grid)

    @staticmethod
    def move_ant(grid: Grid) -> None:
        keyboard = grid.globals.get("keyboard")
        direction = keyboard["direction"]

        for ant in grid.maps.get(data={"type": "ant"}):
            cell = grid.cells.wrap(ant.cell + direction)

            grid.maps.move(ant, cell)

            trails = grid.maps.get(data={"type": "trail"}, at_cells={cell})
            if trails:
                for trail in trails:
                    trail["concentration"] = trail["concentration"] + 1.0
            else:
                grid.maps.add(cell, {"type": "trail",
                                     "concentration": 1.0})

    @staticmethod
    def decay_trails(grid: Grid) -> None:
        evaporation_rate = 0.07

        for trail in grid.maps.get(data={"type": "trail"}):
            concentration = trail["concentration"]

            if concentration < 0.07:
                grid.maps.delete(trail)
            else:
                trail["concentration"] = concentration * (1.0 - evaporation_rate)

    @staticmethod
    def randomize_direction(grid: Grid) -> None:
        keyboard = grid.globals.get("keyboard")
        idle_ticks = keyboard["idle_ticks"]

        if idle_ticks > 50 and random.randrange(100) < 3:
            keyboard["idle_ticks"] = 0
            keyboard["direction"] = Ant.random_direction()
        else:
            keyboard["idle_ticks"] = idle_ticks + 1

    @staticmethod
    def random_direction() -> Offset:
        return random.choice([LEFT, RIGHT, UP, DOWN])


if __name__ == "__main__":
    run(Ant)
