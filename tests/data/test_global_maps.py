"""``tests.data.test_global_maps``"""

import pytest

from gridcode import Grid


def test_global_maps_are_reached_by_name():
    grid = Grid(8)

    game = grid.globals.add("game", {"score": 0})

    assert grid.globals.exists("game")
    assert grid.globals.get("game") is game
    assert game.name == "game"


def test_a_deleted_global_map_refuses_every_access():
    grid = Grid(8)
    game = grid.globals.add("game", {"score": 0})

    grid.globals.delete("game")

    assert not grid.globals.exists("game")
    with pytest.raises(ValueError):
        game["score"]
    with pytest.raises(ValueError):
        game.name


def test_a_missing_global_map_raises():
    grid = Grid(8)

    with pytest.raises(KeyError):
        grid.globals.get("missing")
