class Window(list):
    def __init__(self, win_id, name):
        self.win_id = win_id
        self.name = name
        self.children = self
        return

    def __repr__(self):
        """
        An inheritable string representation. Prints the window type and ID.
        """
        if self.name is None:
            name_repr = "(has no name)"
        else:
            name_repr = f'"{name}"'
        return f"{type(self).__name__}, id: {self.win_id} {name_repr}"

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

    @children.setter
    def children(self, vals):
        self._children = vals
        return


class WindowDesc(Window):
    def __init__(self, line):
        super(WindowDesc, self).__init__(*self.parse_descline(line))
        return

    @staticmethod
    def parse_descline(line):
        """
        Window ID is either given at the start of a line (when listed as a child)
        or in the middle of a line, after a colon (when listed as the type of window)
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
        self.parent = ParentWindow(line)


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
