"""``gridcode.grid.cells``"""

from enum import StrEnum
from typing import NamedTuple


class Cell(NamedTuple):
    """``Cell``"""

    x: int
    y: int

    def __add__(self, other: Offset) -> Cell:
        return Cell(self.x + other.dx, self.y + other.dy)


class Offset(NamedTuple):
    """``Offset``"""

    dx: int
    dy: int

    def __neg__(self) -> Offset:
        return Offset(-self.dx, -self.dy)


UP    = Offset( 0, -1)
DOWN  = Offset( 0,  1)
LEFT  = Offset(-1,  0)
RIGHT = Offset( 1,  0)


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


MOORE = Neighborhood.MOORE
VON_NEUMANN = Neighborhood.VON_NEUMANN
HORIZONTAL = Neighborhood.HORIZONTAL
VERTICAL = Neighborhood.VERTICAL


class Cells:
    """``Cells``"""

    __slots__ = ("size",)

    def __init__(self, size: int):
        self.size = size

    def all(self) -> set[Cell]:
        """``grid.cells.all()``"""
        raise NotImplementedError

    def wrap(self, cell: Cell) -> Cell:
        """``grid.cells.wrap(cell)``"""
        raise NotImplementedError

    def nearest(self, candidates: set[Cell], to: Cell, *, count: int = 1) -> set[Cell]:
        """``grid.cells.nearest(cells, to, count)``"""
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
