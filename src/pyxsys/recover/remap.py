from pyxsys.wm.territory import WorkspaceTerritory as WsTerritory
from pyxsys.wm.workspace import Workspace
from pyxsys.wm.window import WorkspaceWindow as WsWindow
from subprocess import run

def recover_territory_placement(recorded, current=None):
    """
    Transform the `current` territory (which if not specified will not be examined)
    into the `recorded` territory, so as to recover a stored representation of
    window placements across workspaces.

    Both territories passed in should be `pyxsys.wm.territory⠶WorkspaceTerritory`.

    This function instantiates a `WorkspaceTerritoryRemap` event from `remap.py`.

    #TODO: if not specified, prompt to select a pickle with curses.
    """
    remapped = WorkspaceTerritoryRemap(recorded, current)
    remapped.transform_to_remap()
    return remapped

def temporary_territory_lookup(territory, d_num):
    """
    Returns the `workspace` from the territory with the given desktop number `d_num`.
    TODO: move this to be a class method on WorkspaceTerritory in pyxsys.wm.territory
    """
    for workspace in territory.workspaces:
        if workspace.number == d_num:
            return workspace

def temporary_workspace_lookup(workspace, win_id):
    """
    Checks if the `workspace` contains a window with the given ID `win_id`.
    TODO: move this to be a class method on Workspace in pyxsys.wm.workspace
    """
    has_id = any(filter(lambda x: x.win_id == win_id, workspace.windows))
    return has_id

class WorkspaceTerritoryRemap(object):
    """
    A WorkspaceTerritoryRemap (consider it as a 'remap' event) is equipped with
    a method to remap against another workspace territory. This makes it clear
    which is the source of ground truth (of the current mapping) and which is
    the destination mapping that this ground truth should be transformed to.

    This class does not need to be provided with the ground truth 'source', as it is
    implicit that this will simply be the current state of the window manager (hence
    `src` default: `None`). All that is needed is the 'destination' target, `dst`.

    If an `src` is provided, a remap will not be performed for a given window in any
    workspace if the desktop number of the window in the source territory which has
    a matching window ID is the same as that in the reference `remap` (i.e. it's
    already on the target workspace, so does not need to be moved there).
    """
    def __init__(self, dst, src=None):
        assert type(dst) is WsTerritory, f"Not a WorkspaceTerritory ({type(dst)})"
        if src is not None:
            assert type(src) is WsTerritory, f"Not a WorkspaceTerritory ({type(src)})"
        self.target_territory = dst
        self.source_territory = src
        return

    def transform_to_remap(self):
        for target_ws in self.target_territory.workspaces:
            target_d = target_ws.number
            if self.source_territory is None:
                src_ws = None
            else:
                src_ws = temporary_territory_lookup(self.source_territory, target_d)
            ws_remap = WorkspaceRemap(target_ws, src_ws)
        return

class WorkspaceRemap(object):
    def __init__(self, target, src):
        """
        `target` is a workspace in the target workspace territory, whose windows are in
        the desired locations. We want to move the windows to match this reference.

        `src` may be `None`, otherwise it is the 'ground truth' source of the equivalent
        workspace (i.e. the one with matching desktop number to `target`). If it is not
        `None` then we want to check if the windows here need moving before we make the
        call to `wmctrl` (via the `move_wm_id_to_d` function) to avoid wasting calls.

        This class stores an attribute 'remaps', which is a list of window remappings
        (represented as `WorkspaceWindowRemap` events) which were sent to the given
        desktop (the attribute `target_d`), only intended to be used to check the
        status/existence of individual `WorkspaceWindowRemap` event objects in the
        case it's unclear whether there was only partial remapping success.
        """
        assert type(target) is Workspace, f"Target is not a Workspace ({type(target)})"
        if src is not None:
            assert type(src) is Workspace, f"Source is not a Workspace ({type(src)})"
        self.target_d = target.number
        self.remaps = []
        print(f"Workspace {self.target_d}")
        for n_w, w in enumerate(target.windows):
            print(f"{n_w} Iterating over a window {w.win_id}")
            if src is not None:
                if temporary_workspace_lookup(src, w.win_id):
                    # Skip this window, it's already on the right desktop in the source
                    print(f"Skipping window: {w.desktop_number} == {self.target_d}")
                    continue
                else:
                    # Otherwise move the window to the right desktop
                    print(f"Remapping window: {w.desktop_number} => {self.target_d}")
                    self.remap(w, self.target_d)
            else:
                print(f"Trying to remap window: {w.desktop_number} => {self.target_d}")
                self.remap(w, self.target_d)
        return

    def remap(self, w, d):
        w_remap = WorkspaceWindowRemap(w, d)
        self.store_remap(w_remap)
        return

    @property
    def remaps(self):
        return self._remaps

    @remaps.setter
    def remaps(self, r):
        self._remaps = r
        return

    def store_remap(self, remap):
        self._remaps.append(remap)
        return

    @property
    def target_d(self):
        return self._d

    @target_d.setter
    def target_d(self, d):
        self._d = d
        return

class WorkspaceWindowRemap(object):
    """
    Initiate a remap event given a Workspace (pyxsys.wm.workspace⠶Workspace) and
    a desktop number. A remap event is a call to `wmctrl` to move the window
    using its ID (this is handled by the function `move_wm_id_to_d`).
    """
    def __init__(self, w, d_num):
        assert type(w) is WsWindow, f"This is not a WorkspaceWindow ({type(w)})"
        self.remap_win_id = w.win_id
        self.target_desktop = d_num
        self.move()
        return

    def move(self):
        move_wm_id_to_d(self.remap_win_id, self.target_desktop)
        return

    @property
    def remap_win_id(self):
        return self._remap_win_id

    @remap_win_id.setter
    def remap_win_id(self, win_id):
        self._remap_win_id = win_id
        return

    @property
    def target_desktop(self):
        return self._target_d

    @target_desktop.setter
    def target_desktop(self, d_num):
        self._target_d = d_num
        return

def move_wm_id_to_d(wm_id, d_num):
    """
    Given a wmctrl window manager ID `wm_id`, move the corresponding window to the
    desktop number `d_num`, by calling `wmctrl -i -r WM_ID  -t D_NUM`.
    
    N.B. wmctrl does not give an informative error code so no way to check it succeeded
    without querying wmctrl again for the ID to verify that its desktop number has
    successfully updated to the target `d_num` (this function doesn't handle that yet).
    """
    wmctrl_cmd = f"wmctrl -i -r {wm_id} -t {d_num}".split()
    print(f"Moving {wm_id} to {d_num}")
    run(wmctrl_cmd)
    return
