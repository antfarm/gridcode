"""``tests.test_inspector``"""

from gridcode import Cell, Grid, Offset
from gridcode.runtime.inspector import Inspector


def inspector_on(cell=None):
    inspector = Inspector()
    inspector.enabled = True
    inspector.cell = cell
    return inspector


def test_the_separator_carries_the_label():
    grid = Grid(4)

    first_line = inspector_on()._inspection_string("tick 7 · 1.5ms", grid).split("\n")[0]

    assert first_line.endswith(" tick 7 · 1.5ms")
    assert set(first_line.split(" ")[0]) == {"─"}


def test_an_empty_grid_shows_only_the_separator():
    grid = Grid(4)

    assert inspector_on()._inspection_string("tick 0", grid).strip().endswith("tick 0")


def test_globals_are_shown_when_they_hold_data():
    grid = Grid(4)
    grid.data.globals.set({"over": False, "score": 2})

    text = inspector_on()._inspection_string("tick 0", grid)

    assert text == (
        "──────────────────────────────────────────────────────────── tick 0\n"
        "\n"
        "globals\n"
        "\n"
        "   ┌───────┬───────┐\n"
        "   │ over  │ false │\n"
        "   ├───────┼───────┤\n"
        "   │ score │ 2     │\n"
        "   └───────┴───────┘\n")


def test_the_inspected_cell_shows_its_maps():
    grid = Grid(4)
    grid.data.add(Cell(2, 3), {"kind": "ant"})

    text = inspector_on(Cell(2, 3))._inspection_string("cell (2,3)", grid)

    assert "cell (2,3)\n" in text
    assert "│ kind │ ant │" in text


def test_an_empty_cell_adds_nothing():
    grid = Grid(4)
    grid.data.add(Cell(0, 0), {"kind": "ant"})

    text = inspector_on(Cell(2, 2))._inspection_string("cell (2,2)", grid)

    assert "ant" not in text
    assert text.count("cell (2,2)") == 1


def test_keys_are_sorted_and_columns_aligned():
    grid = Grid(4)
    grid.data.add(Cell(0, 0), {"zebra": 1, "ant": 22, "mongoose": 333})

    rows = [line for line in
            inspector_on(Cell(0, 0))._inspection_string("", grid).split("\n")
            if line.startswith("   │")]

    assert [row.split("│")[1].strip() for row in rows] == ["ant", "mongoose", "zebra"]
    assert len({len(row) for row in rows}) == 1


def test_values_use_gridcode_notation():
    grid = Grid(4)
    grid.data.add(Cell(0, 0), {"home": Cell(1, 2), "heading": Offset(-1, 0),
                               "alive": True, "dead": False, "rate": 0.5})

    text = inspector_on(Cell(0, 0))._inspection_string("", grid)
    rows = dict(tuple(cell.strip() for cell in line.split("│")[1:3])
                for line in text.split("\n") if line.startswith("   │"))

    assert rows == {"home": "(cell 1 2)", "heading": "(offset -1 0)",
                    "alive": "true", "dead": "false", "rate": "0.5"}


def test_an_empty_map_renders_as_an_empty_table():
    grid = Grid(4)
    grid.data.add(Cell(0, 0), {})

    text = inspector_on(Cell(0, 0))._inspection_string("", grid)

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
