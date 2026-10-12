# Gridcode

A minimal engine for grid-based games and simulations.

## API Overview

### Grid

| Class                  | Member    | Type             | Raises | Usage                                      |
| ---------------------- | --------- | ---------------- | ------ | ------------------------------------------ |
| **grid.Grid**          |           |                  |        |                                            |
| <sub>Topology</sub>    | `cells`   | `Cells`          |        | `grid.cells.all()`                         |
| <sub>Cell data</sub>   | `maps`    | `CellMaps`   |        | `grid.maps.select(matches={"key": value})` |
| <sub>Global data</sub> | `globals` | `GlobalMaps` |        | `grid.globals.get("name")`                 |

### Topology

| Class                       | Member                                           | Type           | Raises | Usage                                                    |
| --------------------------- | ------------------------------------------------ | -------------- | ------ | -------------------------------------------------------- |
| **grid.cells.Cell**         |                                                  |                |        |                                                          |
| <sub>Construction</sub>     | `Cell(x, y)`                                     | `Cell`         |        | `Cell(3, 4)`                                             |
| <sub>Transformation</sub>   | `__add__(offset)`                                | `Cell`         |        | `cell + UP`                                              |
|                             |                                                  |                |        |                                                          |
| **grid.cells.Offset**       |                                                  |                |        |                                                          |
| <sub>Construction</sub>     | `Offset(dx, dy)`                                 | `Offset`       |        | `Offset(-1, 0)`                                          |
| <sub>Transformation</sub>   | `__neg__()`                                      | `Offset`       |        | `-offset`                                                |
| <sub>Constants</sub>        | `UP`, `DOWN`, `LEFT`, `RIGHT`                    | `Offset`       |        |                                                          |
|                             |                                                  |                |        |                                                          |
| **grid.cells.Neighborhood** |                                                  |                |        |                                                          |
| <sub>Constants</sub>        | `MOORE`, `VON_NEUMANN`, `HORIZONTAL`, `VERTICAL` | `Neighborhood` |        |                                                          |
|                             |                                                  |                |        |                                                          |
| **grid.cells.Cells**        |                                                  |                |        |                                                          |
| <sub>Construction</sub>     | `cells.all()`                                    | `set[Cell]`    |        |                                                          |
|                             | `cells.random()`                                 | `Cell`         |        | `grid.cells.random()`                                    |
|                             | `cells.random(*, count)`                         | `set[Cell]`    |        | `grid.cells.random(count=5)`                             |
|                             | `cells.row(y)`                                   | `set[Cell]`    |        | `grid.cells.row(3)`                                      |
|                             | `cells.col(x)`                                   | `set[Cell]`    |        | `grid.cells.col(5)`                                      |
|                             | `cells.rect(x, y, width, height)`                | `set[Cell]`    |        | `grid.cells.rect(0, 0, 8, 8)`                            |
|                             | `cells.neighbors(cell, *, kind=MOORE, radius=1)` | `set[Cell]`    |        | `grid.cells.neighbors(cell, kind=VON_NEUMANN, radius=2)` |
| <sub>Filter</sub>           | `cells.nearest(candidates, to)`                  | `Cell`         |        | `grid.cells.nearest({cell1, cell2}, to=cell3)`           |
|                             | `cells.nearest(candidates, to, *, count)`        | `set[Cell]`    |        | `grid.cells.nearest({cell1, cell2}, to=cell3, count=2)`  |
| <sub>Transformation</sub>   | `cells.wrap(cell)`                               | `Cell`         |        | `grid.cells.wrap(cell)`                                  |
|                             | `cells.wrap(cells)`                              | `set[Cell]`    |        | `grid.cells.wrap({cell1, cell2})`                        |
|                             | `cells.bounds_of(cells)`                         | `set[Cell]`    |        | `grid.cells.bounds_of({cell1, cell2})`                   |
| <sub>Property</sub>         | `cells.size`                                     | `int`          |        |                                                          |

### Data in maps

| Class                   | Member                      | Type                | Raises      | Usage                                       |
| ----------------------- | --------------------------- | ------------------- | ----------- | ------------------------------------------- |
| **grid.maps.Map**       |                             |                     |             |                                             |
| <sub>Data</sub>         | `__getitem__(key)`          | `Value`             | `KeyError`  | `map["key"]`                                |
|                         | `__setitem__(key, value)`   | `None`              | `TypeError` | `map["key"] = value`                        |
|                         | `map.get(key, key, ...)`    | `tuple[Value, ...]` | `KeyError`  | `map.get("key1", "key2")`                   |
|                         | `map.set(data)`             | `None`              | `TypeError` | `map.set({"key1": value1, "key2": value2})` |
|                         | `map.delete(key, key, ...)` | `None`              |             | `map.delete("key1", "key2")`                |
| <sub>Querying</sub>     | `map.has(key, key, ...)`    | `bool`              |             | `map.has("key1", "key2")`                   |
|                         | `map.matches(data)`         | `bool`              |             | `map.matches({"key": value})`               |
|                         |                             |                     |             |                                             |
| **grid.maps.CellMap**   |                             |                     |             |                                             |
| <sub>Location</sub>     | `map.cell`                  | `Cell`              |             | `map.cell`                                  |
|                         |                             |                     |             |                                             |
| **grid.maps.GlobalMap** |                             |                     |             |                                             |
| <sub>Location</sub>     | `map.name`                  | `str`               |             | `map.name`                                  |

### Map stores

| Class                        | Member                                         | Type           | Raises      | Usage                                                                            |
| ---------------------------- | ---------------------------------------------- | -------------- | ----------- | -------------------------------------------------------------------------------- |
| **grid.maps.CellMaps**   |                                                |                |             |                                                                                  |
| <sub>Lifecycle</sub>         | `maps.add(cell, data)`                         | `CellMap`      | `TypeError` | `grid.maps.add(cell, {"key": value})`                                            |
|                              | `maps.copy(map, cell)`                         | `CellMap`      |             | `grid.maps.copy(map, cell)`                                                      |
|                              | `maps.copy(map, offset)`                       | `CellMap`      |             | `grid.maps.copy(map, UP)`                                                        |
|                              | `maps.delete(map)`                             | `None`         |             | `grid.maps.delete(map)`                                                          |
|                              | `maps.clear()`                                 | `None`         |             |                                                                                  |
| <sub>Movement</sub>          | `maps.move(map, cell)`                         | `None`         |             | `grid.maps.move(map, cell)`                                                      |
|                              | `maps.move(map, offset)`                       | `None`         |             | `grid.maps.move(map, UP)`                                                        |
| <sub>Querying</sub>          | `maps.select(*, matches, has, at_cells)`       | `set[CellMap]` |             | `grid.maps.select(matches={"key": value}, has={"key"}, at_cells={cell1, cell2})` |
|                              | `maps.exists(*, matches, has, at_cells)`       | `bool`         |             | `grid.maps.exists(matches={"key": value}, at_cells={cell})`                      |
|                              | `maps.count(*, matches, has, at_cells)`        | `int`          |             | `grid.maps.count(has={"key"}, at_cells=cells)`                                   |
|                              | `maps.select_cells(*, matches, has, at_cells)` | `set[Cell]`    |             | `grid.maps.select_cells(matches={"key": value})`                                 |
|                              |                                                |                |             |                                                                                  |
| **grid.maps.GlobalMaps** |                                                |                |             |                                                                                  |
| <sub>Lifecycle</sub>         | `globals.add(name, data)`                      | `GlobalMap`    | `TypeError` | `grid.globals.add("name", {"key": value})`                                       |
|                              | `globals.delete(name)`                         | `None`         |             | `grid.globals.delete("name")`                                                    |
|                              | `globals.clear()`                              | `None`         |             |                                                                                  |
| <sub>Querying</sub>          | `globals.get(name)`                            | `GlobalMap`    | `KeyError`  | `grid.globals.get("name")`                                                       |
|                              | `globals.exists(name)`                         | `bool`         |             | `grid.globals.exists("name")`                                                    |

### Display

| Class                     | Member                  | Type    | Raises | Usage                       |
| ------------------------- | ----------------------- | ------- | ------ | --------------------------- |
| **display.color.Color**   |                         |         |        |                             |
| <sub>Construction</sub>   | `Color(r, g, b, a=1.0)` | `Color` |        | `Color(1.0, 1.0, 1.0, 0.5)` |
| <sub>Transformation</sub> | `color.with_opacity(a)` | `Color` |        | `color.with_opacity(0.5)`   |

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
