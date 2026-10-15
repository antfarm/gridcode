"""``gridcode.gridcode``"""

from .runtime import Program, Runtime


def run(program: type[Program]) -> None:
    """``run(Program)``"""
    from .ui import UI

    UI(Runtime(program)).show()
