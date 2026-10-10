#!/usr/bin/env python3

"""Snake"""

import random

from gridcode import *


class Snake(Program, size=16, frame_rate=8):

    @staticmethod
    def setup(grid: Grid) -> None:
        center_cell = Cell(grid.size // 2, grid.size // 2)
        grid.add(center_cell, {"type": "snake",
                               "id": 0,
                               "head": True})

        snake_cells = {m.cell for m in grid.select(data={"type": "snake"})}
        food_cell = random.choice(list(grid.cells() - snake_cells))
        grid.add(food_cell, {"type": "food"})

        direction = random.choice([LEFT, RIGHT, UP, DOWN])
        grid.add("game", {"direction": direction,
                          "key_direction": direction,
                          "over": False})

    @staticmethod
    def update(grid: Grid) -> None:
        game = grid.get("game")
        game["direction"] = game["key_direction"]

        if game["over"]:
            return

        snake = grid.select(data={"type": "snake"})
        head = max(snake, key=lambda m: m["id"])

        target_cell = grid.wrap(head.cell + game["direction"])
        food = grid.select(data={"type": "food"}, cells=[target_cell])

        if food:
            grid.delete(food)
            snake_cells = {m.cell for m in snake}
            food_cell = random.choice(list(grid.cells() - snake_cells - {target_cell}))
            grid.add(food_cell, {"type": "food"})
        else:
            grid.delete(min(snake, key=lambda m: m["id"]))

        if grid.exists(data={"type": "snake"}, cells=[target_cell]):
            game["over"] = True

        head.delete("head")

        grid.add(target_cell,
                 {"type": "snake", "head": True, "id": head["id"] + 1})

    @staticmethod
    def color_for_cell(cell: Cell, grid: Grid) -> Color:
        if grid.exists(cells=[cell], data={"head": True}):
            return Color(0.2, 0.4, 0.6)
        if grid.exists(cells=[cell], data={"type": "snake"}):
            return Color(0.2, 0.4, 0.6, 0.5)
        if grid.exists(cells=[cell], data={"type": "food"}):
            return Color(0.7, 0.2, 0.2)
        if grid.get("game")["over"]:
            return Color(0.7, 0.2, 0.2)
        return Color(0.0, 0.0, 0.0)

    @staticmethod
    def on_key_press(key: str, grid: Grid) -> None:
        key_direction = {"left": LEFT, "right": RIGHT, "up": UP, "down": DOWN}.get(key)

        if key_direction is not None:
            game = grid.get("game")
            if key_direction != -game["direction"]:
                game["key_direction"] = key_direction

        if key == "space":
            grid.clear()
            Snake.setup(grid)

    @staticmethod
    def on_cell_click(cell: Cell, grid: Grid) -> None:
        pass


if __name__ == "__main__":
    run(Snake)
