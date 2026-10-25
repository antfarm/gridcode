"""``tests.test_sets``"""

import pytest

from gridcode import Cell, only


def test_only_returns_the_single_item():
    assert only({Cell(1, 1)}) == Cell(1, 1)
    assert only({"ant"}) == "ant"


def test_only_raises_for_more_than_one_item():
    with pytest.raises(ValueError):
        only({"ant", "bee"})


def test_only_raises_for_an_empty_set():
    with pytest.raises(ValueError):
        only(set())


def test_only_returns_the_default_for_an_empty_set():
    assert only(set(), None) is None
    assert only(set(), "nothing") == "nothing"


def test_only_raises_for_more_than_one_item_even_with_a_default():
    with pytest.raises(ValueError):
        only({"ant", "bee"}, None)
