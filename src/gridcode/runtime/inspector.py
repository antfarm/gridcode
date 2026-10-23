"""``gridcode.runtime.inspector``"""

import time
from contextlib import contextmanager

from ..cells import Cell, Offset
from ..data import Map, Value
from .grid import Grid


SEPARATOR_WIDTH = 60
INDENT = "   "


class Inspector:
    """``Inspector``"""

    __slots__ = ("enabled", "cell", "elapsed_ms")

    def __init__(self):
        self.enabled = False
        self.cell = None
        self.elapsed_ms = 0.0

    @contextmanager
    def timing(self):
        """``with inspector.timing(): ...``"""
        time_start = time.monotonic()
        try:
            yield
        finally:
            self.elapsed_ms = (time.monotonic() - time_start) * 1000

    def set_enabled(self, enabled: bool, tick: int, grid: Grid) -> None:
        """``inspector.set_enabled(enabled, tick, grid)``"""
        self.enabled = enabled
        self.on_tick(tick, grid)

    def select_cell(self, x: int, y: int, grid: Grid) -> None:
        """``inspector.select_cell(x, y, grid)``"""
        self.cell = Cell(x, y)
        self.on_cell_selected(grid)

    def clear_cell(self) -> None:
        """``inspector.clear_cell()``"""
        self.cell = None

    def on_tick(self, tick: int, grid: Grid) -> None:
        """``inspector.on_tick(tick, grid)``"""
        self.print(f"tick {tick} · {self.elapsed_ms:.1f}ms", grid)

    def on_key_pressed(self, key: str, grid: Grid) -> None:
        """``inspector.on_key_pressed(key, grid)``"""
        self.print(f"key '{key}'", grid)

    def on_cell_selected(self, grid: Grid) -> None:
        """``inspector.on_cell_selected(grid)``"""
        self.print(f"cell ({self.cell.x},{self.cell.y})", grid)

    def print(self, label: str, grid: Grid) -> None:
        """``inspector.print(label, grid)``"""
        if self.enabled:
            print(self._inspection_string(label, grid))

    def _inspection_string(self, label: str, grid: Grid) -> str:
        blocks = [_separator_string(label)]

        for name, map in grid.globals._maps.items():
            blocks.append(name)
            blocks.append(_map_string(map))

        if self.cell is not None:
            maps = grid.maps.select(at_cells={self.cell})
            if maps:
                blocks.append(f"cell ({self.cell.x},{self.cell.y})")
                blocks.extend(_map_string(map) for map in maps)

        return "\n\n".join(blocks) + "\n"


def _value_string(value: Value) -> str:
    if isinstance(value, Cell):
        return f"(cell {value.x} {value.y})"
    if isinstance(value, Offset):
        return f"(offset {value.dx} {value.dy})"
    if value is True:
        return "true"
    if value is False:
        return "false"
    return str(value)


def _separator_string(label: str) -> str:
    return f"{"─" * SEPARATOR_WIDTH} {label}"


def _map_string(map: Map) -> str:
    pairs = sorted((key, _value_string(value)) for key, value in map._data.items())
    key_width = max((len(key) for key, _ in pairs), default=1)
    value_width = max((len(value) for _, value in pairs), default=1)

    def line(left, middle, right):
        return (f"{INDENT}{left}{'─' * (key_width + 2)}"
                f"{middle}{'─' * (value_width + 2)}{right}")

    rows = [f"{INDENT}│ {key:<{key_width}} │ {value:<{value_width}} │"
            for key, value in pairs]

    row_separator = line("├", "┼", "┤")
    inside = []
    for position, row in enumerate(rows):
        if position:
            inside.append(row_separator)
        inside.append(row)

    return "\n".join([line("┌", "┬", "┐"), *inside, line("└", "┴", "┘")])
