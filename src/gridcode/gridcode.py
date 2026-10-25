"""``gridcode.gridcode``"""

from .runtime import Program
from .runtime.runtime import Runtime


def run(program: Program) -> None:
    """``run(program)``"""
    from .ui.ui import UI

    UI(Runtime(program)).show()
