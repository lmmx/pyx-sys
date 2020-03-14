from pathlib import Path
from subprocess import run
from shutil import which
from json import loads

# ff_jsonlz4 = ss_dir / 'recovery.jsonlz4'
def read_jsonlz4(jsonlz4_path):
    """
    Copy the .jsonlz4 file, decompress it with dejsonlz4 (assumed to be on PATH),
    read and handle the recovery file, then delete the copy.
    """
    assert which("dejsonlz4") is not None, "dejsonlz4 not found, please install it"
    result = run(["dejsonlz4", jsonlz4_path], capture_output=True)
    # no OUT_FILE given to dejsonlz4 will decompress to STDOUT, captured to variable
    json_str = result.stdout
    err = result.stderr
    assert result.returncode == 0, f"dejsonlz4 failed.\n{'' if err == b'' else err}"
    json = loads(json_str)
    return json
