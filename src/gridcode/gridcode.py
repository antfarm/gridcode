"""``gridcode.gridcode``"""

from .runtime import Program, Runtime


def run(program: Program) -> None:
    """``run(program)``"""
    from .ui import UI

    UI(Runtime(program)).show()
