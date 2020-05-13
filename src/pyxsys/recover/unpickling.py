import pickle
from pathlib import Path

def unpickle_vars(pkl, frame, name_affix="_recorded", as_suffix=True):
    """
    Given a stored pickle (`pkl`, expected to be a path to a file that exists),
    containing the four variables:

        [ff_session, x_session, wm_territory, tmux_server]

    in that order (though they are allowed to be stored as `None`), load these
    variables back into the namespace above with a suffix (or prefix if
    `as_suffix` is False [default: True]), given as `name_affix` (default: "_recorded")

    The `frame` argument should be invoked with `sys._getframe(0)` at the point of use.
    """
    with open(pkl, "rb") as f:
        rets = pickle.load(f)
    checklist = ["ff_session", "x_session", "wm_territory", "tmux_server"]
    if as_suffix:
        storables = [f"{x}{name_affix}" for x in checklist]
    else:
        storables = [f"{name_affix}{x}" for x in checklist]
    for i, var_name in enumerate(storables):
        frame.f_locals[var_name] = rets[i]
    return
