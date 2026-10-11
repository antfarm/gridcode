#!/usr/bin/env python3

"""Pong"""

import random

from gridcode import *


class Pong(Program, size=32, frame_rate=30):

    @staticmethod
    def setup(grid: Grid) -> None:
        for wall_cell in grid.cells.col(0):
            grid.maps.add(wall_cell, {"type": "wall", "dx": 1})
        for wall_cell in grid.cells.col(grid.cells.size - 1):
            grid.maps.add(wall_cell, {"type": "wall", "dx": -1})
        for wall_cell in grid.cells.row(0):
            grid.maps.add(wall_cell, {"type": "wall", "dy": 1})
        for wall_cell in grid.cells.row(grid.cells.size - 1):
            grid.maps.add(wall_cell, {"type": "out"})

        center = grid.cells.size // 2

        paddle_origin = Cell(center, grid.cells.size - 1)
        paddle_cells = grid.cells.neighbors(paddle_origin,
                                            kind=HORIZONTAL,
                                            radius=2) | {paddle_origin}
        for paddle_cell in paddle_cells:
            grid.maps.add(paddle_cell, {"type": "paddle"})

        ball_cell = Cell(center - 2 + random.randrange(5), grid.cells.size - 2)
        grid.maps.add(ball_cell, {"type": "ball",
                                  "dx": random.choice([-1, 1]),
                                  "dy": -1})

    @staticmethod
    def update(grid: Grid) -> None:
        for ball in grid.maps.get(data={"type": "ball"}):
            dx, dy = ball.get("dx", "dy")
            ball_cell = ball.cell
            next_ball_cell = Cell(ball_cell.x + dx, ball_cell.y + dy)

            if grid.maps.has(data={"type": "wall"}, at_cells={next_ball_cell}):
                for wall in grid.maps.get(data={"type": "wall"}, at_cells={next_ball_cell}):
                    new_dx = wall["dx"] if wall.has("dx") else dx
                    new_dy = wall["dy"] if wall.has("dy") else dy
                    dest = Cell(ball_cell.x + new_dx, ball_cell.y + new_dy)
                    grid.maps.move(ball, dest)
                    ball.set({"dx": new_dx, "dy": new_dy})
            elif grid.maps.has(data={"type": "paddle"},
                               at_cells={Cell(ball_cell.x, next_ball_cell.y)}):
                new_dx = random.choice([-1, 1])
                dest = Cell(ball_cell.x + new_dx, ball_cell.y - 1)
                grid.maps.move(ball, dest)
                ball.set({"dx": new_dx, "dy": -1})
            elif grid.maps.has(data={"type": "out"}, at_cells={next_ball_cell}):
                grid.maps.delete(ball)
                grid.maps.add(next_ball_cell, {"type": "ball-out"})
            else:
                grid.maps.move(ball, next_ball_cell)

    @staticmethod
    def color_for_cell(grid: Grid, cell: Cell) -> Color:
        if grid.maps.has(data={"type": "wall"}, at_cells={cell}):
            return Color(1.0, 1.0, 1.0)
        if grid.maps.has(data={"type": "ball-out"}, at_cells={cell}):
            return Color(1.0, 0.0, 0.0)
        if grid.maps.has(data={"type": "ball"}, at_cells={cell}):
            return Color(0.2, 0.9, 0.0)
        if grid.maps.has(data={"type": "paddle"}, at_cells={cell}):
            return Color(1.0, 0.8, 0.2)
        return Color(0.0, 0.0, 0.0)

    @staticmethod
    def on_cell_click(grid: Grid, cell: Cell) -> None:
        direction = "left" if cell.x < grid.cells.size // 2 else "right"
        Pong.move_paddle(grid, direction)

    @staticmethod
    def on_key_press(grid: Grid, key: str) -> None:
        if key == "left":
            Pong.move_paddle(grid, "left")
        if key == "right":
            Pong.move_paddle(grid, "right")
        if key == "space":
            grid.maps.clear()
            grid.globals.clear()
            Pong.setup(grid)

    @staticmethod
    def move_paddle(grid: Grid, direction: str) -> None:
        dx = -1 if direction == "left" else 1

        paddle_cells = grid.maps.cells_of(data={"type": "paddle"})
        wall_cells = grid.maps.cells_of(data={"type": "wall"})

        if not ({cell + Offset(dx, 0) for cell in paddle_cells} & wall_cells):
            for paddle in grid.maps.get(data={"type": "paddle"}):
                grid.maps.move(paddle, Offset(dx, 0))


if __name__ == "__main__":
    run(Pong)
