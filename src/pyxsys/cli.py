from pyxsys.ff import read_session


def main(session_file=None, report=True):
    if report:
        print("--------------RUNNING pyxsys.cli⠶main()--------------")
    session = read_session(session_file=session_file, report=report)
    if report:
        print("------------------COMPLETE--------------------------")
    return session
