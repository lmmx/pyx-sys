from x_window import Window, RootWindow, SourceWindow, ParentWindow

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
        self._initialised = False
        self._header_initialised = False
        self._root_indent_offset = None
        self._open_path = None
        self._deepest_opened_level = None
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
    def initialised(self):
        return self._initialised

    def initialise(self):
        self._initialised = True
        return

    @property
    def header_initialised(self):
        return self._initialised

    def initialise_header(self):
        self._header_initialised = True
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

    @property
    def deepest_opened_level(self):
        return self.open_path.deepest_level

    @property
    def indent_step_size(self):
        return self._indent_step_size


class TreePath(list):
    """
    Class listing the levels down a particular branch of a tree, to be used to keep
    track of which 'path' has been 'opened' when adding descendants from a source node.
    For conciseness, store only the ID of each window on the branch, given as a list.
    """

    def __init__(self, branch_id_list):
        assert len(branch_id_list) > 0, "Cannot create a TreePath from an empty ID list"
        self.extend(branch_id_list)
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
        return self._deepest_level

    def deepen(self, extension_branch):
        assert len(extension_branch) > 0, "Cannot extend a TreePath with an empty list"
        self.extend(extension_branch)
        return

    def retract_levels(self, n_levels):
        assert type(n_levels) is int, TypeError("Not an integer number of levels")
        initial_d = self.deepest_level
        assert n_levels <= initial_d, f"Cannot retract {n_levels}, max. is {initial_d}"
        for n in range(n_levels):
            self.pop()
        assert initial_d - self.deepest_level == n_levels, f"Did not retract {n_levels}"
        return
