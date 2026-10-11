# Gridcode

A minimal engine for grid-based games and simulations.

## API

| Domain         | Category        | Function                                                        | Usage                                                                |
| -------------- | --------------- | --------------------------------------------------------------- | -------------------------------------------------------------------- |
| **Cells**      | constructors    | `grid.cells.all()`                                              |                                                                      |
|                |                 | `grid.cells.random()`                                           | `random()`                                                           |
|                |                 | `grid.cells.random(count)`                                      | `random(count=5)`                                                    |
|                |                 | `grid.cells.row(y)`                                             | `row(3)`                                                             |
|                |                 | `grid.cells.col(x)`                                             | `col(5)`                                                             |
|                |                 | `grid.cells.rect(x, y, width, height)`                          | `rect(2, 2, 4, 4)`                                                   |
|                |                 | `grid.cells.neighbors(cell, kind=MOORE, radius=1)`              | `neighbors(c)`, `neighbors(c, kind=VON_NEUMANN, radius=2)`           |
|                | filters         | `grid.cells.nearest(candidates, to, count=1)`                   | `nearest({c1, c2}, to=c3, count=2)`                                  |
|                | transformations | `grid.cells.wrap(cell_or_cells)`                                | `wrap(c)`, `wrap({c1, c2})`                                          |
|                |                 | `grid.cells.bounds_of(cells)`                                   | `bounds_of({c1, c2})`                                                |
|                | property        | `grid.cells.size`                                               |                                                                      |
|                | geometry        | `Cell(x, y)`                                                    | `Cell(3, 4)`                                                         |
|                |                 | `Offset(dx, dy)`                                                | `Offset(-1, 0)`                                                      |
|                |                 | `cell + offset`, `-offset`                                      | `c + UP`, `-direction`                                               |
|                |                 | `UP`, `DOWN`, `LEFT`, `RIGHT`                                   |                                                                      |
|                |                 | `MOORE, VON_NEUMANN, HORIZONTAL, VERTICAL`                      |                                                                      |
|                |                 |                                                                 |                                                                      |
| **GlobalMaps** | lifecycle       | `grid.globals.add(name, data)`                                  | `add("game", {"over": False})`                                       |
|                |                 | `grid.globals.delete(name)`                                     | `delete("game")`                                                     |
|                |                 | `grid.globals.clear()`                                          |                                                                      |
|                | queries         | `grid.globals.get(name)`                                        | `get("game")`                                                        |
|                |                 | `grid.globals.exists(name)`                                     | `exists("game")`                                                     |
|                |                 |                                                                 |                                                                      |
| **CellMaps**   | lifecycle       | `grid.maps.add(cell, data)`                                     | `add(c, {"type": "ant", "dx": 1})`                                   |
|                |                 | `grid.maps.copy(map, cell)`                                     | `copy(ant, c)`                                                       |
|                |                 | `grid.maps.delete(map_or_maps)`                                 | `delete(ant)`, `delete(ants)`                                        |
|                |                 | `grid.maps.clear()`                                             |                                                                      |
|                | movement        | `grid.maps.move(map, cell_or_offset)`                           | `move(ant, c)`, `move(ant, UP)`                                      |
|                | queries         | `grid.maps.select(matches=None, has=None, at_cells=None)`       | `select(matches={"type": "ant"}, has={"hungry"}, at_cells={c1, c2})` |
|                |                 | `grid.maps.exists(matches=None, has=None, at_cells=None)`       | `exists(matches={"type": "wall"}, at_cells={c})`                     |
|                |                 | `grid.maps.count(matches=None, has=None, at_cells=None)`        | `count(has={"alive"}, at_cells=cells)`                               |
|                |                 | `grid.maps.select_cells(matches=None, has=None, at_cells=None)` | `select_cells(matches={"type": "snake"})`                            |
|                |                 |                                                                 |                                                                      |
| **Map**        | fields          | `map[key]`                                                      | `ant["dx"]`                                                          |
|                |                 | `map[key] = value`                                              | `ant["dx"] = 1`                                                      |
|                |                 | `map.get(key, key, ...)`                                        | `get("dx", "dy")`                                                    |
|                |                 | `map.set(data)`                                                 | `set({"dx": 1, "dy": -1})`                                           |
|                |                 | `map.delete(key_or_keys)`                                       | `delete("dx")`, `delete({"dx", "dy"})`                               |
|                | queries         | `map.has(key)`                                                  | `has("dx")`                                                          |
|                |                 | `map.matches(data)`                                             | `matches({"type": "ant"})`                                           |
| **CellMap**    | location        | `map.cell`                                                      |                                                                      |
| **GlobalMap**  | location        | `map.name`                                                      |                                                                      |
|                |                 |                                                                 |                                                                      |
| **Color**      |                 | `Color(r, g, b, a=1.0)`                                         | `Color(0.2, 0.9, 0.0)`, `Color(0.2, 0.9, 0.0, 0.5)`                  |
|                |                 | `color.with_opacity(a)`                                         | `with_opacity(0.5)`                                                  |

## Program Structure

```python
#!/usr/bin/env python3

"""Example"""

from gridcode import *


class Example(Program, size=16, frame_rate=8):

    @staticmethod
    def setup(grid: Grid) -> None:
        pass

    @staticmethod
    def update(grid: Grid) -> None:
        pass

    @staticmethod
    def color_for_cell(grid: Grid, cell: Cell) -> Color:
        return Color(1.0, 1.0, 1.0)

    @staticmethod
    def on_key_press(grid: Grid, key: str) -> None:
        pass

    @staticmethod
    def on_cell_click(grid: Grid, cell: Cell) -> None:
        pass


if __name__ == "__main__":
    run(Example)
```
