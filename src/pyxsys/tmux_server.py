from tmux_session import list_sessions


class TmuxServer(object):
    """
    This class represents a tmux server with children that are sessions, containing
    windows (usually just 1), each with 1 or more panes.
    """

    def __init__(self):
        self.sessions = list_sessions()
        return

    def __repr__(self):
        n_s = len(self.sessions)
        n_w = len(self.windows)
        return f"TmuxServer of {n_s} sessions ({n_w} windows)"

    @property
    def sessions(self):
        return self._sessions

    @sessions.setter
    def sessions(self, session_list):
        self._sessions = session_list
        return

    @property
    def windows(self):
        """
        Return a list of all windows of all sessions (N.B. sorted numerically by
        session ID, usually window IDs will be sorted but do not always match
        their associated session ID). Windows are listed within the call to
        list_sessions in the __init__ method of this class, see tmux_session.py
        """
        all_window_lists = [s.windows for s in self.sessions]
        all_windows = [x for xs in all_window_lists for x in xs]
        return all_windows
