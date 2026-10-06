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


class Cells:
    """``Cells``"""

    __slots__ = ("size",)

    def __init__(self, size: int):
        self.size = size

    def cells(self) -> set[Cell]:
        """``grid.cells()``"""
        raise NotImplementedError

    def wrap(self, cell: Cell) -> Cell:
        """``grid.wrap(cell)``"""
        raise NotImplementedError

    def nearest(self, candidates: set[Cell], to: Cell, count: int = 1) -> set[Cell]:
        """``grid.nearest(cells, to, count)``"""
        raise NotImplementedError

    def row(self, y: int) -> set[Cell]:
        """``grid.row(y)``"""
        raise NotImplementedError

    def col(self, x: int) -> set[Cell]:
        """``grid.col(x)``"""
        raise NotImplementedError

    def rect(self, x: int, y: int, width: int, height: int) -> set[Cell]:
        """``grid.rect(x, y, width, height)``"""
        raise NotImplementedError

    def neighbors(self,
                  cell: Cell,
                  kind: Neighborhood = Neighborhood.MOORE,
                  radius: int = 1) -> set[Cell]:
        """``grid.neighbors(cell, kind, radius)``"""
        raise NotImplementedError

    def neighbors_including(self,
                            cell: Cell,
                            kind: Neighborhood = Neighborhood.MOORE,
                            radius: int = 1) -> set[Cell]:
        """``grid.neighbors_including(cell, kind, radius)``"""
        raise NotImplementedError

    def bounds_of(self, cells: set[Cell]) -> set[Cell]:
        """``grid.bounds_of(cells)``"""
        raise NotImplementedError
