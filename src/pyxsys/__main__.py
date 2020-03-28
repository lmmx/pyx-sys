from sys import path as syspath
from sys import argv
from pathlib import Path
from argparse import ArgumentParser

# Put the absolute path to the module directory on the system PATH:
syspath.insert(0, str(Path(__file__).parent))

from pyxsys.cli import main as run_cli

parser = ArgumentParser(
    description="Store system session or restore a session from file."
)
# action_group = parser.add_mutually_exclusive_group(required=False)
# action_group.add_argument("-s", "--store", action="store_true")
# action_group.add_argument("-r", "--restore", action="store_true")
# parser.add_argument("-k", "--kill", action="store_true")
parser.add_argument("-j", "--jsonlz4", action="store")
parser.add_argument("-q", "--quiet", action="store_true")
target_group = parser.add_argument_group()
target_group.add_argument("-f", "--firefox-only", action="store_true")
target_group.add_argument("-x", "--x-win-only", action="store_true")
target_group.add_argument("-w", "--wmctrl-only", action="store_true")
target_group.add_argument("-t", "--tmux-only", action="store_true")
target_dests = [x.dest for x in target_group._group_actions]

if __name__ == "__main__":
    if argv[0].endswith("__main__.py"):
        argv = [a for a in argv if a != argv[0]]

arg_l = parser.parse_args(argv)

# store = arg_l.store
# restore = arg_l.restore
# kill = arg_l.kill
jsonlz4 = arg_l.jsonlz4
report = not arg_l.quiet

tog_on = [x for (x, v) in arg_l._get_kwargs() if v is True and x in target_dests]
if len(tog_on) > 0:
    toggled = tuple([arg_l.__dict__[x] for x in target_dests])
    rets = run_cli(ff_x_wm_tmux_toggle=toggled, ff_session_file=jsonlz4, report=report)
else:
    rets = run_cli(ff_session_file=jsonlz4, report=report)

ff_session, x_session, wm_territory, tmux_server = rets
