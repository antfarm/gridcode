"""``tests.data.test_index``"""

import random

import pytest

from gridcode import ALL, Cell, Grid

KINDS = ("ant", "bee", "food", "trail")


def scanned(grid, matches=None, has=None, at_cells=None):
    """What a query should return, found by looking at every map."""
    maps = set(grid.maps._cell_store.cells_by_item)
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
        grid.maps.add(cell, data)
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

    assert grid.maps.select(**query) == scanned(grid, **query)


def test_the_index_holds_no_deleted_maps():
    grid = populated(ALL)
    index = grid.maps._index

    for map in list(grid.maps.select(matches={"kind": "ant"})):
        grid.maps.delete(map)

    alive = set(grid.maps._cell_store.cells_by_item)
    assert all(maps <= alive for maps in index.maps_by_key.values())
    assert all(maps <= alive for maps in index.maps_by_data.values())
    assert grid.maps.count(matches={"kind": "ant"}) == 0


def test_the_index_follows_a_changed_value():
    grid = Grid(8, ALL)
    ant = grid.maps.add(Cell(1, 1), {"kind": "ant"})

    ant["kind"] = "bee"

    assert grid.maps.count(matches={"kind": "ant"}) == 0
    assert grid.maps.count(matches={"kind": "bee"}) == 1
    assert scanned(grid, matches={"kind": "bee"}) == grid.maps.select(matches={"kind": "bee"})


def test_the_index_survives_a_rejected_write():
    grid = Grid(8, ALL)
    ant = grid.maps.add(Cell(1, 1), {"kind": "ant"})

    with pytest.raises(TypeError):
        ant.set({"kind": "bee", "bad": [1]})

    assert grid.maps.count(matches={"kind": "ant"}) == 1
    assert grid.maps.select(matches={"kind": "ant"}) == {ant}


def test_clear_empties_the_index():
    grid = populated(ALL)
    index = grid.maps._index

    grid.maps.clear()

    assert index.maps_by_key == {}
    assert index.maps_by_data == {}
    assert grid.maps.count(matches={"kind": "ant"}) == 0


def test_an_index_is_only_built_when_fields_are_declared():
    assert not Grid(8).maps.has_index
    assert not Grid(8, []).maps.has_index
    assert Grid(8, ["kind"]).maps.has_index
    assert Grid(8, ALL).maps.has_index


def test_only_declared_fields_are_indexed():
    grid = Grid(8, ["kind"])
    index = grid.maps._index

    grid.maps.add(Cell(1, 1), {"kind": "ant", "energy": 3})

    assert index.is_indexed("kind")
    assert not index.is_indexed("energy")
    assert index.maps_with_key("energy") == set()
    assert len(index.maps_with_data("kind", "ant")) == 1
