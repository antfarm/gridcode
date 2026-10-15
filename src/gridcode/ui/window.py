"""``gridcode.ui.window``"""

import tkinter

from ..runtime import Color
from .grid_view import GridView


def key_name(event) -> str:
    """``key_name(event)``"""
    if event.char and not event.char.isspace():
        return event.char
    return event.keysym.lower()


class Window:
    """``Window``"""

    def __init__(self, ui, title: str, grid_size: int):
        self.root = tkinter.Tk()
        self.root.title(title)

        self.root.bind("<Key>", lambda event: ui.key_pressed(key_name(event)))

        self.content = tkinter.Frame(self.root)
        self.content.pack()

        self.grid = GridView(ui, self.content, grid_size)

        self.controls = tkinter.Frame(self.root)
        self.controls.pack(pady=8)

        self.reset_button = tkinter.Button(self.controls, text="Setup",
                                           command=ui.reset)
        self.start_button = tkinter.Button(self.controls, text="Run",
                                           command=ui.start)
        self.pause_button = tkinter.Button(self.controls, text="Stop",
                                           command=ui.pause)
        self.step_button = tkinter.Button(self.controls, text="Step",
                                          command=ui.step)

        self.inspect_var = tkinter.BooleanVar()
        self.inspect_check = tkinter.Checkbutton(self.controls,
                                                 text="Inspect",
                                                 variable=self.inspect_var,
                                                 command=lambda: ui.set_inspecting(
                                                     self.inspect_var.get()))

        for widget in (self.reset_button, self.start_button, self.pause_button,
                       self.step_button, self.inspect_check):
            widget.pack(side="left", padx=10)

        self.update_controls(ui.running, ui.inspecting)

    def update_grid(self, colors: list[Color]) -> None:
        """``window.update_grid(colors)``"""
        self.grid.draw(colors)

    def update_cell_highlight(self, x: int, y: int, highlighted: bool) -> None:
        """``window.update_cell_highlight(x, y, highlighted)``"""
        if highlighted:
            self.grid.add_cell_highlight(x, y)
        else:
            self.grid.remove_cell_highlight(x, y)

    def update_controls(self, running: bool, inspecting: bool) -> None:
        """``window.update_controls(running, inspecting)``"""
        self.start_button["state"] = "disabled" if running else "normal"
        self.step_button["state"] = "disabled" if running else "normal"
        self.pause_button["state"] = "normal" if running else "disabled"
        self.inspect_var.set(inspecting)
