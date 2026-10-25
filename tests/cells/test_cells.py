"""``tests.test_cells``"""

import pytest

from gridcode import Cell, Offset
from gridcode.cells import CellGrid, CellStore, Neighborhood


def test_all_returns_every_cell():
    grid = CellGrid(3)

    assert grid.all() == {Cell(x, y) for y in range(3) for x in range(3)}


def test_row_and_column_return_a_line_of_cells():
    grid = CellGrid(3)

    assert grid.row(1) == {Cell(0, 1), Cell(1, 1), Cell(2, 1)}
    assert grid.column(2) == {Cell(2, 0), Cell(2, 1), Cell(2, 2)}


def test_row_and_column_reject_an_index_outside_the_grid():
    grid = CellGrid(3)

    with pytest.raises(IndexError):
        grid.row(3)
    with pytest.raises(IndexError):
        grid.column(-1)


def test_wrap_moves_a_cell_inside_the_grid():
    grid = CellGrid(4)

    assert grid.wrap(Cell(4, -1)) == Cell(0, 3)
    assert grid.wrap({Cell(-1, -1), Cell(2, 2)}) == {Cell(3, 3), Cell(2, 2)}


def test_contains_tells_whether_a_cell_is_on_the_grid():
    grid = CellGrid(3)

    assert grid.contains(Cell(0, 0))
    assert grid.contains(Cell(2, 2))
    assert not grid.contains(Cell(3, 0))
    assert not grid.contains(Cell(0, -1))


def test_clip_drops_cells_outside_the_grid():
    grid = CellGrid(3)

    assert grid.clip({Cell(0, 0), Cell(3, 0), Cell(-1, 2)}) == {Cell(0, 0)}


def test_rect_clips_or_wraps_at_the_edge():
    grid = CellGrid(4)

    assert grid.rect(3, 3, 2, 2, wrap=False) == {Cell(3, 3)}
    assert grid.rect(3, 3, 2, 2, wrap=True) == {Cell(3, 3), Cell(0, 3),
                                                Cell(3, 0), Cell(0, 0)}


def test_moore_neighbors_surround_the_cell():
    grid = CellGrid(5)

    assert grid.neighbors(Cell(2, 2), wrap=False) == {
        Cell(1, 1), Cell(2, 1), Cell(3, 1),
        Cell(1, 2), Cell(3, 2),
        Cell(1, 3), Cell(2, 3), Cell(3, 3)}


def test_von_neumann_neighbors_leave_out_the_diagonals():
    grid = CellGrid(5)

    assert grid.neighbors(Cell(2, 2), kind=Neighborhood.VON_NEUMANN, wrap=False) == {
        Cell(2, 1), Cell(1, 2), Cell(3, 2), Cell(2, 3)}


def test_horizontal_and_vertical_neighbors_follow_one_axis():
    grid = CellGrid(5)

    assert grid.neighbors(Cell(2, 2), kind=Neighborhood.HORIZONTAL, wrap=False) == {
        Cell(1, 2), Cell(3, 2)}
    assert grid.neighbors(Cell(2, 2), kind=Neighborhood.VERTICAL, wrap=False) == {
        Cell(2, 1), Cell(2, 3)}


def test_radius_widens_the_neighborhood():
    grid = CellGrid(7)

    moore = grid.neighbors(Cell(3, 3), radius=2, wrap=False)
    von_neumann = grid.neighbors(Cell(3, 3), kind=Neighborhood.VON_NEUMANN,
                                 radius=2, wrap=False)

    assert len(moore) == 24
    assert len(von_neumann) == 12
    assert Cell(3, 3) not in moore


def test_neighbors_clip_or_wrap_at_the_edge():
    grid = CellGrid(3)

    assert grid.neighbors(Cell(0, 0), wrap=False) == {
        Cell(1, 0), Cell(0, 1), Cell(1, 1)}
    assert len(grid.neighbors(Cell(0, 0), wrap=True)) == 8


def test_nearest_returns_the_closest_candidate():
    grid = CellGrid(10)

    assert grid.nearest({Cell(5, 5), Cell(1, 1)}, to=Cell(0, 0)) == Cell(1, 1)
    assert grid.nearest({Cell(5, 5), Cell(1, 1), Cell(9, 9)},
                        to=Cell(0, 0), count=2) == {Cell(1, 1), Cell(5, 5)}


def test_nearest_rejects_an_empty_candidate_set():
    grid = CellGrid(10)

    with pytest.raises(ValueError):
        grid.nearest(set(), to=Cell(0, 0))


def test_bounds_of_fills_the_enclosing_rectangle():
    grid = CellGrid(5)

    assert grid.bounds_of({Cell(1, 1), Cell(2, 2)}) == {
        Cell(1, 1), Cell(2, 1), Cell(1, 2), Cell(2, 2)}
    assert grid.bounds_of(set()) == set()


def test_random_returns_cells_from_the_grid():
    grid = CellGrid(4)

    assert grid.random() in grid.all()
    assert grid.random(count=3) <= grid.all()
    assert len(grid.random(count=3)) == 3


def test_cell_arithmetic():
    assert Cell(1, 1) + Offset(1, 0) == Cell(2, 1)
    assert Cell(2, 1) - Offset(1, 0) == Cell(1, 1)
    assert Cell(2, 1) - Cell(1, 1) == Offset(1, 0)
    assert -Offset(1, 0) == Offset(-1, 0)


def test_a_cell_holds_the_item_it_was_given():
    store = CellStore[str](CellGrid(4))

    store.set(Cell(1, 2), "wall")

    assert store.item_at(Cell(1, 2)) == "wall"


def test_an_empty_cell_holds_nothing():
    store = CellStore[str](CellGrid(4))

    assert store.item_at(Cell(1, 2)) is None


def test_setting_a_cell_replaces_what_was_there():
    store = CellStore[str](CellGrid(4))

    store.set(Cell(1, 2), "wall")
    store.set(Cell(1, 2), "floor")

    assert store.item_at(Cell(1, 2)) == "floor"


def test_delete_empties_the_cell_and_allows_an_empty_one():
    store = CellStore[str](CellGrid(4))
    store.set(Cell(1, 2), "wall")

    store.delete(Cell(1, 2))
    store.delete(Cell(1, 2))

    assert store.item_at(Cell(1, 2)) is None


def test_a_cell_outside_the_grid_is_refused():
    store = CellStore[str](CellGrid(4))

    with pytest.raises(IndexError):
        store.set(Cell(4, 0), "wall")


def test_clear_empties_every_cell():
    store = CellStore[str](CellGrid(4))
    store.set(Cell(0, 0), "wall")
    store.set(Cell(1, 1), "floor")

    store.clear()

    assert store.item_at(Cell(0, 0)) is None
    assert store.item_at(Cell(1, 1)) is None


def test_the_item_can_be_anything():
    store = CellStore(CellGrid(4))

    store.set(Cell(0, 0), (True, None))
    store.set(Cell(1, 1), {"alive": True})

    assert store.item_at(Cell(0, 0)) == (True, None)
    assert store.item_at(Cell(1, 1)) == {"alive": True}
