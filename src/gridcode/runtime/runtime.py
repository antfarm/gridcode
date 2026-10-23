"""``gridcode.runtime.runtime``"""

from ..cells import Cell
from .color import Color
from .grid import Grid
from .inspector import Inspector
from .program import Program


class Runtime:
    """``Runtime``"""

    def __init__(self, program: Program):
        program.check_complete()

        self.program = program
        self.inspector = Inspector()
        self.reset()

    @property
    def name(self) -> str:
        """``runtime.name``"""
        return self.program.title

    @property
    def size(self) -> int:
        """``runtime.size``"""
        return self.program.size

    @property
    def frame_rate(self) -> float:
        """``runtime.frame_rate``"""
        return self.program.frame_rate

    def reset(self) -> None:
        """``runtime.reset()``"""
        self.grid = Grid(self.size, self.program.index)
        self.tick = 0
        with self.inspector.timing():
            self.program._setup(self.grid)
        self.inspector.on_tick(self.tick, self.grid)

    def step(self) -> None:
        """``runtime.step()``"""
        with self.inspector.timing():
            self.program._update(self.grid)
        self.tick += 1
        self.inspector.on_tick(self.tick, self.grid)

    def key_press(self, key: str) -> None:
        """``runtime.key_press(key)``"""
        self.program._on_key(self.grid, key)
        self.inspector.on_key_pressed(key, self.grid)

    def cell_click(self, x: int, y: int) -> None:
        """``runtime.cell_click(x, y)``"""
        self.program._on_click(self.grid, Cell(x, y))
        self.inspector.on_tick(self.tick, self.grid)

    def colors(self) -> list[Color]:
        """``runtime.colors()``"""
        return [self.program._color(self.grid, Cell(x, y))
                for y in range(self.size)
                for x in range(self.size)]
