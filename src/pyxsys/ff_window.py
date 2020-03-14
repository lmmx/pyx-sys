from ff_tab import TabSet

class Window(object):
    """
    A class representing an individual entry in the 'windows' list of a Firefox session
    recovery JSON file. It contains a TabSet class and information about selected tab,
    whether the window is maximised, the z-index of the window, and a WindowGeom class
    (which describes the size of the window and its position on the screen).
    """

    def __init__(self, json):
        self._tabs = TabSet(json["tabs"])
        self._selected_tab = json["selected"] - 1
        self._sizemode = json["sizemode"]
        self._z_index = json["zIndex"]
        self._geom = WindowGeom(
            json["width"], json["height"], json["screenX"], json["screenY"]
        )
        return

    @property
    def tabs(self):
        return self._tabs

    @property
    def selected_tab(self):
        return self._selected_tab

    @property
    def sizemode(self):
        return self._sizemode

    @property
    def z_index(self):
        return self._z_index

    @property
    def geom(self):
        return self._geom


class WindowGeom(object):
    """
    A class for concise representation of a window's geometry (size, screen position).
    """

    def __init__(self, width, height, screen_x, screen_y):
        self._width = width
        self._height = height
        self._x = screen_x
        self._y = screen_y
        return

    def __repr__(self):
        return f"WindowGeom: {self.width} x {self.height} at ({self.x}, {self.y})"

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y
