"""``gridcode.display.color``"""

from typing import NamedTuple


class Color(NamedTuple):
    """``Color``"""

    r: float
    g: float
    b: float
    a: float = 1.0

    def with_opacity(self, a: float) -> Color:
        """``color.with_opacity(a)``"""
        return Color(self.r, self.g, self.b, a)
