from subprocess import run
from shutil import which
from pyxsys.tm.server import TmuxServer


def read_tmux_server():
    """
    Read all of the tmux server's windows and their panes into a single representation.
    """
    assert which("tmux") is not None, "tmux not found, please install it"
    tmux_server = TmuxServer()
    return tmux_server
