"""``gridcode.cells.cells``"""

import random
from dataclasses import dataclass
from enum import StrEnum


@dataclass(frozen=True, slots=True)
class Cell:
    """``Cell``"""

    x: int
    y: int

    def __add__(self, offset: Offset) -> Cell:
        if not isinstance(offset, Offset):
            return NotImplemented
        return Cell(self.x + offset.dx, self.y + offset.dy)

    def __sub__(self, other: Cell | Offset) -> Cell | Offset:
        if isinstance(other, Offset):
            return Cell(self.x - other.dx, self.y - other.dy)
        if isinstance(other, Cell):
            return Offset(self.x - other.x, self.y - other.y)
        return NotImplemented


@dataclass(frozen=True, slots=True)
class Offset:
    """``Offset``"""

    dx: int
    dy: int

    def __add__(self, other: Offset) -> Offset:
        if not isinstance(other, Offset):
            return NotImplemented
        return Offset(self.dx + other.dx, self.dy + other.dy)

    def __sub__(self, other: Offset) -> Offset:
        if not isinstance(other, Offset):
            return NotImplemented
        return Offset(self.dx - other.dx, self.dy - other.dy)

    def __neg__(self) -> Offset:
        return Offset(-self.dx, -self.dy)


Offset.UP    = Offset( 0, -1)
Offset.DOWN  = Offset( 0,  1)
Offset.LEFT  = Offset(-1,  0)
Offset.RIGHT = Offset( 1,  0)


class Neighborhood(StrEnum):
    """``Neighborhood``"""

    MOORE = "moore"
    """``Neighborhood.MOORE``"""

    VON_NEUMANN = "von_neumann"
    """``Neighborhood.VON_NEUMANN``"""

    HORIZONTAL = "horizontal"
    """``Neighborhood.HORIZONTAL``"""

    VERTICAL = "vertical"
    """``Neighborhood.VERTICAL``"""


class CellGrid:
    """``CellGrid``"""

    __slots__ = ("size",)

    def __init__(self, size: int):
        self.size = size

    def all(self) -> set[Cell]:
        """``grid.cells.all()``"""
        return set(self._every_cell())

    def random(self, *, count: int | None = None) -> Cell | set[Cell]:
        """``grid.cells.random()``

        ``grid.cells.random(count)``
        """
        cells = self._every_cell()
        if count is None:
            return random.choice(cells)
        return set(random.sample(cells, count))

    def row(self, y: int) -> set[Cell]:
        """``grid.cells.row(y)``"""
        self._check_index(y)
        return {Cell(x, y) for x in range(self.size)}

    def column(self, x: int) -> set[Cell]:
        """``grid.cells.column(x)``"""
        self._check_index(x)
        return {Cell(x, y) for y in range(self.size)}

    def rect(self, x: int, y: int, width: int, height: int, *,
             wrap: bool) -> set[Cell]:
        """``grid.cells.rect(x, y, width, height, wrap)``"""
        cells = {Cell(x + dx, y + dy)
                 for dy in range(height)
                 for dx in range(width)}
        return self._bounded(cells, wrap)

    def neighbors(self,
                  cell: Cell,
                  *,
                  kind: Neighborhood = Neighborhood.MOORE,
                  radius: int = 1,
                  wrap: bool) -> set[Cell]:
        """``grid.cells.neighbors(cell, kind, radius, wrap)``"""
        cells = {cell + offset for offset in self._offsets(kind, radius)}
        return self._bounded(cells, wrap)

    def nearest(self, candidates: set[Cell], to: Cell, *,
                count: int | None = None) -> Cell | set[Cell]:
        """``grid.cells.nearest(candidates, to)``

        ``grid.cells.nearest(candidates, to, count)``
        """
        ordered = sorted(candidates, key=lambda candidate: self._distance(candidate, to))
        if count is None:
            if not ordered:
                raise ValueError("nearest needs at least one candidate")
            return ordered[0]
        return set(ordered[:count])

    def clip(self, cells: set[Cell]) -> set[Cell]:
        """``grid.cells.clip(cells)``"""
        return {cell for cell in cells if self._contains(cell)}

    def wrap(self, cell_or_cells: Cell | set[Cell]) -> Cell | set[Cell]:
        """``grid.cells.wrap(cell)``

        ``grid.cells.wrap(cells)``
        """
        if isinstance(cell_or_cells, Cell):
            return self._wrapped(cell_or_cells)
        return {self._wrapped(cell) for cell in cell_or_cells}

    def bounds_of(self, cells: set[Cell]) -> set[Cell]:
        """``grid.cells.bounds_of(cells)``"""
        if not cells:
            return set()
        xs = [cell.x for cell in cells]
        ys = [cell.y for cell in cells]
        return {Cell(x, y)
                for y in range(min(ys), max(ys) + 1)
                for x in range(min(xs), max(xs) + 1)}

    def _every_cell(self) -> list[Cell]:
        return [Cell(x, y) for y in range(self.size) for x in range(self.size)]

    def _wrapped(self, cell: Cell) -> Cell:
        return Cell(cell.x % self.size, cell.y % self.size)

    def _contains(self, cell: Cell) -> bool:
        return 0 <= cell.x < self.size and 0 <= cell.y < self.size

    def _bounded(self, cells: set[Cell], wrap: bool) -> set[Cell]:
        if wrap:
            return {self._wrapped(cell) for cell in cells}
        return self.clip(cells)

    def _check_index(self, index: int) -> None:
        if not 0 <= index < self.size:
            raise IndexError(f"{index} is outside the grid")

    def _distance(self, cell: Cell, other: Cell) -> int:
        return (cell.x - other.x) ** 2 + (cell.y - other.y) ** 2

    def _offsets(self, kind: Neighborhood, radius: int) -> set[Offset]:
        span = range(-radius, radius + 1)
        if kind is Neighborhood.HORIZONTAL:
            return {Offset(dx, 0) for dx in span if dx != 0}
        if kind is Neighborhood.VERTICAL:
            return {Offset(0, dy) for dy in span if dy != 0}
        if kind is Neighborhood.VON_NEUMANN:
            return {Offset(dx, dy) for dx in span for dy in span
                    if (dx, dy) != (0, 0) and abs(dx) + abs(dy) <= radius}
        return {Offset(dx, dy) for dx in span for dy in span if (dx, dy) != (0, 0)}


class CellStore[Item]:
    """``CellStore``"""

    __slots__ = ("grid", "items", "cells_by_item")

    def __init__(self, grid: CellGrid):
        self.grid = grid
        self.items: dict[Cell, set[Item]] = {}
        self.cells_by_item: dict[Item, Cell] = {}

    def add(self, cell: Cell, item: Item) -> None:
        """``store.add(cell, item)``"""
        self._check_bounds(cell)
        self.items.setdefault(cell, set()).add(item)
        self.cells_by_item[item] = cell

    def delete(self, item: Item) -> None:
        """``store.delete(item)``"""
        cell = self.cell_of(item)
        items = self.items[cell]
        items.discard(item)
        if not items:
            del self.items[cell]
        del self.cells_by_item[item]

    def move(self, item: Item, cell: Cell) -> None:
        """``store.move(item, cell)``"""
        self._check_bounds(cell)
        self.delete(item)
        self.add(cell, item)

    def items_at(self, cell: Cell) -> set[Item]:
        """``store.items_at(cell)``"""
        return set(self.items.get(cell, ()))

    def cell_of(self, item: Item) -> Cell:
        """``store.cell_of(item)``"""
        cell = self.cells_by_item.get(item)
        if cell is None:
            raise KeyError(f"{item!r} is not in the grid")
        return cell

    def clear(self) -> None:
        """``store.clear()``"""
        self.items.clear()
        self.cells_by_item.clear()

    def _check_bounds(self, cell: Cell) -> None:
        if not self.grid._contains(cell):
            raise IndexError(f"{cell} is outside the grid")
