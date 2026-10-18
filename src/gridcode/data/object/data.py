"""``gridcode.data.object.data``"""

from ...grid import GridStore


class ObjectData:
    """``ObjectData``"""

    def __init__(self, store: GridStore[object]):
        self.store = store
