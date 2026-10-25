"""``tests.runtime.test_grid``"""

import pytest

from gridcode import Grid
from gridcode.cells import CellGrid
from gridcode.data import DataStore


def test_a_grid_holds_its_cells_and_its_data():
    grid = Grid(8)

    assert isinstance(grid.cells, CellGrid)
    assert isinstance(grid.data, DataStore)
    assert grid.cells.size == 8


def test_a_grid_cannot_hold_extra_state():
    grid = Grid(8)

    with pytest.raises(AttributeError):
        grid.score = 0
