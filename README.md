# Gridcode

A minimal engine for grid-based games and simulations.

## Program Structure

A Gridcode program is a subclass of `Program` that implements five static callback methods: `setup`, `update`, `color_for_cell`, `on_key_press` and `on_cell_click`. Each of these methods gets called by the engine with the `grid` instance passed as an argument.

A program is executed by calling the `run` function with its class.

```python
#!/usr/bin/env python3

"""Example"""

from gridcode import *

class Example(Program, size=16, frame_rate=2):

    @staticmethod
    def setup(grid: Grid) -> None:
        ...

    @staticmethod
    def update(grid: Grid) -> None:
        ...

    @staticmethod
    def color_for_cell(grid: Grid, cell: Cell) -> Color:
        ...

    @staticmethod
    def on_key_press(grid: Grid, key: str) -> None:
        ...

    @staticmethod
    def on_cell_click(grid: Grid, cell: Cell) -> None:
        ...


if __name__ == "__main__":
    run(Example)
```

Gridcode programs store data in simple key/value maps that live inside cells on a grid or, in the case of globals, are accessible by name. The use of other data structures is discouraged. This deliberately chosen constraint forces the user to store data directly on the grid, a pattern that is similiar to the concept of _stygmergy_ in nature.

Time in Gridcode is discrete and for every tick of the simulated clock, the behavior specified in one of the program's callback functions (`setup`, `update`) is executed. To persist data between ticks, it has to be stored in maps on the grid.

User events like mouse clicks on a displayed cell or key presses are handled asynchronously by the corresponding callback functions (`on_key_press`, `on_cell_click`).

The color of each cell is determined in every tick by calling `color_for_cell` for the given cell.

## API Overview

### Grid Components

The `grid` instance that is passed to the program callback functions gives acces to cell data and global data stored in maps via its `maps`and `globals` members.

Cells and cell sets can be constructed, transformed or filtered vusing the `cells` member.

#### grid.Grid

|               | Member    | Type             | Raises | Usage                                      |
| ------------- | --------- | ---------------- | ------ | ------------------------------------------ |
| *Topology*    | `cells`   | `Cells`          |        | `grid.cells.all()`                         |
| *Cell data*   | `maps`    | `CellMapStore`   |        | `grid.maps.select(matches={"key": value})` |
| *Global data* | `globals` | `GlobalMapStore` |        | `grid.globals.get("name")`                 |

### Cells & Offsets

#### grid.cells.Cell

|                  | Member            | Type   | Raises | Usage        |
| ---------------- | ----------------- | ------ | ------ | ------------ |
| *Construction*   | `Cell(x, y)`      | `Cell` |        | `Cell(3, 4)` |
| *Transformation* | `__add__(offset)` | `Cell` |        | `cell + UP`  |

#### grid.cells.Offset

|                  | Member                        | Type     | Raises | Usage           |
| ---------------- | ----------------------------- | -------- | ------ | --------------- |
| *Construction*   | `Offset(dx, dy)`              | `Offset` |        | `Offset(-1, 0)` |
| *Transformation* | `__neg__()`                   | `Offset` |        | `-offset`       |
| *Constants*      | `UP`, `DOWN`, `LEFT`, `RIGHT` | `Offset` |        | `cell + UP`     |

#### grid.cells.Neighborhood

|             | Member                                           | Type           | Raises | Usage                                    |
| ----------- | ------------------------------------------------ | -------------- | ------ | ---------------------------------------- |
| *Constants* | `MOORE`, `VON_NEUMANN`, `HORIZONTAL`, `VERTICAL` | `Neighborhood` |        | `grid.cells.neighbors(cell, kind=MOORE)` |

#### grid.cells.Cells

|                  | Member                                           | Type        | Raises | Usage                                                    |
| ---------------- | ------------------------------------------------ | ----------- | ------ | -------------------------------------------------------- |
| *Construction*   | `cells.all()`                                    | `set[Cell]` |        | `grid.cells.all()`                                       |
|                  | `cells.random()`                                 | `Cell`      |        | `grid.cells.random()`                                    |
|                  | `cells.random(*, count)`                         | `set[Cell]` |        | `grid.cells.random(count=5)`                             |
|                  | `cells.row(y)`                                   | `set[Cell]` |        | `grid.cells.row(3)`                                      |
|                  | `cells.col(x)`                                   | `set[Cell]` |        | `grid.cells.col(5)`                                      |
|                  | `cells.rect(x, y, width, height)`                | `set[Cell]` |        | `grid.cells.rect(0, 0, 8, 8)`                            |
|                  | `cells.neighbors(cell, *, kind=MOORE, radius=1)` | `set[Cell]` |        | `grid.cells.neighbors(cell, kind=VON_NEUMANN, radius=2)` |
| *Filter*         | `cells.nearest(candidates, to)`                  | `Cell`      |        | `grid.cells.nearest({cell1, cell2}, to=cell3)`           |
|                  | `cells.nearest(candidates, to, *, count)`        | `set[Cell]` |        | `grid.cells.nearest({cell1, cell2}, to=cell3, count=2)`  |
|                  | `cells.clip(cells)`                              | `set[Cell]` |                | `grid.cells.clip({cell1, cell2})`                        |
| *Transformation* | `cells.wrap(cell)`                               | `Cell`      |        | `grid.cells.wrap(cell)`                                  |
|                  | `cells.wrap(cells)`                              | `set[Cell]` |        | `grid.cells.wrap({cell1, cell2})`                        |
|                  | `cells.bounds_of(cells)`                         | `set[Cell]` |        | `grid.cells.bounds_of({cell1, cell2})`                   |
| *Property*       | `cells.size`                                     | `int`       |        | `grid.cells.size`                                        |

### Maps & Data

#### grid.maps.Map

|            | Member                      | Type                | Raises      | Usage                                       |
| ---------- | --------------------------- | ------------------- | ----------- | ------------------------------------------- |
| *Data*     | `__getitem__(key)`          | `Value`             | `KeyError`  | `map["key"]`                                |
|            | `__setitem__(key, value)`   | `None`              | `TypeError` | `map["key"] = value`                        |
|            | `map.get(key, key, ...)`    | `tuple[Value, ...]` | `KeyError`  | `map.get("key1", "key2")`                   |
|            | `map.set(data)`             | `None`              | `TypeError` | `map.set({"key1": value1, "key2": value2})` |
|            | `map.delete(key, key, ...)` | `None`              |             | `map.delete("key1", "key2")`                |
| *Querying* | `map.has(key, key, ...)`    | `bool`              |             | `map.has("key1", "key2")`                   |
|            | `map.matches(data)`         | `bool`              |             | `map.matches({"key": value})`               |

#### grid.maps.CellMap

|            | Member     | Type   | Raises | Usage      |
| ---------- | ---------- | ------ | ------ | ---------- |
| *Location* | `map.cell` | `Cell` |        | `map.cell` |

#### grid.maps.GlobalMap

|            | Member     | Type  | Raises | Usage      |
| ---------- | ---------- | ----- | ------ | ---------- |
| *Location* | `map.name` | `str` |        | `map.name` |

### Map Stores

#### grid.maps.CellMapStore

|             | Member                                         | Type           | Raises      | Usage                                                                            |
| ----------- | ---------------------------------------------- | -------------- | ----------- | -------------------------------------------------------------------------------- |
| *Lifecycle* | `maps.add(cell, data)`                         | `CellMap`      | `TypeError` | `grid.maps.add(cell, {"key": value})`                                            |
|             | `maps.copy(map, cell)`                         | `CellMap`      |             | `grid.maps.copy(map, cell)`                                                      |
|             | `maps.copy(map, offset)`                       | `CellMap`      |             | `grid.maps.copy(map, UP)`                                                        |
|             | `maps.delete(map)`                             | `None`         |             | `grid.maps.delete(map)`                                                          |
|             | `maps.clear()`                                 | `None`         |             | `grid.maps.clear()`                                                              |
| *Movement*  | `maps.move(map, cell)`                         | `None`         |             | `grid.maps.move(map, cell)`                                                      |
|             | `maps.move(map, offset)`                       | `None`         |             | `grid.maps.move(map, UP)`                                                        |
| *Querying*  | `maps.select(*, matches, has, at_cells)`       | `set[CellMap]` |             | `grid.maps.select(matches={"key": value}, has={"key"}, at_cells={cell1, cell2})` |
|             | `maps.exists(*, matches, has, at_cells)`       | `bool`         |             | `grid.maps.exists(matches={"key": value}, at_cells={cell})`                      |
|             | `maps.count(*, matches, has, at_cells)`        | `int`          |             | `grid.maps.count(has={"key"}, at_cells=cells)`                                   |
|             | `maps.select_cells(*, matches, has, at_cells)` | `set[Cell]`    |             | `grid.maps.select_cells(matches={"key": value})`                                 |

#### grid.maps.GlobalMapStore

|             | Member                    | Type        | Raises      | Usage                                      |
| ----------- | ------------------------- | ----------- | ----------- | ------------------------------------------ |
| *Lifecycle* | `globals.add(name, data)` | `GlobalMap` | `TypeError` | `grid.globals.add("name", {"key": value})` |
|             | `globals.delete(name)`    | `None`      |             | `grid.globals.delete("name")`              |
|             | `globals.clear()`         | `None`      |             | `grid.globals.clear()`                     |
| *Querying*  | `globals.get(name)`       | `GlobalMap` | `KeyError`  | `grid.globals.get("name")`                 |
|             | `globals.exists(name)`    | `bool`      |             | `grid.globals.exists("name")`              |

### Display

#### display.color.Color

|                  | Member                  | Type    | Raises | Usage                       |
| ---------------- | ----------------------- | ------- | ------ | --------------------------- |
| *Construction*   | `Color(r, g, b, a=1.0)` | `Color` |        | `Color(1.0, 1.0, 1.0, 0.5)` |
| *Transformation* | `color.with_opacity(a)` | `Color` |        | `color.with_opacity(0.5)`   |
