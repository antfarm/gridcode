"""``tests.data.test_index``"""

import random

import pytest

from gridcode import ALL, Cell, Grid


KINDS = ("ant", "bee", "food", "trail")


def scanned(grid, matches=None, has=None, at_cells=None):
    """What a query should return, found by looking at every map."""
    maps = grid.data._all_maps()
    if at_cells is not None:
        maps = {map for map in maps if map.cell in at_cells}
    if matches:
        maps = {map for map in maps
                if all(map._data.get(key) == value for key, value in matches.items())}
    if has:
        maps = {map for map in maps if all(key in map._data for key in has)}
    return maps


def populated(index, seed=1):
    """A grid with maps of mixed keys, built the same way every time."""
    random.seed(seed)
    grid = Grid(8, index)
    for _ in range(40):
        cell = Cell(random.randrange(8), random.randrange(8))
        data = {"kind": random.choice(KINDS)}
        if random.random() < 0.5:
            data["energy"] = random.randrange(3)
        if random.random() < 0.3:
            data["alive"] = True
        grid.data.add(cell, data)
    return grid


QUERIES = [
    {},
    {"matches": {"kind": "ant"}},
    {"matches": {"kind": "wasp"}},
    {"matches": {"energy": 1}},
    {"matches": {"kind": "ant", "energy": 1}},
    {"has": {"energy"}},
    {"has": {"energy", "alive"}},
    {"matches": {"kind": "bee"}, "has": {"energy"}},
    {"at_cells": {Cell(0, 0), Cell(1, 1), Cell(2, 2)}},
    {"at_cells": set()},
    {"matches": {"kind": "food"}, "at_cells": {Cell(3, 3), Cell(4, 4)}},
    {"matches": {"kind": "ant"}, "has": {"alive"}, "at_cells": {Cell(5, 5)}},
]


@pytest.mark.parametrize("index", [None, ["kind"], ["energy"], ["kind", "alive"], ALL])
@pytest.mark.parametrize("query", QUERIES)
def test_select_agrees_with_a_full_scan(index, query):
    grid = populated(index)

    assert grid.data.select(**query) == scanned(grid, **query)


def test_a_deleted_map_leaves_the_index():
    grid = Grid(8, ALL)
    ant = grid.data.add(Cell(1, 1), {"kind": "ant", "energy": 3})

    grid.data.delete(ant)

    assert grid.data.count(matches={"kind": "ant"}) == 0
    assert grid.data.count(has={"energy"}) == 0


def test_the_index_follows_a_changed_value():
    grid = Grid(8, ALL)
    ant = grid.data.add(Cell(1, 1), {"kind": "ant"})

    ant["kind"] = "bee"

    assert grid.data.count(matches={"kind": "ant"}) == 0
    assert grid.data.count(matches={"kind": "bee"}) == 1
    assert scanned(grid, matches={"kind": "bee"}) == grid.data.select(matches={"kind": "bee"})


def test_the_index_survives_a_rejected_write():
    grid = Grid(8, ALL)
    ant = grid.data.add(Cell(1, 1), {"kind": "ant"})

    with pytest.raises(TypeError):
        ant.set({"kind": "bee", "bad": [1]})

    assert grid.data.count(matches={"kind": "ant"}) == 1
    assert grid.data.select(matches={"kind": "ant"}) == {ant}


def test_clear_empties_the_index():
    grid = populated(ALL)
    index = grid.data._index

    grid.data.clear_cells()

    assert index.maps_by_key == {}
    assert index.maps_by_data == {}
    assert grid.data.count(matches={"kind": "ant"}) == 0


def test_an_index_is_only_built_when_fields_are_declared():
    assert not Grid(8).data._has_index
    assert not Grid(8, []).data._has_index
    assert Grid(8, ["kind"]).data._has_index
    assert Grid(8, ALL).data._has_index


def test_only_declared_fields_are_indexed():
    grid = Grid(8, ["kind"])
    index = grid.data._index

    grid.data.add(Cell(1, 1), {"kind": "ant", "energy": 3})

    assert index.is_indexed("kind")
    assert not index.is_indexed("energy")
    assert index.maps_with_key("energy") == set()
    assert len(index.maps_with_data("kind", "ant")) == 1
