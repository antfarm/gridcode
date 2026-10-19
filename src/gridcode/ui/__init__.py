"""``gridcode.ui``"""

import time

from ..runtime import Runtime
from .window import Window

__all__ = [
    "UI",
    "Window",
]


class UI:
    """``UI``"""

    def __init__(self, runtime: Runtime):
        self.runtime = runtime
        self.running = False
        self.inspecting = False
        self.inspected_cell = None
        self.window = Window(self, f"GridCode - {runtime.name}", runtime.size)

    def show(self) -> None:
        """``ui.show()``"""
        self.window.update_grid(self.runtime.colors())
        self.window.root.mainloop()

    def start(self) -> None:
        """``ui.start()``"""
        self.running = True
        self.window.update_controls(self.running, self.inspecting)
        self._tick()

    def pause(self) -> None:
        """``ui.pause()``"""
        self.running = False
        self.window.update_controls(self.running, self.inspecting)

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

    def set_inspecting(self, inspecting: bool) -> None:
        """``ui.set_inspecting(inspecting)``"""
        self.inspecting = inspecting
        if not inspecting:
            self._reset_inspected_cell()
        self.window.update_controls(self.running, self.inspecting)

    def key_pressed(self, key: str) -> None:
        """``ui.key_pressed(key)``"""
        self.runtime.key_press(key)
        self.window.update_grid(self.runtime.colors())

    def cell_clicked(self, x: int, y: int) -> None:
        """``ui.cell_clicked(x, y)``"""
        if self.inspecting:
            self._reset_inspected_cell()
            self._set_inspected_cell(x, y)
        else:
            self.runtime.cell_click(x, y)
            self.window.update_grid(self.runtime.colors())

    def _reset_inspected_cell(self) -> None:
        if self.inspected_cell is not None:
            x, y = self.inspected_cell
            self.runtime.stop_inspection(x, y)
            self.window.update_cell_highlight(x, y, False)
        self.inspected_cell = None

    def _set_inspected_cell(self, x: int, y: int) -> None:
        self.inspected_cell = (x, y)
        self.runtime.start_inspection(x, y)
        self.window.update_cell_highlight(x, y, True)
