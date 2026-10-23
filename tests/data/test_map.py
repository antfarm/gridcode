"""``tests.data.test_map``"""

import pytest

from gridcode import Cell, Grid, Offset


def test_values_must_be_gridcode_values():
    grid = Grid(8)

    with pytest.raises(TypeError):
        grid.maps.add(Cell(1, 1), {"bad": [1, 2]})

    ant = grid.maps.add(Cell(1, 1), {"kind": "ant"})
    with pytest.raises(TypeError):
        ant["bad"] = {"nested": True}


def test_every_value_type_is_accepted():
    grid = Grid(8)

    map = grid.maps.add(Cell(1, 1), {"flag": True, "count": 2, "rate": 0.5,
                                     "kind": "ant", "home": Cell(0, 0),
                                     "heading": Offset(1, 0)})

    assert map.get("flag", "count", "rate") == (True, 2, 0.5)
    assert map["home"] == Cell(0, 0)


def test_get_and_delete_take_several_keys():
    grid = Grid(8)
    map = grid.maps.add(Cell(1, 1), {"a": 1, "b": 2, "c": 3})

    assert map.get("a", "c") == (1, 3)

    map.delete("a", "b")

    assert not map.has("a")
    assert map.has("c")


def test_has_and_matches_ask_about_keys_and_values():
    grid = Grid(8)
    map = grid.maps.add(Cell(1, 1), {"kind": "ant", "energy": 3})

    assert map.has("kind", "energy")
    assert not map.has("kind", "missing")
    assert map.matches({"kind": "ant"})
    assert not map.matches({"kind": "bee"})


def test_missing_key_raises():
    grid = Grid(8)
    map = grid.maps.add(Cell(1, 1), {"kind": "ant"})

    with pytest.raises(KeyError):
        map["missing"]
    with pytest.raises(KeyError):
        map.delete("missing")
