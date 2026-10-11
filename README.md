# Gridcode

A minimal engine for grid-based games and simulations.

## API

| Category        | Function                                              | Usage                                                                            | Returns             |
| --------------- | ----------------------------------------------------- | -------------------------------------------------------------------------------- | ------------------- |
| **Geometry**    |                                                       |                                                                                  |                     |
|                 | `Cell(x, y)`                                          | `Cell(3, 4)`                                                                     | `Cell`              |
|                 | `Offset(dx, dy)`                                      | `Offset(-1, 0)`                                                                  | `Offset`            |
|                 | `cell + offset`                                       | `cell + UP`                                                                      | `Cell`              |
|                 | `-offset`                                             | `-offset`                                                                        | `Offset`            |
|                 | `UP`, `DOWN`, `LEFT`, `RIGHT`                         |                                                                                  | `Offset`            |
|                 | `MOORE`, `VON_NEUMANN`, `HORIZONTAL`, `VERTICAL`      |                                                                                  | `Neighborhood`      |
|                 |                                                       |                                                                                  |                     |
| **Cells**       |                                                       |                                                                                  |                     |
| constructors    | `grid.cells.all()`                                    |                                                                                  | `set[Cell]`         |
|                 | `grid.cells.random()`                                 | `grid.cells.random()`                                                            | `Cell`              |
|                 | `grid.cells.random(*, count)`                         | `grid.cells.random(count=5)`                                                     | `set[Cell]`         |
|                 | `grid.cells.row(y)`                                   | `grid.cells.row(3)`                                                              | `set[Cell]`         |
|                 | `grid.cells.col(x)`                                   | `grid.cells.col(5)`                                                              | `set[Cell]`         |
|                 | `grid.cells.rect(x, y, width, height)`                | `grid.cells.rect(0, 0, 8, 8)`                                                    | `set[Cell]`         |
|                 | `grid.cells.neighbors(cell, *, kind=MOORE, radius=1)` | `grid.cells.neighbors(cell, kind=VON_NEUMANN, radius=2)`                         | `set[Cell]`         |
| filters         | `grid.cells.nearest(candidates, to)`                  | `grid.cells.nearest({cell1, cell2}, to=cell3)`                                   | `Cell`              |
|                 | `grid.cells.nearest(candidates, to, *, count)`        | `grid.cells.nearest({cell1, cell2}, to=cell3, count=2)`                          | `set[Cell]`         |
| transformations | `grid.cells.wrap(cell)`                               | `grid.cells.wrap(cell)`                                                          | `Cell`              |
|                 | `grid.cells.wrap(cells)`                              | `grid.cells.wrap({cell1, cell2})`                                                | `set[Cell]`         |
|                 | `grid.cells.bounds_of(cells)`                         | `grid.cells.bounds_of({cell1, cell2})`                                           | `set[Cell]`         |
| property        | `grid.cells.size`                                     |                                                                                  | `int`               |
|                 |                                                       |                                                                                  |                     |
| **GlobalMaps**  |                                                       |                                                                                  |                     |
| lifecycle       | `grid.globals.add(name, data)`                        | `grid.globals.add("name", {"key": value})`                                       | `GlobalMap`         |
|                 | `grid.globals.delete(name)`                           | `grid.globals.delete("name")`                                                    | `None`              |
|                 | `grid.globals.clear()`                                |                                                                                  | `None`              |
| queries         | `grid.globals.get(name)`                              | `grid.globals.get("name")`                                                       | `GlobalMap \| None` |
|                 | `grid.globals.exists(name)`                           | `grid.globals.exists("name")`                                                    | `bool`              |
|                 |                                                       |                                                                                  |                     |
| **CellMaps**    |                                                       |                                                                                  |                     |
| lifecycle       | `grid.maps.add(cell, data)`                           | `grid.maps.add(cell, {"key": value})`                                            | `CellMap`           |
|                 | `grid.maps.copy(map, cell)`                           | `grid.maps.copy(map, cell)`                                                      | `CellMap`           |
|                 | `grid.maps.delete(map)`                               | `grid.maps.delete(map)`                                                          | `None`              |
|                 | `grid.maps.clear()`                                   |                                                                                  | `None`              |
| movement        | `grid.maps.move(map, cell)`                           | `grid.maps.move(map, cell)`                                                      | `None`              |
|                 | `grid.maps.move(map, offset)`                         | `grid.maps.move(map, UP)`                                                        | `None`              |
| queries         | `grid.maps.select(*, matches, has, at_cells)`         | `grid.maps.select(matches={"key": value}, has={"key"}, at_cells={cell1, cell2})` | `set[CellMap]`      |
|                 | `grid.maps.exists(*, matches, has, at_cells)`         | `grid.maps.exists(matches={"key": value}, at_cells={cell})`                      | `bool`              |
|                 | `grid.maps.count(*, matches, has, at_cells)`          | `grid.maps.count(has={"key"}, at_cells=cells)`                                   | `int`               |
|                 | `grid.maps.select_cells(*, matches, has, at_cells)`   | `grid.maps.select_cells(matches={"key": value})`                                 | `set[Cell]`         |
|                 |                                                       |                                                                                  |                     |
| **Map**         |                                                       |                                                                                  |                     |
| fields          | `map[key]`                                            | `map["key"]`                                                                     | `Value`             |
|                 | `map[key] = value`                                    | `map["key"] = value`                                                             | `None`              |
|                 | `map.get(key, key, ...)`                              | `map.get("key1", "key2")`                                                        | `tuple[Value, ...]` |
|                 | `map.set(data)`                                       | `map.set({"key1": value1, "key2": value2})`                                      | `None`              |
|                 | `map.delete(key, key, ...)`                           | `map.delete("key1", "key2")`                                                     | `None`              |
| queries         | `map.has(key, key, ...)`                              | `map.has("key1", "key2")`                                                        | `bool`              |
|                 | `map.matches(data)`                                   | `map.matches({"key": value})`                                                    | `bool`              |
|                 |                                                       |                                                                                  |                     |
| **CellMap**     |                                                       |                                                                                  |                     |
| location        | `map.cell`                                            | `map.cell`                                                                       | `Cell`              |
|                 |                                                       |                                                                                  |                     |
| **GlobalMap**   |                                                       |                                                                                  |                     |
| location        | `map.name`                                            | `map.name`                                                                       | `str`               |
|                 |                                                       |                                                                                  |                     |
| **Color**       |                                                       |                                                                                  |                     |
|                 | `Color(r, g, b, a=1.0)`                               | `Color(1.0, 1.0, 1.0, 0.5)`                                                      | `Color`             |
|                 | `color.with_opacity(a)`                               | `color.with_opacity(0.5)`                                                        | `Color`             |

`Value` is `bool | int | float | str | Cell | Offset`.

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
