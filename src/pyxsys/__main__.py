from sys import path as syspath
from sys import argv
from pathlib import Path
from argparse import ArgumentParser

# Put the absolute path to the module directory on the system PATH:
syspath.insert(0, str(Path(__file__).parent))

from pyxsys.cli import run_cli

parser = ArgumentParser(
    description="Store system session or restore a session from file."
)
action_group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-s", "--store", action="store_true")
group.add_argument("-r", "--restore", action="store_true")
parser.add_argument("-k", "--kill", action="store_true")
target_group = parser.add_mutually_exclusive_group()
target_group.add_argument("-f", "--firefox-only", action="store_true")
target_group.add_argument("-x", "--x-win-only", action="store_true")


if __name__ == "__main__":
    if argv[0].endswith("__main__.py"):
        argv = [a for a in argv if a != argv[0]]

arg_l = parser.parse_args(argv)

store = arg_l.store
restore = arg_l.restore
kill = arg_l.kill
ff_only = arg_l.firefox_only
x_only = arg_l.x_win_only

run_cli(restore, kill, ff_only, x_only)
