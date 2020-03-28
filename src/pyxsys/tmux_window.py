from subprocess import run
from tmux_pane import TmuxPane, PaneSplit


def list_window_formats():
    window_formats = [
        "session_id",
        "window_id",
        "window_name",
        "window_width",
        "window_height",
        "window_layout",
        "window_panes",
        "window_index",
        "window_active",
        "session_attached",
    ]
    return window_formats


def list_windows(attached_only=True, numeric_id_sort=True):
    """
    Return a list of TmuxWindow instances created by parsing the output of
    `tmux list-windows`.
    """
    pre_str = "#{"
    post_str = "}"
    s_formats = [f"{pre_str}{x}{post_str}" for x in list_window_formats()]
    format_string = "\t".join(s_formats)
    tmux_args = ["tmux", "list-windows", "-a", "-F", format_string]
    result = run(tmux_args, capture_output=True)
    assert result.returncode == 0, f"`{' '.join(tmux_args)}'` failed.\n{result.stderr}"
    windows_str = result.stdout.decode()
    window_list = []
    for line in windows_str.split("\n"):
        if line == "":
            continue
        window = parse_window_line(line)
        if attached_only:
            if not window.is_attached:
                continue
        window_list.append(window)
    if numeric_id_sort:
        window_list = sorted(window_list, key=lambda x: int(x.win_id.lstrip("@")))
    return window_list


def parse_window_line(line):
    """
    Instantiate a TmuxWindow object from the TSV returned by `tmux list-sessions`.
    """
    window = TmuxWindow(*line.split("\t"))
    return window


class TmuxWindow(object):
    def __init__(
        self,
        session_id,
        win_id,
        win_name,
        w_w,
        w_h,
        w_layout,
        n_panes,
        win_index,
        is_active,
        is_attached,
    ):
        self.session_id = session_id
        self.win_id = win_id
        self.name = win_name
        self.width = int(w_w)
        self.height = int(w_h)
        self.layout = LayoutDesc(w_layout)
        self.n_panes = int(n_panes)
        self.index = int(win_index)
        self.is_active = bool(int(is_active))
        self.is_attached = bool(int(is_attached))
        return

    def __repr__(self):
        r = f"TmuxWindow {self.win_id} (session {self.session_id}, #{self.index})"
        r += f" {self.name} "
        r += f"~ {self.width}x{self.height} [{self.layout}], "
        if not self.is_active:
            r += f"in"
        r += f"active, "
        if not self.is_attached:
            r += f"not"
        r += f"attached"
        return r


class TmuxWindowLayout(object):
    def __init__(self, layout_id, pane_geom_tree):
        self.id = layout_id
        self.pane_geom_tree = pane_geom_tree
        return


class LayoutDesc(TmuxWindowLayout):
    def __init__(self, layout_str):
        super(LayoutDesc, self).__init__(*self.parse_layout_str(layout_str))
        return

    @staticmethod
    def parse_layout_str(layout_str):
        """
        E.g. layout_str = "a455,317x81,0,0{101x81,0,0,112,215x81,102,0[215x22,102,0,
                           113,215x58,102,23{24x58,102,23,114,190x58,127,23,125}]}"

        Which represents a layout with ID 'a455', beginning with a horizontal split
        containing a pane with ID 112, which is itself split vertically, containing
        a pane with ID 113, and this pane is in turn itself split horizontally and
        contains two panes with IDs 114 and 125.
        """
        layout_id = layout_str.split(",")[0]
        panes_str = layout_str[len(layout_id) + 1 :]
        pane_geom_tree = parse_pane_geom_tree(panes_str)
        return layout_id, pane_geom_tree

    def __repr__(self):
        pane_tree_repr = f"{self.pane_geom_tree}".lstrip("PaneTree of ")
        return f"{self.id}::{pane_tree_repr}"


def parse_pane_geom_tree(panes_str):
    panes_str = panes_str.replace("{", "{{{").replace("}", "}}}")
    panes_str = panes_str.replace("[", "[[[").replace("]", "]]]")
    p_split = [x for xs in [x.split("}}") for x in panes_str.split("{{")] for x in xs]
    p_split = [x for xs in [x.split("[[") for x in p_split] for x in xs]
    p_split = [x for xs in [x.split("]]") for x in p_split] for x in xs]
    p_split_processed = []
    for (i, x) in enumerate(p_split):
        if x.startswith("[") or x.startswith("{"):
            p_split_processed[i - 1] += x[0]
            p_split_processed.append(x[1:])
        else:
            p_split_processed.append(x)
    open_index = -1
    split_index_path = []
    pane_list = []
    pane_split_list = []
    for p in p_split_processed:
        opening_h, opening_v = [p.endswith(x) for x in ("{", "[")]
        closing_h, closing_v = [p.startswith(x) for x in ("}", "]")]
        if closing_v or closing_h:
            split_closer = p[0]
            p = p.lstrip(f"{split_closer},")
            split_index_path.pop()
        #######################
        n_csv = 4  # Number of comma-separated values in a pane description
        if opening_v or opening_h:
            split_opener = p[-1]
            # the last 3 comma-separated values describe the new pane split, omit them
            p = p.rstrip(split_opener)
            panes_csv = p.split(",")[:-3]
        else:
            panes_csv = p.split(",")
        pane_it = range(len(panes_csv) // n_csv)  # iterator to take 4 CSV at a time
        pane_descs = [panes_csv[n_csv * i : n_csv * (i + 1)] for i in pane_it]
        if len(split_index_path) > 0:
            current_split_i = split_index_path[-1]
        else:
            # This only happens if there are no splits i.e. window only has one pane
            current_split_i = None
        for pane_desc_4_tuple in pane_descs:
            pane_info = ",".join(pane_desc_4_tuple)
            pane = TmuxPane(pane_info, parent_split_index=current_split_i)
            pane_list.append(pane)
        if opening_v or opening_h:
            # Increment the split index for the new PaneSplit being opened
            open_index += 1
            if open_index > 0:
                parent_split_index = split_index_path[-1]
            else:
                parent_split_index = None
            split_index_path.append(open_index)
            split_desc_3_tuple = p.split(",")[-3:]
            pane_split_info = ",".join(split_desc_3_tuple)
            ps = PaneSplit(pane_split_info, open_index, parent_split_index)
            pane_split_list.append(ps)
    pane_tree = PaneTree(pane_split_list, pane_list)
    #pane_tree = {"splits": pane_split_list, "panes": pane_list}
    return pane_tree

class PaneTree(object):
    def __init__(self, splits, panes):
        self.splits = splits
        if len(splits) > 0:
            for pane in panes:
                self.assign_pane(pane, to_split = pane.parent_split_index)
            self.root_pane = None
        else:
            assert len(panes) == 1, ValueError(f"Expected panes to be just one pane")
            self.root_pane = panes[0]
        return

    def __repr__(self):
        n_splits = len(self.splits)
        split_str = f"{n_splits} split"
        if n_splits != 1:
            split_str += "s"
        n_panes = len(self.panes)
        pane_str = f"{n_panes} pane"
        if n_panes > 1:
            pane_str += "s"
        r = f"PaneTree of {pane_str} in {split_str}"
        return r
    
    @property
    def splits(self):
        return self._splits

    @splits.setter
    def splits(self, split_list):
        self._splits = split_list
        return
    
    @property
    def root_pane(self):
        return self._root_pane

    @root_pane.setter
    def root_pane(self, p):
        self._root_pane = p
        return

    @property
    def panes(self):
        if self.root_pane is None:
            list_of_pane_lists = [s.panes for s in self.splits]
            pane_list = [x for xs in list_of_pane_lists for x in xs]
        else:
            pane_list = [self.root_pane]
        return pane_list

    def assign_pane(self, pane, to_split):
        for split in self.splits:
            if split.split_index == to_split:
                split.add_pane(pane)
                return
        raise ValueError(f"No split has split index {to_split}")
