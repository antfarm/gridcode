# Gridcode

A minimal engine for grid-based games and simulations.

## API

| Domain         | Category        | Function                                                    |
| -------------- | --------------- | ----------------------------------------------------------- |
| **Cells**      | constructors    | `grid.cells.all()`                                          |
|                |                 | `grid.cells.random()`                                       |
|                |                 | `grid.cells.random(count)`                                  |
|                |                 | `grid.cells.row(y)`                                         |
|                |                 | `grid.cells.col(x)`                                         |
|                |                 | `grid.cells.rect(x, y, width, height)`                      |
|                |                 | `grid.cells.neighbors(cell, kind=MOORE, radius=1)`          |
|                | filters         | `grid.cells.nearest(candidates, to, count=1)`               |
|                | transformations | `grid.cells.wrap(cell_or_cells)`                            |
|                |                 | `grid.cells.bounds_of(cells)`                               |
|                | property        | `grid.cells.size`                                           |
|                | geometry        | `Cell(x, y)`                                                |
|                |                 | `Offset(dx, dy)`                                            |
|                |                 | `cell + offset`, `-offset`                                  |
|                |                 | `UP`, `DOWN`, `LEFT`, `RIGHT`                               |
|                |                 | `MOORE, VON_NEUMANN, HORIZONTAL, VERTICAL`                  |
|                |                 |                                                             |
| **GlobalMaps** | lifecycle       | `grid.globals.add(name, data)`                              |
|                |                 | `grid.globals.delete(name)`                                 |
|                |                 | `grid.globals.clear()`                                      |
|                | queries         | `grid.globals.get(name)`                                    |
|                |                 | `grid.globals.exists(name)`                                 |
|                |                 |                                                             |
| **CellMaps**   | lifecycle       | `grid.maps.add(cell, data)`                                 |
|                |                 | `grid.maps.copy(map, cell)`                                 |
|                |                 | `grid.maps.delete(map_or_maps)`                             |
|                |                 | `grid.maps.clear()`                                         |
|                | movement        | `grid.maps.move(map, cell_or_offset)`                       |
|                | queries         | `grid.maps.select(matches=None, has=None, at_cells=None)`   |
|                |                 | `grid.maps.exists(matches=None, has=None, at_cells=None)`   |
|                |                 | `grid.maps.count(matches=None, has=None, at_cells=None)`    |
|                |                 | `grid.maps.select_cells(matches=None, has=None, at_cells=None)` |
|                |                 |                                                             |
| **Map**        | fields          | `map[key]`                                                  |
|                |                 | `map[key] = value`                                          |
|                |                 | `map.get(key, key, ...)`                                    |
|                |                 | `map.set(data)`                                             |
|                |                 | `map.delete(key_or_keys)`                                   |
|                | queries         | `map.has(key)`                                              |
|                |                 | `map.matches(data)`                                         |
| **CellMap**    | location        | `map.cell`                                                  |
| **GlobalMap**  | location        | `map.name`                                                  |
|                |                 |                                                             |
| **Color**      |                 | `Color(r, g, b, a=1.0)`                                     |
|                |                 | `color.with_opacity(a)`                                     |

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
