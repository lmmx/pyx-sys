from pathlib import Path
from subprocess import run
from shutil import which
from json import loads

def read_jsonlz4(jsonlz4_path):
    """
    Decompress the jsonlz4 file (over STDIN) using dejsonlz4 (assumed to be on PATH),
    read the JSON into a Python dict (using the json library) and return that.
    """
    assert which("dejsonlz4") is not None, "dejsonlz4 not found, please install it"
    result = run(["dejsonlz4", jsonlz4_path], capture_output=True)
    # no OUT_FILE given to dejsonlz4 will decompress to STDOUT, captured to variable
    json_str = result.stdout
    err = result.stderr
    assert result.returncode == 0, f"dejsonlz4 call failed.\n{err}"
    json = loads(json_str)
    return json
