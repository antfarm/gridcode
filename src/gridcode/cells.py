"""``gridcode.cells``"""

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


class Cells:
    """``Cells``"""

    __slots__ = ("size",)

    def __init__(self, size: int):
        self.size = size

    def all(self) -> set[Cell]:
        """``grid.cells.all()``"""
        raise NotImplementedError

    def random(self, *, count: int | None = None) -> Cell | set[Cell]:
        """``grid.cells.random()``

        ``grid.cells.random(count)``
        """
        raise NotImplementedError

    def wrap(self, cell_or_cells: Cell | set[Cell]) -> Cell | set[Cell]:
        """``grid.cells.wrap(cell)``

        ``grid.cells.wrap(cells)``
        """
        raise NotImplementedError

    def nearest(self, candidates: set[Cell], to: Cell, *,
                count: int | None = None) -> Cell | set[Cell]:
        """``grid.cells.nearest(candidates, to)``

        ``grid.cells.nearest(candidates, to, count)``
        """
        raise NotImplementedError

    def clip(self, cells: set[Cell]) -> set[Cell]:
        """``grid.cells.clip(cells)``"""
        raise NotImplementedError

    def row(self, y: int) -> set[Cell]:
        """``grid.cells.row(y)``"""
        raise NotImplementedError

    def col(self, x: int) -> set[Cell]:
        """``grid.cells.col(x)``"""
        raise NotImplementedError

    def rect(self, x: int, y: int, width: int, height: int) -> set[Cell]:
        """``grid.cells.rect(x, y, width, height)``"""
        raise NotImplementedError

    def neighbors(self,
                  cell: Cell,
                  *,
                  kind: Neighborhood = Neighborhood.MOORE,
                  radius: int = 1) -> set[Cell]:
        """``grid.cells.neighbors(cell, kind, radius)``"""
        raise NotImplementedError

    def bounds_of(self, cells: set[Cell]) -> set[Cell]:
        """``grid.cells.bounds_of(cells)``"""
        raise NotImplementedError
