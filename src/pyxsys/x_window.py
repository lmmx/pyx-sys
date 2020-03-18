class Window(list):
    def __init__(self, win_id, name, geom=None):
        self.win_id = win_id
        self.name = name
        self.geom = geom
        self._children = list()
        return

    def __repr__(self):
        """
        An inheritable string representation. Prints the window type and ID.
        """
        if self.name is None:
            name_repr = "(has no name)"
        else:
            name_repr = f'"{self.name}"'
        n_children = len(self.children)
        if n_children == 1:
            child_repr = f"\n1 child window: {self.children}"
        elif n_children > 1:
            child_repr = f"\n{n_children} child windows: {self.children}"
        else:
            child_repr = ""
        return f"{type(self).__name__}, id: {self.win_id} {name_repr}{child_repr}"

    @staticmethod
    def check_id(win_id):
        assert win_id.startswith("0x"), "Window ID is not a hexadecimal"
        return

    def check_line_entry(self, line, prefix):
        bad_input_err_msg = f"Not a valid {type(self).__name__} line entry"
        assert line.lstrip().startswith(prefix), bad_input_err_msg
        return

    @property
    def win_id(self):
        return self._win_id

    @win_id.setter
    def win_id(self, win_id):
        self.check_id(win_id)
        self._win_id = win_id
        return

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
        return

    @property
    def children(self):
        return self._children

    def add_children(self, subnode_list):
        self.children.extend(subnode_list)
        return

    @property
    def geom(self):
        return self._geom

    @geom.setter
    def geom(self, geom):
        self._geom = geom
        return


class WindowGeom(object):
    """
    TODO: structure this class to represent window geometry (for now it only applies
    to the SubnodeDesc class, which is given on the lines of xwininfo output which
    describe the children of another node, so no need to add to base Window class).
    """

    def __init__(self, width, height, abs_x, abs_y, rel_x, rel_y):
        self.width = width
        self.height = height
        self.abs_x = abs_x
        self.abs_y = abs_y
        self.rel_x = rel_x
        self.rel_y = rel_y
        return

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, w):
        self._width = w
        return

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, h):
        self._height = h
        return

    @property
    def abs_x(self):
        return self._abs_x

    @abs_x.setter
    def abs_x(self, abs_x):
        self._abs_x = abs_x
        return

    @property
    def abs_y(self):
        return self._abs_y

    @abs_y.setter
    def abs_y(self, abs_y):
        self._abs_y = abs_y
        return

    @property
    def rel_x(self):
        return self._rel_x

    @rel_x.setter
    def rel_x(self, rel_x):
        self._rel_x = rel_x
        return

    @property
    def rel_y(self):
        return self._rel_y

    @rel_y.setter
    def rel_y(self, rel_y):
        self._rel_y = rel_y
        return


class WindowDesc(Window):
    def __init__(self, line):
        super(WindowDesc, self).__init__(*self.parse_descline(line))
        return

    @staticmethod
    def parse_descline(line):
        """
        Window ID is given in the middle of a line, after a colon (window type format),
        followed by the window's name (if any).
        """
        win_id = line.lstrip().split(":")[1].lstrip().split()[0]
        if line.endswith("(has no name)") or win_id == "0x0":
            name = None
        else:
            assert line.count('"') > 1, ValueError("Missing enclosing quotation marks")
            first_quote = line.find('"')
            assert line.endswith('"'), ValueError("Expected quotation mark at EOL")
            name = line[first_quote + 1 : -1]
        return win_id, name


class SourceWindow(WindowDesc):
    def __init__(self, line):
        self.check_line_entry(line, "xwininfo: Window")
        # Remove xwininfo output prefix before processing line for ID and window name
        super(SourceWindow, self).__init__(line[line.find(":") + 1 :])
        return

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent
        return

    def assign_parent(self, parent_line):
        self.parent = ParentWindow(parent_line)


class RootWindow(WindowDesc):
    def __init__(self, line):
        self.check_line_entry(line, "Root window")
        super(RootWindow, self).__init__(line)
        return


class ParentWindow(WindowDesc):
    def __init__(self, line):
        self.check_line_entry(line, "Parent window")
        super(ParentWindow, self).__init__(line)
        return


class SubnodeDesc(Window):
    def __init__(self, line):
        super(SubnodeDesc, self).__init__(*self.parse_descline(line))
        return

    @staticmethod
    def parse_descline(line):
        """
        Window ID is given at the start of a line (child window format), then
        the window's name, then a colon, then a bracketed set of window tags,
        then window width and height, then absolute and relative window positions.
        """
        win_id = line.lstrip().split()[0]
        tag_open_br = 0 - line[::-1].find("(")
        tag_close_br = -1 - line[::-1].find(")")
        tags = [x.strip('"') for x in line[tag_open_br:tag_close_br].split()]
        if line.split(":")[0].endswith("(has no name)"):
            name = None
        else:
            assert line.count('"') > 1, ValueError("Missing enclosing quotation marks")
            name_open_qm = line.find('"')
            name_close_qm = tag_open_br - line[:tag_open_br][::-1].find(":") - 1
            name = line[name_open_qm:name_close_qm].strip('"')
        geom = WindowGeom(*SubnodeDesc.parse_geomline(line[tag_close_br + 1 :]))
        return win_id, name, geom

    @staticmethod
    def parse_geomline(line):
        w_h_abs, rel = line.lstrip().split()
        width = w_h_abs.split("x")[0]
        height, abs_x, abs_y = w_h_abs.split("x")[1].split("+")
        rel_x, rel_y = rel.split("+")[-2:]
        return width, height, abs_x, abs_y, rel_x, rel_y


class ChildWindow(SubnodeDesc):
    def __init__(self, line):
        self.check_line_entry(line, "0x")
        super(ChildWindow, self).__init__(line)
        return
