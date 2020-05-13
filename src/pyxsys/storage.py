import pickle
from pathlib import Path
from datetime import datetime as dt

def storage_timestamp(t=dt.now(), storage_dir=Path.home() / ".pyx_store", ext="p"):
    """
    Return a timestamp now suitable to create a file path as:
    
        yy/mm/dd/hh-mm-ss

    By default under `~/.pyx_store/` (`storage_dir`) with file extension `.p` (`ext`):

        ~/.pyx_store/yy/mm/dd/hh-mm-ss.p
    
    Assuming you will never pickle a workspace representation more than once per second,
    this can be used as a path into `~/.pyx_store/yy/mm/dd/hh_mm_ss`.
    """
    assert type(t) is dt, TypeError("Time isn't a datetime.datetime instance")
    datestamp, timestamp = t.isoformat().split("T")
    datestamp = datestamp.replace("-", "/")
    timestamp = timestamp[:timestamp.find(".")].replace(":", "-")
    subpath = storage_dir / Path(datestamp)
    storage_path = storage_dir / subpath
    storage_path.mkdir(parents=True, exist_ok=True)
    file_name = f"{timestamp}.{ext}"
    return storage_path / file_name

def pickle_vars(local_names=vars()):
    checklist = ["ff_session", "x_session", "wm_territory", "tmux_server"]
    pickle_filepath = storage_timestamp() # Create a dir for today's date under ~/.pyx_store/
    storables = []
    for var_name in checklist:
        if var_name in local_names:
            storables.append(local_names[var_name])
    with open(pickle_filepath, "wb") as f:
        pickle.dump(storables, file=f, protocol=-1)
    return
