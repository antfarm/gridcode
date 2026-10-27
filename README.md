# Gridcode

A minimal framework for grid-based games and simulations.

## Installation

Python 3.14 or later and tkinter are required. tkinter is not on PyPI — it ships with Python, but most platforms package it separately.

On macOS:

```sh
brew install python@3.14 python-tk@3.14
```

On Linux:

```sh
apt install python3-tk        # Debian, Ubuntu
dnf install python3-tkinter   # Fedora, RHEL
pacman -S tk                  # Arch
```

Then clone the repository and install Gridcode into a virtual environment:

```sh
git clone https://github.com/antfarm/gridcode.git
cd gridcode
python3 -m venv .venv
source .venv/bin/activate
make install
```

## Running the Examples

The examples are simply executable Python scripts:

```sh
./examples/snake.py
```

## Using Gridcode

To write your own programs with Gridcode, install it from the repository. Here is a typical workflow that creates a virtual environment in a project directory to isolate changes from your system's Python installation:

```sh
mkdir my_project
cd my_project
python3 -m venv .venv
source .venv/bin/activate
pip install git+https://github.com/antfarm/gridcode.git
```

Now you can write your program, e.g. in a file `my_program.py` (`./examples/empty.py` is a good starting point) and execute it :

```sh
chmod +x my_program.py
./my_program.py
```

## Program Structure

A Gridcode program is a `Program` object with five callback functions that are assigned via its decorators: `setup`, `update`, `color`, `on_key` and `on_click`.

A program is executed by calling the `run` function with the instance. During execution, the framework calls the program's callback functions passing the `Grid` instance, which is supposed to be the only mutable state a program keeps.


```python
#!/usr/bin/env python3

"""Example"""

from gridcode import *


program = Program("Example", size=16, frame_rate=2)


@program.setup
def setup(grid: Grid) -> None:
    ...


@program.update
def update(grid: Grid) -> None:
    ...


@program.color
def color(grid: Grid, cell: Cell) -> Color:
    ...


@program.on_click
def on_click(grid: Grid, cell: Cell) -> None:
    ...


@program.on_key
def on_key(grid: Grid, key: str) -> None:
    ...


if __name__ == "__main__":
    run(program)
```

Gridcode programs store data in simple key/value maps that live inside cells on a grid or, in the case of globals, are accessible by name. The use of other data structures is discouraged. This deliberately chosen constraint forces the user to store data directly on the grid, a pattern that is similar to the concept of _stigmergy_ in nature.

Time in Gridcode is discrete and for every tick of the simulated clock, the behavior specified in one of the program's callback functions (`setup`, `update`) is executed. To persist data between ticks, it has to be stored in maps on the grid.

User events like mouse clicks on a displayed cell or key presses are handled asynchronously by the corresponding callback functions (`on_key`, `on_click`).

The color of each cell is determined in every tick by calling `color` for the given cell.

## API Overview

### Program

#### runtime.program.Program

|              | Member             | Type                            | Usage               |
| ------------ | ------------------ | ------------------------------- | ------------------- |
| *Settings*   | `title`            | `str`                           | `Program("Snake")`  |
|              | `size=16`          | `int`                           | `size=32`           |
|              | `frame_rate=8`     | `float`                         | `frame_rate=2`      |
|              | `index=None`       | `list[str] \| ALL`              | `index=["id"]`      |
| *Decorators* | `program.setup`    | `Callable[[Grid], None]`        | `@program.setup`    |
|              | `program.update`   | `Callable[[Grid], None]`        | `@program.update`   |
|              | `program.color`    | `Callable[[Grid, Cell], Color]` | `@program.color`    |
|              | `program.on_click` | `Callable[[Grid, Cell], None]`  | `@program.on_click` |
|              | `program.on_key`   | `Callable[[Grid, str], None]`   | `@program.on_key`   |

#### runtime.color.Color

|                  | Member                  | Type    | Usage                       |
| ---------------- | ----------------------- | ------- | --------------------------- |
| *Construction*   | `Color(r, g, b, a=1.0)` | `Color` | `Color(1.0, 1.0, 1.0, 0.5)` |
| *Transformation* | `color.with_opacity(a)` | `Color` | `color.with_opacity(0.5)`   |

### Grid Components

The `grid` instance that is passed to the program callback functions gives access to cell data (`grid.data`) and global values (`grid.data.globals`). Cells and cell sets can be constructed, transformed or filtered (`grid.cells`).

#### grid.Grid

|            | Member  | Type        | Usage                                      |
| ---------- | ------- | ----------- | ------------------------------------------ |
| *Topology* | `cells` | `CellGrid`  | `grid.cells.all()`                         |
| *Data*     | `data`  | `DataStore` | `grid.data.select(matches={"key": value})` |

### Grid Geometry, Cells and Offsets

#### grid.cells.Cell

|                | Member            | Type     | Usage               |
| -------------- | ----------------- | -------- | ------------------- |
| *Construction* | `Cell(x, y)`      | `Cell`   | `Cell(3, 4)`        |
| *Math*         | `__add__(offset)` | `Cell`   | `cell + UP`         |
|                | `__sub__(offset)` | `Cell`   | `cell - UP`         |
|                | `__sub__(cell)`   | `Offset` | `cell - other_cell` |

#### grid.cells.Offset

|                | Member                        | Type     | Usage           |
| -------------- | ----------------------------- | -------- | --------------- |
| *Construction* | `Offset(dx, dy)`              | `Offset` | `Offset(-1, 0)` |
| *Math*         | `__add__(offset)`             | `Offset` | `UP + LEFT`     |
|                | `__sub__(offset)`             | `Offset` | `UP - LEFT`     |
|                | `__neg__()`                   | `Offset` | `-offset`       |
| *Constants*    | `UP`, `DOWN`, `LEFT`, `RIGHT` | `Offset` | `cell + UP`     |

#### grid.cells.Neighborhood

|             | Member                                           | Type           | Usage                                               |
| ----------- | ------------------------------------------------ | -------------- | --------------------------------------------------- |
| *Constants* | `MOORE`, `VON_NEUMANN`, `HORIZONTAL`, `VERTICAL` | `Neighborhood` | `grid.cells.neighbors(cell, kind=MOORE, wrap=True)` |

#### grid.cells.CellGrid

|                  | Member                                                 | Type        | Raises       | Usage                                                               |
| ---------------- | ------------------------------------------------------ | ----------- | ------------ | ------------------------------------------------------------------- |
| *Construction*   | `cells.all()`                                          | `set[Cell]` |              | `grid.cells.all()`                                                  |
|                  | `cells.random()`                                       | `Cell`      |              | `grid.cells.random()`                                               |
|                  | `cells.random(*, count)`                               | `set[Cell]` | `ValueError` | `grid.cells.random(count=5)`                                        |
|                  | `cells.row(y)`                                         | `set[Cell]` | `IndexError` | `grid.cells.row(3)`                                                 |
|                  | `cells.column(x)`                                      | `set[Cell]` | `IndexError` | `grid.cells.column(5)`                                              |
|                  | `cells.rect(x, y, width, height, *, wrap)`             | `set[Cell]` |              | `grid.cells.rect(0, 0, 8, 8, wrap=False)`                           |
|                  | `cells.neighbors(cell, *, kind=MOORE, radius=1, wrap)` | `set[Cell]` |              | `grid.cells.neighbors(cell, kind=VON_NEUMANN, radius=2, wrap=True)` |
| *Filter*         | `cells.nearest(candidates, to)`                        | `Cell`      | `ValueError` | `grid.cells.nearest({cell1, cell2}, to=cell3)`                      |
|                  | `cells.nearest(candidates, to, *, count)`              | `set[Cell]` | `ValueError` | `grid.cells.nearest({cell1, cell2}, to=cell3, count=2)`             |
|                  | `cells.contains(cell)`                                 | `bool`      |              | `grid.cells.contains(cell)`                                         |
|                  | `cells.clip(cells)`                                    | `set[Cell]` |              | `grid.cells.clip({cell1, cell2})`                                   |
| *Transformation* | `cells.wrap(cell)`                                     | `Cell`      |              | `grid.cells.wrap(cell)`                                             |
|                  | `cells.wrap(cells)`                                    | `set[Cell]` |              | `grid.cells.wrap({cell1, cell2})`                                   |
|                  | `cells.bounds_of(cells)`                               | `set[Cell]` |              | `grid.cells.bounds_of({cell1, cell2})`                              |
| *Property*       | `cells.size`                                           | `int`       |              | `grid.cells.size`                                                   |

### Key/Value Maps

#### grid.data.Value

```python
type Value = bool | int | float | str | Cell | Offset
```

#### grid.data.Map

|            | Member                      | Type                | Raises      | Usage                                       |
| ---------- | --------------------------- | ------------------- | ----------- | ------------------------------------------- |
| *Data*     | `__getitem__(key)`          | `Value`             | `KeyError`  | `map["key"]`                                |
|            | `__setitem__(key, value)`   | `None`              | `TypeError` | `map["key"] = value`                        |
|            | `map.get(key, key, ...)`    | `tuple[Value, ...]` | `KeyError`  | `map.get("key1", "key2")`                   |
|            | `map.set(data)`             | `None`              | `TypeError` | `map.set({"key1": value1, "key2": value2})` |
|            | `map.delete(key, key, ...)` | `None`              | `KeyError`  | `map.delete("key1", "key2")`                |
| *Querying* | `map.has(key, key, ...)`    | `bool`              |             | `map.has("key1", "key2")`                   |
|            | `map.matches(data)`         | `bool`              | `TypeError` | `map.matches({"key": value})`               |

### Maps on the Grid

#### grid.data.CellMap

|            | Member     | Type   | Raises                  | Usage      |
| ---------- | ---------- | ------ | ----------------------- | ---------- |
| *Location* | `map.cell` | `Cell` | `ValueError` `KeyError` | `map.cell` |

#### grid.data.DataStore

|             | Member                                                        | Type           | Raises       | Usage                                                                            |
| ----------- | ------------------------------------------------------------- | -------------- | ------------ | -------------------------------------------------------------------------------- |
| *Lifecycle* | `data.add(cell, data)`                                        | `CellMap`      | `TypeError`  | `grid.data.add(cell, {"key": value})`                                            |
|             | `data.copy(map, cell)`                                        | `CellMap`      | `IndexError` | `grid.data.copy(map, cell)`                                                      |
|             | `data.copy(map, offset)`                                      | `CellMap`      | `IndexError` | `grid.data.copy(map, UP)`                                                        |
|             | `data.delete(map)`                                            | `None`         |              | `grid.data.delete(map)`                                                          |
|             | `data.clear_cells()`                                          | `None`         |              | `grid.data.clear_cells()`                                                        |
|             | `data.clear_globals()`                                        | `None`         |              | `grid.data.clear_globals()`                                                      |
|             | `data.clear()`                                                | `None`         |              | `grid.data.clear()`                                                              |
| *Movement*  | `data.move(map, cell)`                                        | `None`         | `IndexError` | `grid.data.move(map, cell)`                                                      |
|             | `data.move(map, offset)`                                      | `None`         | `IndexError` | `grid.data.move(map, UP)`                                                        |
| *Location*  | `data.cell_of(map)`                                           | `Cell`         | `KeyError`   | `grid.data.cell_of(map)`                                                         |
| *Querying*  | `data.select(*, matches=None, has=None, at_cells=None)`       | `set[CellMap]` | `TypeError`  | `grid.data.select(matches={"key": value}, has={"key"}, at_cells={cell1, cell2})` |
|             | `data.exists(*, matches=None, has=None, at_cells=None)`       | `bool`         | `TypeError`  | `grid.data.exists(matches={"key": value}, at_cells={cell})`                      |
|             | `data.count(*, matches=None, has=None, at_cells=None)`        | `int`          | `TypeError`  | `grid.data.count(has={"key"}, at_cells=cells)`                                   |
|             | `data.select_cells(*, matches=None, has=None, at_cells=None)` | `set[Cell]`    | `TypeError`  | `grid.data.select_cells(matches={"key": value})`                                 |
| *Globals*   | `data.globals`                                                | `Map`          |              | `grid.data.globals["key"] = value`                                               |

### Sets

#### gridcode.sets

|             | Member                | Type   | Raises       | Usage                                            |
| ----------- | --------------------- | ------ | ------------ | ------------------------------------------------ |
| *Reduction* | `only(set)`           | `Item` | `ValueError` | `only(grid.data.select(at_cells={cell}))`        |
|             | `only(set, default)`  | `Item \| None` | `ValueError` | `only(grid.data.select(at_cells={cell}), None)` |

