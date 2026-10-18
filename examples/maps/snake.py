#!/usr/bin/env python3

"""Snake"""

import random

from gridcode import *
from gridcode.data.maps import MapsData


class Snake(Program, data_class=MapsData, size=16, frame_rate=8):

    @staticmethod
    def setup(grid: Grid[MapsData]) -> None:
        center_cell = Cell(grid.cells.size // 2, grid.cells.size // 2)
        grid.data.maps.add(center_cell, {"type": "snake",
                                    "id": 0,
                                    "head": True})

        snake_cells = grid.data.maps.select_cells(matches={"type": "snake"})
        food_cell = random.choice(list(grid.cells.all() - snake_cells))
        grid.data.maps.add(food_cell, {"type": "food"})

        direction = random.choice([LEFT, RIGHT, UP, DOWN])
        grid.data.globals.add("game", {"direction": direction,
                                  "key_direction": direction,
                                  "over": False})

    @staticmethod
    def update(grid: Grid[MapsData]) -> None:
        game = grid.data.globals.get("game")
        game["direction"] = game["key_direction"]

        if game["over"]:
            return

        snake = grid.data.maps.select(matches={"type": "snake"})
        head = max(snake, key=lambda m: m["id"])

        target_cell = grid.cells.wrap(head.cell + game["direction"])
        food = grid.data.maps.select(matches={"type": "food"}, at_cells={target_cell})

        if food:
            for food_map in food:
                grid.data.maps.delete(food_map)
            snake_cells = {m.cell for m in snake}
            food_cell = random.choice(list(grid.cells.all() - snake_cells - {target_cell}))
            grid.data.maps.add(food_cell, {"type": "food"})
        else:
            grid.data.maps.delete(min(snake, key=lambda m: m["id"]))

        if grid.data.maps.exists(matches={"type": "snake"}, at_cells={target_cell}):
            game["over"] = True

        head.delete("head")

        grid.data.maps.add(target_cell,
                      {"type": "snake", "head": True, "id": head["id"] + 1})

    @staticmethod
    def color_for_cell(grid: Grid[MapsData], cell: Cell) -> Color:
        if grid.data.maps.exists(at_cells={cell}, matches={"head": True}):
            return Color(0.2, 0.4, 0.6)
        if grid.data.maps.exists(at_cells={cell}, matches={"type": "snake"}):
            return Color(0.2, 0.4, 0.6, 0.5)
        if grid.data.maps.exists(at_cells={cell}, matches={"type": "food"}):
            return Color(0.7, 0.2, 0.2)
        if grid.data.globals.get("game")["over"]:
            return Color(0.7, 0.2, 0.2)
        return Color(0.0, 0.0, 0.0)

    @staticmethod
    def on_cell_click(grid: Grid[MapsData], cell: Cell) -> None:
        pass

    @staticmethod
    def on_key_press(grid: Grid[MapsData], key: str) -> None:
        key_direction = {"left": LEFT, "right": RIGHT, "up": UP, "down": DOWN}.get(key)

        if key_direction is not None:
            game = grid.data.globals.get("game")
            if key_direction != -game["direction"]:
                game["key_direction"] = key_direction


if __name__ == "__main__":
    run(Snake)
