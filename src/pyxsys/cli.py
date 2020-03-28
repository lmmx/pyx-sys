from pyxsys.ff import read_session as read_ff_session
from xwininfo import read_xwin_tree
from wmctrl import read_wmctrl_listings as read_wm
from tmux import read_tmux_server


def main(ff_x_wm_tmux_toggle=tuple([True] * 4), ff_session_file=None, report=True):
    """
    Return the Firefox session (from the recovery.jsonlz4 in sessionstore-backups),
    the X window tree (from `xwininfo -tree -root`), the window manager's
    workspace/window mapping (from `wmctrl -d` and `wmctrl -l` respectively),
    and the current tmux server.
    """
    if report:
        print("--------------RUNNING pyxsys.cli⠶main()--------------")
    ff_toggled, x_toggled, wm_toggled, tmux_toggled = ff_x_wm_tmux_toggle
    if ff_toggled:
        ff_session = read_ff_session(session_file=ff_session_file)
    else:
        ff_session = None
    if x_toggled:
        x_tree = read_xwin_tree()
    else:
        x_tree = None
    if wm_toggled:
        wm_territory = read_wm()
    else:
        wm_territory = None
    if tmux_toggled:
        tmux_server = read_tmux_server()
    else:
        tmux_server = None
    if report:
        print("------------------COMPLETE--------------------------")
    return ff_session, x_tree, wm_territory, tmux_server
