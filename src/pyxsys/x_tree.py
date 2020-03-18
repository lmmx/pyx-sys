from x_window import ChildWindow, RootWindow, SourceWindow

class WindowTree(object):
    def __init__(self):
        """
        Each call to `xwininfo -tree` will return:
        
        - a 'source' window (first line of output), which is the node that was queried,
          e.g. when called with the `-root` flag, the source will be the root and
          subsequently make the WindowTree a "root tree" (i.e. the source window ID
          matches the root window ID).
        - a 'root' window (first line of indented output, indented by 2 spaces)
        - a 'parent' window (specifically it is the parent of the source window

        This class is to be initialised 'empty' and then completed by adding these
        attributes upon reading the lines of the output. It is possible to check if
        the class has been 'completed' by checking if the value of 
        """
        self._source = None
        self._root = None
        self._source_initialised = False
        self._root_initialised = False
        self._root_indent_offset = None
        self._open_path = None
        self._deepest_open_level = None
        self._indent_step_size = 3
        return

    def __repr__(self):
        if self.root.win_id == self.source.win_id:
            return "WindowTree (unrooted)"
        else:
            return "WindowTree (root: {self.root})"

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, root_node):
        self._root = root_node
        return

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, source_node):
        self._source = source_node
        return

    @property
    def source_initialised(self):
        return self._source_initialised

    def initialise_source(self, source_line):
        self.source = SourceWindow(source_line)
        assert self.open_path is None, "Expected no open path on uninitialised tree"
        self.open_path = TreePath([self.source])
        self._source_initialised = True
        return

    @property
    def root_initialised(self):
        return self._root_initialised

    def initialise_root(self, root_line, root_line_indent):
        self.root = RootWindow(root_line)
        assert self.root.win_id != "0x0", ValueError("Cannot root a tree at NULL")
        self.root_indent_offset = root_line_indent  # it's 2, but do not hard code this
        self._root_initialised = True
        return

    @property
    def root_indent_offset(self):
        return self._root_indent_offset

    @root_indent_offset.setter
    def root_indent_offset(self, offset):
        self._root_indent_offset = offset
        return

    @property
    def open_path(self):
        return self._open_path

    @open_path.setter
    def open_path(self, path):
        self._open_path = path
        return

    @property
    def deepest_open_level(self):
        return self.open_path.deepest_level

    def retract_to_level(self, target_level):
        level_step = self.deepest_open_level - target_level
        self.open_path.retract_levels(level_step)
        return

    @property
    def indent_step_size(self):
        return self._indent_step_size


class TreePath(list):
    """
    Class listing the levels down a particular branch of a tree, to be used to keep
    track of which 'path' has been 'opened' when adding descendants from a source node.
    For conciseness, store only the ID of each window on the branch, given as a list.
    """

    def __init__(self, window_list):
        assert len(window_list) > 0, "Cannot create TreePath from empty window list"
        self.extend(window_list)
        self._deepest_level = len(self) - 1
        self._deepest_node = self[-1]
        return

    def __repr__(self):
        n_id = len(self)
        return f"TreePath of {n_id} IDs, deepest level {self.deepest_level}:\n{self}"

    @property
    def deepest_level(self):
        self._deepest_level = len(self) - 1
        return self._deepest_level

    @property
    def deepest_node(self):
        self._deepest_node = self[-1]
        return self._deepest_node

    @property
    def deepest_parent(self):
        if self.deepest_level < 1:
            return None
        else:
            self._deepest_parent = self[-2]
        return self._deepest_parent

    def deepen(self, child_window_line):
        """
        Extend the open path on the tree by providing a Window object (TODO: store on
        the path by its ID only), while its parent (i.e. prior node on the TreePath)
        window will have the extension window added as a child node.
        """
        extension_window = ChildWindow(child_window_line)
        # assert Window in type(extension_window).mro(), "TreePath.deepen takes a Window"
        self.deepest_node.add_children([extension_window])
        self.extend([extension_window])
        return

    def continue_level(self, sibling_window_line):
        """
        Extend the open path on the tree by providing a Window object (TODO: store on
        the path by its ID only), while its parent (i.e. prior node on the TreePath)
        window will have the extension window added as a child node. Unlike deepen,
        this method is used when the level has already been begun (i.e. adding a sibling
        at the level of a previous child rather than a new level of children).
        """
        extension_window = ChildWindow(sibling_window_line)
        # assert Window in type(extension_window).mro(), "TreePath.deepen takes a Window"
        assert self.deepest_level > 0, "No parent windows: path has only one window"
        self.deepest_parent.add_children([extension_window])
        self.pop()
        self.extend([extension_window])
        return

    def retract_levels(self, n_levels):
        assert type(n_levels) is int, TypeError(f"{n_levels} not an integer of levels")
        initial_d = self.deepest_level
        assert n_levels < initial_d, f"Cannot retract {n_levels}, max. is {initial_d}"
        for n in range(n_levels):
            self.pop()
        assert initial_d - self.deepest_level == n_levels, f"Did not retract {n_levels}"
        return
