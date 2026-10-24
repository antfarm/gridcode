"""``tests.data.test_data``"""

import pytest

from gridcode import ALL, Cell, Grid, Offset


def test_add_stores_the_data_at_the_cell():
    grid = Grid(8)

    ant = grid.data.add(Cell(1, 1), {"kind": "ant", "energy": 3})

    assert ant.cell == Cell(1, 1)
    assert ant["kind"] == "ant"
    assert grid.data.count() == 1


def test_add_copies_the_data_so_the_caller_cannot_change_it():
    grid = Grid(8)
    data = {"kind": "ant"}

    ant = grid.data.add(Cell(1, 1), data)
    data["kind"] = "bee"

    assert ant["kind"] == "ant"


def test_a_cell_holds_several_maps():
    grid = Grid(8)

    grid.data.add(Cell(1, 1), {"kind": "ant"})
    grid.data.add(Cell(1, 1), {"kind": "trail"})

    assert grid.data.count(at_cells={Cell(1, 1)}) == 2


def test_move_takes_a_cell_or_an_offset():
    grid = Grid(8)
    ant = grid.data.add(Cell(3, 3), {"kind": "ant"})

    grid.data.move(ant, Offset(1, 0))
    assert ant.cell == Cell(4, 3)

    grid.data.move(ant, Cell(0, 0))
    assert ant.cell == Cell(0, 0)


def test_copy_leaves_the_original_in_place():
    grid = Grid(8)
    ant = grid.data.add(Cell(3, 3), {"kind": "ant"})

    twin = grid.data.copy(ant, Offset(1, 0))

    assert ant.cell == Cell(3, 3)
    assert twin.cell == Cell(4, 3)
    assert twin["kind"] == "ant"
    assert twin is not ant


def test_copy_does_not_share_data_with_the_original():
    grid = Grid(8)
    ant = grid.data.add(Cell(3, 3), {"kind": "ant"})

    twin = grid.data.copy(ant, Cell(5, 5))
    twin["kind"] = "bee"

    assert ant["kind"] == "ant"


def test_moving_or_copying_off_the_grid_raises():
    grid = Grid(8)
    ant = grid.data.add(Cell(0, 0), {"kind": "ant"})

    with pytest.raises(IndexError):
        grid.data.move(ant, Offset(0, -1))
    with pytest.raises(IndexError):
        grid.data.copy(ant, Cell(8, 0))


def test_a_deleted_map_refuses_every_access():
    grid = Grid(8)
    ant = grid.data.add(Cell(1, 1), {"kind": "ant"})

    grid.data.delete(ant)

    assert grid.data.count() == 0
    for use in (lambda: ant["kind"],
                lambda: ant.get("kind", "kind"),
                lambda: ant.set({"kind": "bee"}),
                lambda: ant.delete("kind"),
                lambda: ant.has("kind"),
                lambda: ant.matches({"kind": "ant"}),
                lambda: ant.cell):
        with pytest.raises(ValueError):
            use()


def test_clear_cells_deletes_every_map():
    grid = Grid(8)
    ant = grid.data.add(Cell(1, 1), {"kind": "ant"})
    grid.data.add(Cell(2, 2), {"kind": "bee"})

    grid.data.clear_cells()

    assert grid.data.count() == 0
    with pytest.raises(ValueError):
        ant["kind"]


def test_globals_hold_data_without_a_cell():
    grid = Grid(8)

    grid.data.globals.set({"over": False, "score": 0})
    grid.data.globals["score"] = 7

    assert grid.data.globals["score"] == 7
    assert grid.data.globals.has("over")
    assert grid.data.count() == 0


def test_clear_globals_empties_the_globals_map():
    grid = Grid(8)
    grid.data.globals.set({"score": 7})
    globals = grid.data.globals

    grid.data.clear_globals()

    assert not grid.data.globals.has("score")
    assert grid.data.globals is globals


def test_clear_empties_both_cells_and_globals():
    grid = Grid(8)
    grid.data.add(Cell(1, 1), {"kind": "ant"})
    grid.data.globals.set({"score": 7})

    grid.data.clear()

    assert grid.data.count() == 0
    assert not grid.data.globals.has("score")


def test_cell_of_finds_the_cell_a_map_sits_in():
    grid = Grid(8)
    ant = grid.data.add(Cell(1, 1), {"kind": "ant"})

    assert grid.data.cell_of(ant) == Cell(1, 1)


def test_an_empty_map_is_allowed():
    grid = Grid(8)

    map = grid.data.add(Cell(1, 1), {})

    assert grid.data.count() == 1
    assert not map.has("anything")


def test_indexed_fields_do_not_change_what_a_program_sees():
    for index in (None, [], ["kind"], ["kind", "energy"], ALL):
        grid = Grid(8, index)
        ant = grid.data.add(Cell(1, 1), {"kind": "ant", "energy": 3})
        grid.data.add(Cell(1, 1), {"kind": "food"})
        grid.data.add(Cell(4, 4), {"kind": "ant", "energy": 1})

        assert grid.data.count() == 3
        assert grid.data.count(matches={"kind": "ant"}) == 2
        assert grid.data.count(matches={"energy": 3}) == 1
        assert grid.data.count(has={"energy"}) == 2
        assert grid.data.count(matches={"kind": "ant"}, has={"energy"}) == 2
        assert grid.data.count(at_cells={Cell(1, 1)}) == 2
        assert grid.data.count(matches={"kind": "ant"}, at_cells={Cell(1, 1)}) == 1
        assert grid.data.count(matches={"kind": "wasp"}) == 0
        assert grid.data.count(at_cells=set()) == 0
        assert grid.data.select_cells(matches={"kind": "ant"}) == {Cell(1, 1), Cell(4, 4)}
        assert grid.data.exists(matches={"kind": "food"})
        assert not grid.data.exists(matches={"kind": "wasp"})

        ant["energy"] = 9

        assert grid.data.count(matches={"energy": 9}) == 1
        assert grid.data.count(matches={"energy": 3}) == 0

        ant.delete("energy")

        assert grid.data.count(has={"energy"}) == 1

        grid.data.delete(ant)

        assert grid.data.count(matches={"kind": "ant"}) == 1
