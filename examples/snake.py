#!/usr/bin/env python3

"""Snake"""

import random

from gridcode import *


program = Program("Snake", size=16, frame_rate=8)


@program.setup
def setup(grid: Grid) -> None:
    center_cell = Cell(grid.cells.size // 2, grid.cells.size // 2)
    grid.data.add(center_cell, {"type": "snake",
                                "id": 0,
                                "head": True})
    snake = grid.data.select(matches={"type": "snake"})
    snake_cells = {map.cell for map in snake}
    food_cell = random.choice(list(grid.cells.all() - snake_cells))
    grid.data.add(food_cell, {"type": "food"})

    direction = random.choice([LEFT, RIGHT, UP, DOWN])
    grid.data.globals.set({"direction": direction,
                           "key_direction": direction,
                           "game_over": False})


@program.update
def update(grid: Grid) -> None:
    grid.data.globals["direction"] = grid.data.globals["key_direction"]

    if grid.data.globals["game_over"]:
        return

    snake = grid.data.select(matches={"type": "snake"})
    head = max(snake, key=lambda m: m["id"])

    target_cell = grid.cells.wrap(head.cell + grid.data.globals["direction"])
    food = grid.data.select(matches={"type": "food"}, at_cells={target_cell})

    head_id = head["id"]
    head.delete("head")

    if food:
        for food_map in food:
            grid.data.delete(food_map)
        snake_cells = {m.cell for m in snake}
        food_cell = random.choice(list(grid.cells.all() - snake_cells - {target_cell}))
        grid.data.add(food_cell, {"type": "food"})
    else:
        grid.data.delete(min(snake, key=lambda m: m["id"]))

    if grid.data.exists(matches={"type": "snake"}, at_cells={target_cell}):
        grid.data.globals["game_over"] = True

    grid.data.add(target_cell,
                  {"type": "snake", "head": True, "id": head_id + 1})


@program.color
def color(grid: Grid, cell: Cell) -> Color:
    if grid.data.exists(at_cells={cell}, matches={"head": True}):
        return Color(0.2, 0.4, 0.6)
    if grid.data.exists(at_cells={cell}, matches={"type": "snake"}):
        return Color(0.2, 0.4, 0.6, 0.5)
    if grid.data.exists(at_cells={cell}, matches={"type": "food"}):
        return Color(0.7, 0.2, 0.2)
    if grid.data.globals["game_over"]:
        return Color(0.7, 0.2, 0.2)
    return Color(0.0, 0.0, 0.0)


@program.on_click
def on_click(grid: Grid, cell: Cell) -> None:
    pass


@program.on_key
def on_key(grid: Grid, key: str) -> None:
    key_direction = {"left": LEFT, "right": RIGHT, "up": UP, "down": DOWN}.get(key)

    if key_direction is not None:
        if key_direction != -grid.data.globals["direction"]:
            grid.data.globals["key_direction"] = key_direction


if __name__ == "__main__":
    run(program)
