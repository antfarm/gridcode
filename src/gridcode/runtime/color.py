"""``gridcode.runtime.color``"""

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

    def to_rgb_hex(self) -> str:
        """``color.to_rgb_hex()``"""
        return "#%02x%02x%02x" % (round(self.r * self.a * 255),
                                  round(self.g * self.a * 255),
                                  round(self.b * self.a * 255))
