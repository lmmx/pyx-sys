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

## Capabilities

- [x] Access the `xwininfo` tree, stored as a `WindowTree` class with a `children` attribute that can be walked
      to enumerate all windows on the system.
  - [ ] Modify and activate particular windows in the tree using `wmctrl` given their ID
  - [ ] Cross-reference to the workspace listing (TODO: find where this is stored)
- [x] List Firefox window/tab list which can be cross-referenced to the X window/workspace list
  - [ ] Store the list of windows/tabs
  - [ ] Cross-reference to the X window/workspace list
- [ ] List and store terminal locations and tmux config, cross-reference to X window/workspace list

## Rationale

- In part, the purpose is to catalogue and archive tabs being viewed rather than have this be standalone logs
  - The goal is to feed into these logs and for their use to also be fed from a mobile app
- Initially however, the goal is to provide session restore for as many components of the developer workflow as possible
  - especially so as to keep associated activities (e.g. doc reading in a browser alongside app development in a terminal)
    recorded together.
  - Partly this is for session restore, however it may also be used for 'reference restore', i.e. restore at a later date,
    (for instance when returning to work on a particular feature and opening both the code files and the docs together).

## Read more

- Wiki ⠶ [Firefox profiles](wiki/Firefox_profiles.md)
