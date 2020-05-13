from pyxsys.firefox import read_session as read_ff_session
from pyxsys.xwininfo import read_xwin_tree
from pyxsys.wmctrl import read_wmctrl_listings as read_wm
from pyxsys.tmux import read_tmux_server
from pyxsys.recover.unpickling import unpickle_vars
from pyxsys.recover.remap import recover_territory_placement
from sys import _getframe as sys_frame

def main(ff_x_wm_tmux_toggle=tuple([True] * 4), ff_session_file=None, wm_territory_file=None, report=True):
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
    if x_tree is not None and wm_territory is not None:
        wm_territory.xref_x_session(x_tree)
    if wm_territory_file is not None:
        unpickle_vars(wm_territory_file, frame=sys_frame(0))
        rec_wmt = sys_frame(0).f_locals["wm_territory_recorded"]
        wm_remap = recover_territory_placement(rec_wmt, wm_territory)
    else:
        wm_remap = None
    if report:
        print("------------------COMPLETE--------------------------")
    return ff_session, x_tree, wm_territory, tmux_server, wm_remap
