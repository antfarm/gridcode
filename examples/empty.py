#!/usr/bin/env python3

"""Empty"""

from gridcode import *


class Empty(Program, size=16, frame_rate=8):

    @staticmethod
    def setup(grid: Grid) -> None:
        pass

    @staticmethod
    def update(grid: Grid) -> None:
        pass

    @staticmethod
    def color_for_cell(cell: Cell, grid: Grid) -> Color:
        return Color(1.0, 1.0, 1.0)

    @staticmethod
    def on_key_press(key: str, grid: Grid) -> None:
        pass

    @staticmethod
    def on_cell_click(cell: Cell, grid: Grid) -> None:
        pass


if __name__ == "__main__":
    run(Empty)
