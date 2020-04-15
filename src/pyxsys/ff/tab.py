from datetime import datetime as dt


class TabSet(list):
    """
    A class representing a list of tabs inside a window.
    """

    def __init__(self, json_list):
        self.extend([Tab(j) for j in json_list])
        return

    def __repr__(self):
        return "\n".join([f"{i} ⠶ {x}" for i, x in enumerate(self)])


class Tab(object):
    def __init__(self, json):
        self._history = TabHistoryChain(json["entries"])
        self._last_accessed = dt.fromtimestamp(json["lastAccessed"] / 1000)
        # TODO: FIX - Commented out as it was giving an error when reading in the file
        # self._index = json["index"] - 1
        self._icon = json["image"]
        return

    def __repr__(self):
        return f"{self.current_state} ({self.index + 1}/{len(self.history)})"

    @property
    def history(self):
        return self._history

    @property
    def last_accessed(self):
        return self._last_accessed

    @property
    def index(self):
        return self._index

    @property
    def current_state(self):
        return self.history[self.index]

    @property
    def icon(self):
        return self._icon


class TabHistoryChain(list):
    """
    Stores the history of a given tab as a list of TabState objects (chronological).
    """

    def __init__(self, json_list):
        self.extend([TabState(j) for j in json_list])
        return


class TabState(object):
    """
    Represent the state of a tab in a TabHistoryChain (i.e. one entry in the history
    of a particular tab): its URL and title. I don't need other attributes from here
    at the time of writing but could in future (e.g. values for "ID" and "persist").
    """

    def __init__(self, json):
        self._url = json["url"]
        self._title = json["title"]
        return

    def __repr__(self):
        return f'["{self.url}" -> "{self.title}"]'

    @property
    def url(self):
        return self._url

    @property
    def title(self):
        return self._title
