from subprocess import run
from datetime import datetime as dt
from tmux_window import list_windows


def list_session_formats():
    session_formats = [
        "session_id",
        "session_windows",
        "session_width",
        "session_height",
        "session_created",
        "session_attached",
    ]
    return session_formats


def list_sessions(attached_only=True, numeric_id_sort=True):
    """
    Return a list of TmuxSession instances created by parsing the output of
    `tmux list-sessions`.
    """
    pre_str = "#{"
    post_str = "}"
    s_formats = [f"{pre_str}{x}{post_str}" for x in list_session_formats()]
    format_string = "\t".join(s_formats)
    result = run(["tmux", "list-sessions", "-F", format_string], capture_output=True)
    assert result.returncode == 0, f"'tmux list-sessions' failed.\n{result.stderr}"
    session_str = result.stdout.decode()
    session_list = []
    for line in session_str.split("\n"):
        if line == "":
            continue
        session = parse_session_line(line)
        if attached_only:
            if not session.is_attached:
                continue
        session_list.append(session)
    if numeric_id_sort:
        session_list = sorted(session_list, key=lambda x: int(x.session_id.lstrip("$")))
    window_list = list_windows()
    for w in window_list:
        for s in session_list:
            if s.session_id == w.session_id:
                s.add_window(w)
                break
    return session_list


def parse_session_line(line):
    """
    Instantiate a TmuxSession object from the TSV returned by `tmux list-sessions`.
    """
    session = TmuxSession(*line.split("\t"))
    return session


class TmuxSession(object):
    def __init__(self, session_id, n_windows, s_w, s_h, created, is_attached):
        self.session_id = session_id
        self.n_windows = int(n_windows)
        self.width = int(s_w)
        self.height = int(s_h)
        self.created = dt.fromtimestamp(int(created))
        self.is_attached = bool(int(is_attached))
        self.windows = []
        return

    def __repr__(self):
        geom_str = f"{self.width}x{self.height}"
        return f"Session {self.session_id} with {self.n_windows} windows ({geom_str})"

    @property
    def windows(self):
        return self._windows

    @windows.setter
    def windows(self, window_list):
        self._windows = window_list
        return

    def add_window(self, win):
        self.windows.extend([win])
        return
