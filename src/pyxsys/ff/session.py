from datetime import datetime as dt
from pyxsys.ff.window import Window


class BrowserSession(object):
    def __init__(self, ss_json):
        self._windows = WindowSet(ss_json["windows"])
        self._start_time = dt.fromtimestamp(ss_json["session"]["startTime"] / 1000)
        self._selected_window = ss_json["selectedWindow"] - 1
        return

    def __repr__(self):
        n_win = len(self.windows)
        return f"BrowserSession of {n_win} windows, since {self.start_time}"

    @property
    def windows(self):
        return self._windows

    @property
    def start_time(self):
        return self._start_time


class WindowSet(list):
    """
    A class which reads the 'windows' of a Firefox recovery JSON file, and
    instantiates a set of Window classes for each of the listed entries.
    """

    def __init__(self, json_list):
        self.extend([Window(j) for j in json_list])
        return

    def __repr__(self):
        n_win = len(self)
        window_reprs = "\n\n".join([str(w) for w in self])
        return f"WindowSet of {n_win} windows\n\n{window_reprs}"
