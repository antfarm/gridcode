"""``tests.runtime.test_program``"""

import pytest

from gridcode import Cell, Color, Grid, Program
from gridcode.runtime import Runtime


def test_settings_have_defaults():
    program = Program("Test")

    assert program.title == "Test"
    assert program.size == 16
    assert program.frame_rate == 8
    assert program.index is None


def test_a_decorator_returns_the_function_unchanged():
    program = Program("Test")

    @program.setup
    def setup(grid: Grid) -> None:
        pass

    assert setup.__name__ == "setup"
    assert program._setup is setup


def test_the_function_name_does_not_have_to_match_the_callback():
    program = Program("Test")

    @program.color
    def paint(grid: Grid, cell: Cell) -> Color:
        return Color(0.0, 0.0, 0.0)

    assert program._color is paint


def test_a_program_cannot_hold_extra_state():
    program = Program("Test")

    with pytest.raises(AttributeError):
        program.score = 0


def test_an_incomplete_program_is_rejected_with_the_missing_names():
    program = Program("Half")

    @program.setup
    def setup(grid: Grid) -> None:
        pass

    with pytest.raises(TypeError) as rejection:
        Runtime(program)

    assert "Half" in str(rejection.value)
    assert "update" in str(rejection.value)
    assert "setup" not in str(rejection.value)
