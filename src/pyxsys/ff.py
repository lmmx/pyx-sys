from pathlib import Path
from configparser import ConfigParser
from lz4 import read_jsonlz4
from ff_session import BrowserSession


def find_recovery_json():
    """
    Return path to the JSONLZ4 backup of the Firefox profile associated with the
    installation version of Firefox (this will error out if there are multiple
    installations on the system). The returned path has been confirmed to exist.
    """
    # For more information on this see wiki ⠶ "Firefox profiles"

    profiles_ini = Path("~/.mozilla/firefox/profiles.ini").expanduser()
    installs_ini = Path("~/.mozilla/firefox/installs.ini").expanduser()

    assert installs_ini.exists(), "No Firefox installation file found"

    i_config = ConfigParser()
    i_config.read(installs_ini)

    if len(i_config._sections) > 1:
        # Perhaps there should be control flow related to the 'Locked' key value
        raise ValueError(
            f"{len(i_config._sections)} installations found, "
            + f"expected 1 (sorry, make a PR/raise an issue with your installs.ini file"
        )
    elif len(i_config._sections) < 1:
        raise ValueError(f"No Firefox installations found in {installs_ini}")

    install_hash = list(i_config._sections.keys())[0]
    install_section = i_config[install_hash]
    assert "Default" in install_section.keys(), "Nonstandard installation section"
    install_path = install_section["Default"]

    # Match the installation path to profile, which indicates if it is relative/absolute
    p_conf = ConfigParser()
    p_conf.read(profiles_ini)

    profiles = [p for p in p_conf if p.startswith("Profile") and "Path" in p_conf[p]]
    install_profile = [p for p in profiles if install_path == p_conf[p]["Path"]]
    assert len(install_profile) == 1, f"Error: {len(install_profile)} FF profiles match"
    install_profile = install_profile[0]

    install_profile_config = p_conf[install_profile]
    if "IsRelative" in install_profile_config:
        rel_val = install_profile_config["IsRelative"]
        assert rel_val in "01", f"Expected 'IsRelative' to be 0 or 1, got {rel_val}"
        is_rel_path = bool(int(rel_val))
    else:
        # Assume that paths are relative unless stated otherwise
        is_rel_path = True

    # Only implemented for Linux, could add Mac/Windows given example locations
    rel_ff_dir = Path("~/.mozilla/firefox/").expanduser()

    if is_rel_path:
        ss_dir = rel_ff_dir / install_path / "sessionstore-backups"
    else:
        # Try to guess what this looks like, raise error if this guess doesn't exist
        ss_dir = install_path / "sessionstore-backups"
    assert ss_dir.exists(), f"sessionstore-backups not found at {ss_dir}"

    ff_jsonlz4 = ss_dir / "recovery.jsonlz4"
    assert ff_jsonlz4.exists(), f"Firefox recovery JSONLZ4 file not found in {ss_dir}"
    return ff_jsonlz4


def read_recovery_json(jsonlz4_path=None):
    """
    Decompress the recovery JSONLZ4 from Firefox's sessionstore-backups directory
    and return the contents as JSON (parsed into a dict with Python's JSON library).
    """
    if jsonlz4_path is None:
        jsonlz4_path = find_recovery_json()
    json = read_jsonlz4(jsonlz4_path)
    return json


def read_session(session_file=None, report=True):
    """
    Decompress the session storage backup of either the default browser profile,
    or one specified by the session_file parameter (filetype must be JSONLZ4).
    """
    session_json = read_recovery_json(session_file)
    session = BrowserSession(session_json)
    return session
