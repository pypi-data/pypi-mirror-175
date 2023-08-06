import typing

import vim_quest_cli.deps.ansi.color as ansi_color

from vim_quest_cli.deps.is_js import IS_JS
from vim_quest_cli.interface.mapping import input_code_to_enum, KeyNames
from vim_quest_cli.mode.mode_interface import Mode

if not IS_JS:
    import curses
    from curses import window as curses_window
else:
    curses_window = typing.Any

from vim_quest_cli.deps.with_stdin_raw import with_stdin_raw
from vim_quest_cli.engine.engine_interface import EngineState, EngineInterface
from vim_quest_cli.interface.curses_window import Window
from vim_quest_cli.view.view import (
    ViewFactory,
    ViewData,
    CharacterView,
    RESET_STYLE,
    FgColor,
)


class TerminalUI:
    def __init__(
        self,
        mode: Mode,
        unicode_supported=True,
    ):
        self._mode: Mode = mode
        self._unicode_supported = unicode_supported
        self._screen_size_has_been_initialized = False

    def _assure_screen_size_present(self, stdscr):
        if self._screen_size_has_been_initialized:
            return
        self._screen_size_has_been_initialized = True
        screen_rows, screen_cols = stdscr.getmaxyx()
        self._state = self._state.copy(
            screen_cols=screen_cols,
            screen_rows=screen_rows - 1,  # Leave space for the status
        )

    def loop_one_step(self, input_str: str, stdscr: curses_window):
        # self._assure_screen_size_present(stdscr)

        if not input_str:
            view = self._mode.feedkey()
            self._refresh_state(view, stdscr)
            return

        key_name = input_code_to_enum(input_str)
        if key_name in {"q", "Q", KeyNames.CTRL_C}:
            raise StopIteration()

        view = self._mode.feedkey([key_name])

        self._refresh_state(view, stdscr)

    def _clean_before_leaving(self, stdscr: curses_window):
        stdscr.clear()
        stdscr.move(0, 0)
        stdscr.refresh()

    def start_with_window(self, stdscr: Window):

        try:
            self.loop_one_step(None, stdscr)
            while True:
                input_str = stdscr.getkey()
                self.loop_one_step(input_str, stdscr)
        except StopIteration:
            self._clean_before_leaving(stdscr)
            return

    def start_ansi(self):
        with with_stdin_raw():
            self.start_with_window(Window())

    def start_curses(self):
        curses.wrapper(self.start_with_window)

    def _refresh_state(self, view: ViewData, stdscr: Window):
        stdscr.clear()  # TODO there should be a way to avoid using that, it makes the screen blink.

        stdscr._write("\033[?25l")  # hide cursor

        def process_character(c: CharacterView) -> str:
            fg_color = c.fg_color.value if c.fg_color is not None else ""
            bg_color = c.bg_color.value if c.bg_color is not None else ""
            return "".join([fg_color, bg_color, c.ascii, RESET_STYLE])

        def process_line(l: typing.Iterable[CharacterView]) -> str:
            return "".join(process_character(c) for c in l)

        to_show = "\n".join(process_line(l) for l in view.chars)
        stdscr.addstr(0, 0, to_show)

        stdscr.move(view.cursor.line - 1, view.cursor.column - 1)

        stdscr._write("\033[?25h")  # Show cursor
        stdscr.refresh()
