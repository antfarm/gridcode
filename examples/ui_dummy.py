#!/usr/bin/env python3

"""Empty"""

import random

from gridcode import *


def random_color() -> Color:
    return Color(random.random(), random.random(), random.random())


class UIDummy(Program, size=8, frame_rate=10):

    @staticmethod
    def setup(grid: Grid) -> None:
        grid.color1 = random_color()
        grid.color2 = random_color()

    @staticmethod
    def update(grid: Grid) -> None:
        grid.color1 = random_color()
        grid.color2 = random_color()

    @staticmethod
    def color_for_cell(grid: Grid, cell: Cell) -> Color:
        return grid.color1 if (cell.x + cell.y) % 2 == 0 else grid.color2

    @staticmethod
    def on_key_press(grid: Grid, key: str) -> None:
        pass

    @staticmethod
    def on_cell_click(grid: Grid, cell: Cell) -> None:
        pass


if __name__ == "__main__":
    run(UIDummy)
