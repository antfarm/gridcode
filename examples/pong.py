#!/usr/bin/env python3

"""Pong"""

import random

from gridcode import *


program = Program("Pong", size=32, frame_rate=30)


@program.setup
def setup(grid: Grid) -> None:
    for wall_cell in grid.cells.column(0):
        grid.maps.add(wall_cell, {"type": "wall", "dx": 1})
    for wall_cell in grid.cells.column(grid.cells.size - 1):
        grid.maps.add(wall_cell, {"type": "wall", "dx": -1})
    for wall_cell in grid.cells.row(0):
        grid.maps.add(wall_cell, {"type": "wall", "dy": 1})
    for wall_cell in grid.cells.row(grid.cells.size - 1):
        grid.maps.add(wall_cell, {"type": "out"})

    center = grid.cells.size // 2

    paddle_origin = Cell(center, grid.cells.size - 1)
    paddle_cells = grid.cells.neighbors(paddle_origin,
                                        kind=HORIZONTAL,
                                        radius=2,
                                        wrap=False) | {paddle_origin}
    for paddle_cell in paddle_cells:
        grid.maps.add(paddle_cell, {"type": "paddle"})

    ball_cell = Cell(center - 2 + random.randrange(5), grid.cells.size - 2)
    grid.maps.add(ball_cell, {"type": "ball",
                              "dx": random.choice([-1, 1]),
                              "dy": -1})


@program.update
def update(grid: Grid) -> None:
    for ball in grid.maps.select(matches={"type": "ball"}):
        dx, dy = ball.get("dx", "dy")
        ball_cell = ball.cell
        next_ball_cell = Cell(ball_cell.x + dx, ball_cell.y + dy)

        if grid.maps.exists(matches={"type": "wall"}, at_cells={next_ball_cell}):
            for wall in grid.maps.select(matches={"type": "wall"}, at_cells={next_ball_cell}):
                new_dx = wall["dx"] if wall.has("dx") else dx
                new_dy = wall["dy"] if wall.has("dy") else dy
                dest = Cell(ball_cell.x + new_dx, ball_cell.y + new_dy)
                grid.maps.move(ball, dest)
                ball.set({"dx": new_dx, "dy": new_dy})
        elif grid.maps.exists(matches={"type": "paddle"},
                           at_cells={Cell(ball_cell.x, next_ball_cell.y)}):
            new_dx = random.choice([-1, 1])
            dest = Cell(ball_cell.x + new_dx, ball_cell.y - 1)
            grid.maps.move(ball, dest)
            ball.set({"dx": new_dx, "dy": -1})
        elif grid.maps.exists(matches={"type": "out"}, at_cells={next_ball_cell}):
            grid.maps.delete(ball)
            grid.maps.add(next_ball_cell, {"type": "ball-out"})
        else:
            grid.maps.move(ball, next_ball_cell)


@program.color
def color(grid: Grid, cell: Cell) -> Color:
    if grid.maps.exists(matches={"type": "wall"}, at_cells={cell}):
        return Color(1.0, 1.0, 1.0)
    if grid.maps.exists(matches={"type": "ball-out"}, at_cells={cell}):
        return Color(1.0, 0.0, 0.0)
    if grid.maps.exists(matches={"type": "ball"}, at_cells={cell}):
        return Color(0.2, 0.9, 0.0)
    if grid.maps.exists(matches={"type": "paddle"}, at_cells={cell}):
        return Color(1.0, 0.8, 0.2)
    return Color(0.0, 0.0, 0.0)


@program.on_click
def on_click(grid: Grid, cell: Cell) -> None:
    direction = "left" if cell.x < grid.cells.size // 2 else "right"
    move_paddle(grid, direction)


@program.on_key
def on_key(grid: Grid, key: str) -> None:
    if key == "left":
        move_paddle(grid, "left")
    if key == "right":
        move_paddle(grid, "right")
    if key == "space":
        grid.maps.clear()
        grid.globals.clear()
        setup(grid)


def move_paddle(grid: Grid, direction: str) -> None:
    dx = -1 if direction == "left" else 1

    paddle_cells = grid.maps.select_cells(matches={"type": "paddle"})
    wall_cells = grid.maps.select_cells(matches={"type": "wall"})

    if not ({cell + Offset(dx, 0) for cell in paddle_cells} & wall_cells):
        for paddle in grid.maps.select(matches={"type": "paddle"}):
            grid.maps.move(paddle, Offset(dx, 0))


if __name__ == "__main__":
    run(program)
