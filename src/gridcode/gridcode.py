"""``gridcode.gridcode``"""

from .grid import Grid
from .runtime import Program, Runtime


def run(program: type[Program]) -> None:
    """``run(Program)``"""
    from .ui import UI

    UI(Runtime(Grid(program.size), program)).show()
