"""``tests.data.test_data``"""

import pytest

from gridcode import Cell, Grid, Offset


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


def test_move_to_the_same_cell_changes_nothing():
    grid = Grid(8)
    ant = grid.data.add(Cell(3, 3), {"kind": "ant"})

    grid.data.move(ant, Cell(3, 3))

    assert ant.cell == Cell(3, 3)
    assert grid.data.count(at_cells={Cell(3, 3)}) == 1


def test_moving_or_copying_off_the_grid_raises():
    grid = Grid(8)
    ant = grid.data.add(Cell(0, 0), {"kind": "ant"})

    with pytest.raises(IndexError):
        grid.data.move(ant, Offset(0, -1))
    with pytest.raises(IndexError):
        grid.data.copy(ant, Cell(8, 0))


def test_a_refused_move_leaves_the_map_where_it_was():
    grid = Grid(8)
    ant = grid.data.add(Cell(0, 0), {"kind": "ant"})

    with pytest.raises(IndexError):
        grid.data.move(ant, Offset(0, -1))

    assert ant.cell == Cell(0, 0)
    assert grid.data.count(at_cells={Cell(0, 0)}) == 1


def test_delete_removes_the_map_from_the_grid():
    grid = Grid(8)
    ant = grid.data.add(Cell(1, 1), {"kind": "ant"})

    grid.data.delete(ant)

    assert grid.data.count() == 0


@pytest.mark.parametrize("use", [
    lambda map: map["kind"],
    lambda map: map.get("kind", "kind"),
    lambda map: map.set({"kind": "bee"}),
    lambda map: map.delete("kind"),
    lambda map: map.has("kind"),
    lambda map: map.matches({"kind": "ant"}),
    lambda map: map.cell,
], ids=["getitem", "get", "set", "delete", "has", "matches", "cell"])
def test_a_deleted_map_refuses_every_access(use):
    grid = Grid(8)
    ant = grid.data.add(Cell(1, 1), {"kind": "ant"})

    grid.data.delete(ant)

    with pytest.raises(ValueError):
        use(ant)


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
    globals_map = grid.data.globals

    grid.data.clear_globals()

    assert not grid.data.globals.has("score")
    assert grid.data.globals is globals_map


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


def test_count_and_exists_follow_select():
    grid = Grid(8)
    grid.data.add(Cell(1, 1), {"kind": "ant"})
    grid.data.add(Cell(1, 1), {"kind": "food"})
    grid.data.add(Cell(4, 4), {"kind": "ant"})

    for query in ({}, {"matches": {"kind": "ant"}}, {"matches": {"kind": "wasp"}}):
        maps = grid.data.select(**query)

        assert grid.data.count(**query) == len(maps)
        assert grid.data.exists(**query) == bool(maps)


def test_select_cells_gives_the_cells_of_the_selected_maps():
    grid = Grid(8)
    grid.data.add(Cell(1, 1), {"kind": "ant"})
    grid.data.add(Cell(1, 1), {"kind": "food"})
    grid.data.add(Cell(4, 4), {"kind": "ant"})

    assert grid.data.select_cells(matches={"kind": "ant"}) == {Cell(1, 1), Cell(4, 4)}
    assert grid.data.select_cells(matches={"kind": "wasp"}) == set()
