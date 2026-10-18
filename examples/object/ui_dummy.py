#!/usr/bin/env python3

"""Empty"""

import random

from gridcode import *
from gridcode.data.object import ObjectData


def random_color() -> Color:
    return Color(random.random(), random.random(), random.random())


class UIDummy(Program, data_class=ObjectData, size=8, frame_rate=10):

    @staticmethod
    def setup(grid: Grid[ObjectData]) -> None:
        grid.data.color1 = random_color()
        grid.data.color2 = random_color()

    @staticmethod
    def update(grid: Grid[ObjectData]) -> None:
        grid.data.color1 = random_color()
        grid.data.color2 = random_color()

    @staticmethod
    def color_for_cell(grid: Grid[ObjectData], cell: Cell) -> Color:
        return grid.data.color1 if (cell.x + cell.y) % 2 == 0 else grid.data.color2

    @staticmethod
    def on_key_press(grid: Grid[ObjectData], key: str) -> None:
        pass

    @staticmethod
    def on_cell_click(grid: Grid[ObjectData], cell: Cell) -> None:
        pass


if __name__ == "__main__":
    run(UIDummy)
