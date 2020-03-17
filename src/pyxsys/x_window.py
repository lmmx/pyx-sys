class Window(list):
    def __init__(self, win_id, description, name):
        self.win_id = win_id
        self.children = self
        return

    def __repr__(self):
        """
        An inheritable string representation. Prints the window type and ID.
        """
        return f"{type(self).__name__}, id: {self.win_id}"

    @staticmethod
    def check_id(win_id):
        assert win_id.startswith("0x"), "Window ID is not a hexadecimal"
        return

    def check_line_entry(self, line, prefix):
        bad_input_err_msg = f"Not a valid {type(self).__name__} line entry"
        assert line.lstrip().startswith(prefix), bad_input_err_msg
        return

    @staticmethod
    def id_from_descline(line):
        """
        Window ID is either given at the start of a line (when listed as a child)
        or in the middle of a line, after a colon (when listed as the type of window)
        """
        win_id = line.lstrip().split(":")[1].lstrip().split()[0]
        return win_id

    @property
    def win_id(self):
        return self._win_id

    @win_id.setter
    def win_id(self, win_id):
        self.check_id(win_id)
        self._win_id = win_id
        return

    @property
    def children(self):
        return self._children


class RootWindow(Window):
    def __init__(self, line):
        self.check_line_entry(line, "Root window")
        self.win_id = self.id_from_descline(line)
        return


class SourceWindow(Window):
    def __init__(self, line):
        self.check_line_entry(line, "xwininfo: Window")
        self.win_id = self.id_from_descline(line)
        return


class ParentWindow(Window):
    def __init__(self, line):
        self.check_line_entry(line, "Parent window")
        self.win_id = self.id_from_descline(line)
        return
