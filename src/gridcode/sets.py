"""``gridcode.sets``"""


_MISSING = object()


def only[Item](items: set[Item], default: Item | None = _MISSING) -> Item | None:
    """``only(items)``

    ``only(items, default)``
    """
    if len(items) > 1:
        raise ValueError(f"expected one item, found {len(items)}")
    if items:
        return next(iter(items))
    if default is _MISSING:
        raise ValueError("expected one item, found none")
    return default
