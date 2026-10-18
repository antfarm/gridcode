#!/usr/bin/env python3

"""Ants"""

import random

from gridcode import *
from gridcode.data.maps import MapsData


class Ants(Program, data_class=MapsData, size=64, frame_rate=10):

    @staticmethod
    def setup(grid: Grid[MapsData]) -> None:
        for _ in range(100):
            grid.data.maps.add(grid.cells.random(),
                          {"type": "ant",
                           "direction": Ants.random_direction()})

    @staticmethod
    def update(grid: Grid[MapsData]) -> None:
        evaporation_rate = 0.07

        for trail in grid.data.maps.select(matches={"type": "trail"}):
            concentration = trail["concentration"]
            new_concentration = concentration * (1.0 - evaporation_rate)
            if new_concentration < evaporation_rate:
                grid.data.maps.delete(trail)
            else:
                trail["concentration"] = new_concentration

        for ant in grid.data.maps.select(matches={"type": "ant"}):
            cell = ant.cell
            trails = grid.data.maps.select(matches={"type": "trail"}, at_cells={cell})
            if trails:
                for trail in trails:
                    trail["concentration"] = trail["concentration"] + 1.0
            else:
                grid.data.maps.add(cell, {"type": "trail", "concentration": 1.0})
            new_cell = grid.cells.wrap(cell + ant["direction"])
            grid.data.maps.move(ant, new_cell)

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
        pass

    @staticmethod
    def random_direction() -> Offset:
        return Offset(random.choice([-1, 0, 1]), 1)


if __name__ == "__main__":
    run(Ants)
