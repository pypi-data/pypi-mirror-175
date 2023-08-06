"""
When reading from stdin, if we want to be efficient, we need to read without cache and fast.
That's why we want to read stdin in a raw mode, but this messes with the stdin and the terminal doesn't like that.
"""
import contextlib
import subprocess
import sys

from vim_quest_cli.deps.is_js import IS_JS

if not IS_JS:
    import termios
    import tty


@contextlib.contextmanager
def with_stdin_raw():
    try:
        with contextlib.suppress(termios.error):
            tty.setraw(sys.stdin)
        yield
    finally:
        with contextlib.suppress(termios.error):
            tty.setraw(sys.stdin)  # Doesn't really works.
        # Should have a way of doing that in python, but maybe for later.
        subprocess.check_call(["stty", "sane"])
