#!/usr/bin/env python3

"""Empty"""

from gridcode import *
from gridcode.data.maps import MapsData


class Empty(Program, data_class=MapsData, size=16, frame_rate=8):

    @staticmethod
    def setup(grid: Grid[MapsData]) -> None:
        pass

    @staticmethod
    def update(grid: Grid[MapsData]) -> None:
        pass

    @staticmethod
    def color_for_cell(grid: Grid[MapsData], cell: Cell) -> Color:
        return Color(1.0, 1.0, 1.0)

    @staticmethod
    def on_key_press(grid: Grid[MapsData], key: str) -> None:
        pass

    @staticmethod
    def on_cell_click(grid: Grid[MapsData], cell: Cell) -> None:
        pass


if __name__ == "__main__":
    run(Empty)
