"""``gridcode.grid``"""

from .cells import Cell, Cells


class GridStore[Item]:
    """``GridStore``"""

    __slots__ = ("cells", "items")

    def __init__(self, cells: Cells):
        self.cells = cells
        self.items: dict[Cell, set[Item]] = {}

    def add(self, cell: Cell, item: Item) -> None:
        """``store.add(cell, item)``"""
        self.check(cell)
        self.items.setdefault(cell, set()).add(item)

    def remove(self, cell: Cell, item: Item) -> None:
        """``store.remove(cell, item)``"""
        items = self.items.get(cell)
        if items is None or item not in items:
            raise KeyError(f"{item!r} is not at {cell}")

        items.discard(item)
        if not items:
            del self.items[cell]

    def move(self, cell: Cell, item: Item, to: Cell) -> None:
        """``store.move(cell, item, to)``"""
        self.check(to)
        self.remove(cell, item)
        self.add(to, item)

    def items_at(self, cell: Cell) -> set[Item]:
        """``store.items_at(cell)``"""
        return set(self.items.get(cell, ()))

    def clear(self) -> None:
        """``store.clear()``"""
        self.items.clear()

    def check(self, cell: Cell) -> None:
        """``store.check(cell)``"""
        size = self.cells.size
        if not (0 <= cell.x < size and 0 <= cell.y < size):
            raise IndexError(f"{cell} is outside the grid")


class Grid[Data]:
    """``Grid``"""

    __slots__ = ("cells", "store", "data")

    def __init__(self, size: int, data_class: type[Data]):
        self.cells = Cells(size)
        self.store = GridStore(self.cells)
        self.data = data_class(self.store)
