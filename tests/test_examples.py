"""``tests.test_examples``"""

import importlib
import random
import sys
from pathlib import Path

import pytest

import gridcode
from gridcode.runtime import Runtime

EXAMPLES = Path(__file__).parent.parent / "examples"
NAMES = sorted(path.stem for path in EXAMPLES.glob("*.py"))

FRAMES = 5


@pytest.fixture
def example(request, monkeypatch):
    """An example's program, with run() disabled so importing opens no window."""
    monkeypatch.syspath_prepend(str(EXAMPLES))
    monkeypatch.setattr(gridcode, "run", lambda program: None)
    monkeypatch.delitem(sys.modules, request.param, raising=False)
    random.seed(1)
    return importlib.import_module(request.param).program


def test_every_example_is_found():
    assert NAMES


@pytest.mark.parametrize("example", NAMES, indirect=True)
def test_an_example_sets_up_updates_and_paints(example):
    runtime = Runtime(example)

    for _ in range(FRAMES):
        runtime.step()
    colors = runtime.colors()

    assert runtime.tick == FRAMES
    assert len(colors) == example.size ** 2


@pytest.mark.parametrize("example", NAMES, indirect=True)
def test_an_example_survives_events_and_a_reset(example):
    runtime = Runtime(example)

    runtime.key_press("left")
    runtime.cell_click(0, 0)
    runtime.step()
    runtime.reset()
    runtime.step()

    assert runtime.tick == 1
