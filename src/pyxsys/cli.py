from pyxsys.ff import read_session
from xwininfo import read_xwin_tree
from wmctrl import read_wmctrl_listings as read_wm

def main(ff_session_file=None, report=True):
    """
    Return the Firefox session (from the recovery.jsonlz4 in sessionstore-backups),
    the X window tree (from `xwininfo -tree -root`), and the window manager's
    workspace/window mapping (from `wmctrl -d` and `wmctrl -l` respectively)
    """
    if report:
        print("--------------RUNNING pyxsys.cli⠶main()--------------")
    ff_session = read_session(session_file=ff_session_file, report=report)
    x_tree = read_xwin_tree()
    wm_territory = read_wm()
    if report:
        print("------------------COMPLETE--------------------------")
    return ff_session, x_tree, wm_territory
