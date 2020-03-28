class PaneGeom(object):
    def __init__(self, width, height, x, y, pane_id):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.pane_id = pane_id
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
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x
        return

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y
        return

    @property
    def pane_id(self):
        return self._pane_id

    @pane_id.setter
    def pane_id(self, pid):
        self._pane_id = pid
        return


class PaneSplitGeom(object):
    def __init__(self, width, height, x, y, split_index):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.split_index = split_index
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
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x
        return

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y
        return

    @property
    def split_index(self):
        return self._split_index

    @split_index.setter
    def split_index(self, i):
        self._split_index = i
        return


class PaneDesc(PaneGeom):
    """
    Class to parse a substring (derived from a layout given by `tmux list-windows`) to
    create a PaneGeom representing a tmux pane with a width, height, position, and ID.
    """

    def __init__(self, geom_str):
        rets = self.parse_geom_str(geom_str)
        super(PaneDesc, self).__init__(*rets)
        # super(PaneDesc, self).__init__(*self.parse_geom_str(geom_str))
        return

    @staticmethod
    def parse_geom_str(geom_str):
        """
        E.g. `geom_str = "101x81,0,0,112"`
        """
        wh, x, y, pane_id = geom_str.split(",")
        width, height = wh.split("x")
        rets = width, height, x, y, pane_id
        rets = [int(val) for val in rets]
        return rets


class TmuxPane(PaneDesc):
    """
    Class for a pane as parsed from a window layout string, situated by a parent index.
    Calls the __init__ method of PaneDesc, which reads the geometry string formatted as
    "{width}x{height},{x},{y},{pane_id}" into attributes: width, height, x, y, pane_id.
    """

    def __init__(self, info_str, parent_split_index):
        self.parent_split_index = parent_split_index
        super(TmuxPane, self).__init__(info_str)
        return

    def __repr__(self):
        r = f"TmuxPane {self.pane_id} ({self.width}x{self.height} at {self.x},{self.y})"
        r += f", parent split: {self.parent_split_index}"
        return r


class PaneSplitDesc(PaneSplitGeom):
    """
    Class to parse a substring (derived from a layout given by `tmux list-windows`) to
    create a PaneSplitGeom representing a tmux pane split encompassing a width, height,
    and position (the width and height can be thought of as what the constituent panes
    took up before the split, or alternatively the size they would have as a PaneGeom
    were those constituent panes to be 'unsplit' back into a single pane).
    """

    def __init__(self, geom_str, split_index):
        super(PaneSplitDesc, self).__init__(*self.parse_geom_str(geom_str), split_index)
        return

    @staticmethod
    def parse_geom_str(geom_str):
        """
        E.g. `geom_str = "317x81,0,0"`
        """
        wh, x, y = geom_str.split(",")
        width, height = wh.split("x")
        rets = width, height, x, y
        rets = [int(val) for val in rets]
        return rets


class PaneSplit(PaneSplitDesc):
    """
    Class for a pane split as parsed from a window layout string. Calls the __init__
    method of PaneSplitDesc, which reads the geometry string formatted as
    "{width}x{height},{x},{y}" into attributes: width, height, x, y.
    """

    def __init__(self, info_str, split_index, parent_split_index):
        self.panes = []
        self.parent_split_index = parent_split_index
        super(PaneSplit, self).__init__(info_str, split_index)
        return

    def __repr__(self):
        r = f"PaneSplit {self.split_index} "
        r += f"({self.width}x{self.height} at {self.x},{self.y})"
        r += f", parent split: {self.parent_split_index}"
        return r

    @property
    def panes(self):
        return self._panes

    @panes.setter
    def panes(self, pane_list):
        self._panes = pane_list
        return

    def add_pane(self, pane):
        self.panes.extend([pane])
        return
