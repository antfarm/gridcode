"""``tests.runtime.test_program``"""

import pytest

from gridcode import Cell, Color, Grid, Program
from gridcode.runtime.runtime import Runtime


def test_size_and_frame_rate_are_required():
    with pytest.raises(TypeError):
        Program("Test")


def test_the_index_is_optional():
    program = Program("Test", size=4, frame_rate=1)

    assert program.index is None


def test_a_decorator_returns_the_function_unchanged():
    program = Program("Test", size=4, frame_rate=1)

    def setup(grid: Grid) -> None:
        pass

    assert program.setup(setup) is setup


def test_a_decorator_registers_the_function():
    program = Program("Test", size=4, frame_rate=1)

    @program.setup
    def setup(grid: Grid) -> None:
        pass

    assert program._setup is setup


def test_the_function_name_does_not_have_to_match_the_callback():
    program = Program("Test", size=4, frame_rate=1)

    @program.color
    def paint(grid: Grid, cell: Cell) -> Color:
        return Color(0.0, 0.0, 0.0)

    assert program._color is paint


def test_a_program_cannot_hold_extra_state():
    program = Program("Test", size=4, frame_rate=1)

    with pytest.raises(AttributeError):
        program.score = 0


def test_an_incomplete_program_is_rejected_with_the_missing_names():
    program = Program("Half", size=4, frame_rate=1)

    @program.setup
    def setup(grid: Grid) -> None:
        pass

    with pytest.raises(TypeError) as rejection:
        Runtime(program)

    assert "Half" in str(rejection.value)
    assert "update" in str(rejection.value)
    assert "setup" not in str(rejection.value)
