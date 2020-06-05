# pyx-sys

A library for storage and restore of system state in terms of windows and workspaces

> _pyxis_ is the Latin name for [the box housing a mariner's compass](https://www.constellationsofwords.com/Constellations/Pyxis.htm).
> This name also relates to the 'box tree' (_Buxus sempervirens_), whose wood is a source of buxine, a steroid alkaloid used to treat fever.
> In a similar vein, this library aims to be an elaborate cabinet for process-centric storage of all the components that make up a
> developer's workflow, to assist in the shutting down of a system in use and restoring its workflow to the same state it was in before.

## Requirements

- dejsonlz4 (GitHub: [avih/dejsonlz4](https://github.com/avih/dejsonlz4))
  - Used to decompress recovery JSON of Firefox browser state (windows, tabs, recent history)
- Linux
  - For use with Mac/Windows, I'd need to see their Firefox `sessionstore-backups` location
- X window system (`xwininfo` must be called to retrieve the list of windows)
- `wmctrl` (determine workspaces the windows are in through the window manager)
- `tmux` (to obtain listings of terminal windows, any splits/resultant panes, and activities therein)

## Capabilities

- [x] Access the `xwininfo` tree, stored as a `WindowTree` class with a `children` attribute that can be walked
      to enumerate all windows on the system.
  - [ ] Modify and activate particular windows in the tree using `wmctrl` given their ID
  - [x] Cross-reference to the workspace listing
- [x] Access the `wmctrl` workspace listing, stored as a `WorkspaceTerritory` class with a `sticky_windows` attribute
      containing the desktop windows and a `workspaces` attribute, each of which has a `windows` attribute that lists
      all windows in that workspace
  - [x] Connect window IDs to those in the `WindowTree` from `xwininfo` (differ by one hex digit)
  - [x] Restore windows to a workspace from a pickled `WorkspaceTerritory` on disk
- [x] List Firefox window/tab list which can be cross-referenced to the X window/workspace list
  - [ ] Store the list of windows/tabs
  - [ ] Cross-reference to the X window/workspace list
- [x] List tmux terminal session list (e.g. which text files are open in vim, command line paths, etc.)
  - [ ] cross-reference to X window/workspace list

## Rationale

- In part, the purpose is to catalogue and archive tabs being viewed rather than have this be standalone logs
  - The goal is to feed into these logs and for their use to also be fed from a mobile app
- Initially however, the goal is to provide session restore for as many components of the developer workflow as possible
  - especially so as to keep associated activities (e.g. doc reading in a browser alongside app development in a terminal)
    recorded together.
  - Partly this is for session restore, however it may also be used for 'reference restore', i.e. restore at a later date,
    (for instance when returning to work on a particular feature and opening both the code files and the docs together).

## Current workflow

When the module is run (`python3 -im pyxsys` from the `src/` directory), `__main__.py` calls `cli.py` and finally
adds four local variables to the Python environment:

- `ff_session` — `pyxsys.ff.session`⠶`BrowserSession` class representing a Firefox browser's state (excluding incognito windows)
- `x_session` — `pyxsys.x.tree`⠶`WindowTree` class representing the X window manager's listing of windows in the active session
- `wm_territory` — `pyxsys.wm.territory`⠶`WorkspaceTerritory` class representing the `wmctrl`-derived window manager set of workspaces 
  (which I term a 'territory' following the notion of _Zubin spaces_ from the GIS research literature on "spatial information theory")
- `tmux_server` — `pyxsys.tm.server`⠶`TmuxServer` class representing the currently running tmux instance, all terminals across
  all windows/workspaces, and listing relevant information about all panes within them.

They look something like this:

```
>>> ff_session
BrowserSession of 11 windows, since 2020-03-05 16:48:39.172000
>>> x_session
WindowTree (rooted at RootWindow, id: 0x13f, (has no name))
>>> wm_territory
WorkspaceTerritory of 9 workspaces (30 windows)
>>> tmux_server
TmuxServer of 15 sessions (15 windows)
```

I'm currently working on finishing off the finer details of these classes, and aim to make them 'work together',
i.e. cross-reference their IDs and related activities.

## Read more

- Wiki ⠶ [Firefox profiles](wiki/Firefox_profiles.md)

## Sources

- Initial spark for this project was these 2 Q&A posts:
  - [Is there a dynamic-multiple-monitor friendly desktop environment available for Ubuntu?](https://askubuntu.com/questions/411503/is-there-a-dynamic-multiple-monitor-friendly-desktop-environment-available-for-u)
  - [How can I save/restore window positions when I undock/dock my laptop?](https://unix.stackexchange.com/questions/59908/how-can-i-save-restore-window-positions-when-i-undock-dock-my-laptop)
