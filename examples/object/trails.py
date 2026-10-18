#!/usr/bin/env python3

"""Trails"""

import random

from gridcode import *
from gridcode.data.object import ObjectData

TRAIL_LIFE = 60
DIRECTIONS = [UP, RIGHT, DOWN, LEFT]
COLORS = [Color(1.0, 0.35, 0.35),
          Color(0.35, 0.8, 1.0),
          Color(1.0, 0.85, 0.3),
          Color(0.55, 1.0, 0.6)]


class Agent:

    def __init__(self, cell: Cell, direction: Offset, color: Color):
        self.cell = cell
        self.direction = direction
        self.color = color


class Trails(Program, data_class=ObjectData, size=48, frame_rate=20):

    @staticmethod
    def setup(grid: Grid[ObjectData]) -> None:
        middle = grid.cells.size // 2
        grid.data.agents = [Agent(Cell(middle, middle), direction, color)
                            for direction, color in zip(DIRECTIONS, COLORS)]
        grid.data.trail = {}

    @staticmethod
    def update(grid: Grid[ObjectData]) -> None:
        grid.data.trail = {cell: (color, age - 1)
                           for cell, (color, age) in grid.data.trail.items()
                           if age > 1}

        for agent in grid.data.agents:
            grid.data.trail[agent.cell] = (agent.color, TRAIL_LIFE)

            ahead = Trails.ahead_of(grid, agent)
            if ahead in grid.data.trail:
                agent.direction = Trails.turn_right(agent.direction)
                ahead = Trails.ahead_of(grid, agent)

            agent.cell = ahead

    @staticmethod
    def color_for_cell(grid: Grid[ObjectData], cell: Cell) -> Color:
        for agent in grid.data.agents:
            if agent.cell == cell:
                return agent.color

        if cell in grid.data.trail:
            color, age = grid.data.trail[cell]
            return color.with_opacity(age / TRAIL_LIFE)

        return Color(0.0, 0.0, 0.0)

    @staticmethod
    def on_cell_click(grid: Grid[ObjectData], cell: Cell) -> None:
        grid.data.agents.append(Agent(cell,
                                      random.choice(DIRECTIONS),
                                      random.choice(COLORS)))

    @staticmethod
    def on_key_press(grid: Grid[ObjectData], key: str) -> None:
        if key == "space":
            grid.data.trail = {}

    @staticmethod
    def ahead_of(grid: Grid[ObjectData], agent: Agent) -> Cell:
        size = grid.cells.size
        return Cell((agent.cell.x + agent.direction.dx) % size,
                    (agent.cell.y + agent.direction.dy) % size)

    @staticmethod
    def turn_right(direction: Offset) -> Offset:
        return DIRECTIONS[(DIRECTIONS.index(direction) + 1) % len(DIRECTIONS)]


if __name__ == "__main__":
    run(Trails)
