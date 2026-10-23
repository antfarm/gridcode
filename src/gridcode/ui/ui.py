"""``gridcode.ui.ui``"""

import time

from ..runtime import Runtime
from ..runtime.inspector import Inspector
from .window import Window


class UI:
    """``UI``"""

    def __init__(self, runtime: Runtime):
        self.runtime = runtime
        self.running = False
        self.window = Window(self, f"GridCode - {runtime.name}", runtime.size)

    def show(self) -> None:
        """``ui.show()``"""
        self.window.update_grid(self.runtime.colors())
        self.window.root.mainloop()

    def start(self) -> None:
        """``ui.start()``"""
        self.running = True
        self.window.update_controls(self.running, self.inspector.enabled)
        self._tick()

    def pause(self) -> None:
        """``ui.pause()``"""
        self.running = False
        self.window.update_controls(self.running, self.inspector.enabled)

    def _tick(self) -> None:
        if not self.running:
            return

        time_start = time.monotonic()
        self.step()
        elapsed_ms = (time.monotonic() - time_start) * 1000

        delay_ms = max(1, round(1000 / self.runtime.frame_rate - elapsed_ms))
        self.window.root.after(delay_ms, self._tick)

    def step(self) -> None:
        """``ui.step()``"""
        self.runtime.step()
        self.window.update_grid(self.runtime.colors())

    def reset(self) -> None:
        """``ui.reset()``"""
        self.runtime.reset()
        self.window.update_grid(self.runtime.colors())

    def key_pressed(self, key: str) -> None:
        """``ui.key_pressed(key)``"""
        self.runtime.key_press(key)
        self.window.update_grid(self.runtime.colors())

    def cell_clicked(self, x: int, y: int) -> None:
        """``ui.cell_clicked(x, y)``"""
        if self.inspector.enabled:
            self._set_inspected_cell(x, y)
        else:
            self.runtime.cell_click(x, y)
            self.window.update_grid(self.runtime.colors())

    @property
    def inspector(self) -> Inspector:
        """``ui.inspector``"""
        return self.runtime.inspector

    def set_inspector_enabled(self, inspector_enabled: bool) -> None:
        """``ui.set_inspector_enabled(inspector_enabled)``"""
        if not inspector_enabled:
            self._clear_inspected_cell()
        self.inspector.set_enabled(inspector_enabled, self.runtime.tick,
                                   self.runtime.grid)
        self.window.update_controls(self.running, self.inspector.enabled)

    def _clear_inspected_cell(self) -> None:
        cell = self.inspector.cell
        self.inspector.clear_cell()
        if cell is not None:
            self.window.update_cell_highlight(cell.x, cell.y, False)

    def _set_inspected_cell(self, x: int, y: int) -> None:
        inspected_cell = self.inspector.cell
        self.inspector.select_cell(x, y, self.runtime.grid)
        if inspected_cell is not None:
            self.window.update_cell_highlight(inspected_cell.x, inspected_cell.y, False)
        self.window.update_cell_highlight(x, y, True)
