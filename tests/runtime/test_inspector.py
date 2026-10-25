"""``tests.runtime.test_inspector``"""

from gridcode import Cell, Grid, Offset
from gridcode.runtime.inspector import SEPARATOR_WIDTH, Inspector


def inspector_on(cell=None):
    inspector = Inspector()
    inspector.enabled = True
    inspector.cell = cell
    return inspector


def printed(capsys, label, grid, cell=None):
    """What the inspector writes for one event, less the newline print adds."""
    inspector_on(cell).print(label, grid)
    return capsys.readouterr().out.removesuffix("\n")


def test_the_separator_carries_the_label(capsys):
    grid = Grid(4)

    first_line = printed(capsys, "tick 7 · 1.5ms", grid).split("\n")[0]

    assert first_line.endswith(" tick 7 · 1.5ms")
    assert set(first_line.split(" ")[0]) == {"─"}


def test_an_empty_grid_shows_only_the_separator(capsys):
    grid = Grid(4)

    assert printed(capsys, "tick 0", grid).strip().endswith("tick 0")


def test_globals_are_shown_when_they_hold_data(capsys):
    grid = Grid(4)
    grid.data.globals.set({"over": False, "score": 2})

    text = printed(capsys, "tick 0", grid)

    assert text == (
        f"{'─' * SEPARATOR_WIDTH} tick 0\n"
        "\n"
        "globals\n"
        "\n"
        "   ┌───────┬───────┐\n"
        "   │ over  │ false │\n"
        "   ├───────┼───────┤\n"
        "   │ score │ 2     │\n"
        "   └───────┴───────┘\n")


def test_the_inspected_cell_shows_its_maps(capsys):
    grid = Grid(4)
    grid.data.add(Cell(2, 3), {"kind": "ant"})

    text = printed(capsys, "cell (2,3)", grid, Cell(2, 3))

    assert "cell (2,3)\n" in text
    assert "│ kind │ ant │" in text


def test_an_empty_cell_adds_nothing(capsys):
    grid = Grid(4)
    grid.data.add(Cell(0, 0), {"kind": "ant"})

    text = printed(capsys, "cell (2,2)", grid, Cell(2, 2))

    assert "ant" not in text
    assert text.count("cell (2,2)") == 1


def test_keys_are_sorted_and_columns_aligned(capsys):
    grid = Grid(4)
    grid.data.add(Cell(0, 0), {"zebra": 1, "ant": 22, "mongoose": 333})

    rows = [line for line in printed(capsys, "", grid, Cell(0, 0)).split("\n")
            if line.startswith("   │")]

    assert [row.split("│")[1].strip() for row in rows] == ["ant", "mongoose", "zebra"]
    assert len({len(row) for row in rows}) == 1


def test_values_use_gridcode_notation(capsys):
    grid = Grid(4)
    grid.data.add(Cell(0, 0), {"home": Cell(1, 2), "heading": Offset(-1, 0),
                               "alive": True, "dead": False, "rate": 0.5})

    text = printed(capsys, "", grid, Cell(0, 0))
    rows = dict(tuple(cell.strip() for cell in line.split("│")[1:3])
                for line in text.split("\n") if line.startswith("   │"))

    assert rows == {"home": "(cell 1 2)", "heading": "(offset -1 0)",
                    "alive": "true", "dead": "false", "rate": "0.5"}


def test_an_empty_map_renders_as_an_empty_table(capsys):
    grid = Grid(4)
    grid.data.add(Cell(0, 0), {})

    text = printed(capsys, "", grid, Cell(0, 0))

    assert "   ┌───┬───┐\n   └───┴───┘" in text


def test_nothing_is_printed_while_disabled(capsys):
    grid = Grid(4)
    grid.data.globals.set({"score": 0})
    inspector = Inspector()

    inspector.on_tick(3, grid)
    inspector.on_key_pressed("left", grid)

    assert capsys.readouterr().out == ""


def test_each_event_prints_its_own_label(capsys):
    grid = Grid(4)
    inspector = Inspector()

    inspector.set_enabled(True, 3, grid)
    inspector.on_key_pressed("left", grid)
    inspector.select_cell(1, 2, grid)

    labels = [line for line in capsys.readouterr().out.split("\n") if line.startswith("─")]

    assert labels[0].endswith("tick 3 · 0.0ms")
    assert labels[1].endswith("key 'left'")
    assert labels[2].endswith("cell (1,2)")


def test_clearing_the_cell_prints_nothing(capsys):
    inspector = inspector_on(Cell(1, 1))

    inspector.clear_cell()

    assert inspector.cell is None
    assert capsys.readouterr().out == ""


def test_timing_records_how_long_the_block_took():
    inspector = Inspector()

    with inspector.timing():
        pass

    assert inspector.elapsed_ms >= 0.0


def test_timing_records_even_when_the_block_raises():
    inspector = Inspector()

    try:
        with inspector.timing():
            raise RuntimeError("program failed")
    except RuntimeError:
        pass

    assert inspector.elapsed_ms >= 0.0
