"""``tests.runtime.test_runtime``"""

import pytest

from gridcode import ALL, Cell, Color, Grid, Program
from gridcode.runtime import Runtime


def complete_program(title="Test", **settings):
    program = Program(title, **settings)

    @program.setup
    def setup(grid: Grid) -> None:
        grid.data.add(Cell(0, 0), {"kind": "ant"})

    @program.update
    def update(grid: Grid) -> None:
        grid.data.add(Cell(1, 1), {"kind": "trail"})

    @program.color
    def color(grid: Grid, cell: Cell) -> Color:
        return Color(1.0, 1.0, 1.0)

    @program.on_click
    def on_click(grid: Grid, cell: Cell) -> None:
        grid.data.add(cell, {"kind": "click"})

    @program.on_key
    def on_key(grid: Grid, key: str) -> None:
        grid.data.add(Cell(2, 2), {"kind": key})

    return program


def test_the_runtime_reads_its_settings_from_the_program():
    runtime = Runtime(complete_program("Snake", size=4, frame_rate=30))

    assert runtime.name == "Snake"
    assert runtime.size == 4
    assert runtime.frame_rate == 30


def test_the_settings_cannot_be_changed_through_the_runtime():
    runtime = Runtime(complete_program())

    for setting in ("name", "size", "frame_rate"):
        with pytest.raises(AttributeError):
            setattr(runtime, setting, 1)


def test_construction_runs_setup():
    runtime = Runtime(complete_program(size=4))

    assert runtime.tick == 0
    assert runtime.grid.data.count(matches={"kind": "ant"}) == 1


def test_a_step_runs_update_and_advances_the_tick():
    runtime = Runtime(complete_program(size=4))

    runtime.step()

    assert runtime.tick == 1
    assert runtime.grid.data.count(matches={"kind": "trail"}) == 1


def test_reset_builds_a_fresh_grid_and_runs_setup_again():
    runtime = Runtime(complete_program(size=4))
    runtime.step()
    first_grid = runtime.grid

    runtime.reset()

    assert runtime.tick == 0
    assert runtime.grid is not first_grid
    assert runtime.grid.data.count(matches={"kind": "trail"}) == 0
    assert runtime.grid.data.count(matches={"kind": "ant"}) == 1


def test_events_reach_the_program():
    runtime = Runtime(complete_program(size=4))

    runtime.cell_click(3, 3)
    runtime.key_press("left")

    assert runtime.grid.data.count(matches={"kind": "click"}, at_cells={Cell(3, 3)}) == 1
    assert runtime.grid.data.count(matches={"kind": "left"}) == 1


def test_colors_gives_one_color_per_cell_row_by_row():
    runtime = Runtime(complete_program(size=4))

    colors = runtime.colors()

    assert len(colors) == 16
    assert all(color == Color(1.0, 1.0, 1.0) for color in colors)


def test_the_index_declaration_reaches_the_grid():
    assert Runtime(complete_program(index=["kind"])).grid.data._has_index
    assert Runtime(complete_program(index=ALL)).grid.data._has_index
    assert not Runtime(complete_program()).grid.data._has_index


def test_the_index_survives_a_reset():
    runtime = Runtime(complete_program(index=["kind"]))

    runtime.reset()

    assert runtime.grid.data._has_index
