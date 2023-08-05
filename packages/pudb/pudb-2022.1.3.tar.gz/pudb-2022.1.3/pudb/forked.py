import sys
import os

from pudb.debugger import Debugger


def set_trace(paused=True, frame=None, term_size=None):
    """Set a breakpoint in a forked process on Unix system, e.g. Linux & MacOS.
    In- and output will be redirected to /dev/stdin & /dev/stdout.
    You can call pudb.forked.set_trace() directly or
    use it with python's built-in breakpoint():
    PYTHONBREAKPOINT=pudb.forked.set_trace python …
    """
    if frame is None:
        frame = sys._getframe().f_back
    if term_size is None:
        try:
            # Getting terminal size
            s = os.get_terminal_size()
            term_size = (s.columns, s.lines)
        except Exception:
            term_size = (80, 24)

    Debugger(
        stdin=open("/dev/stdin"),
        stdout=open("/dev/stdout", "w"),
        term_size=term_size,
    ).set_trace(frame, paused=paused)
