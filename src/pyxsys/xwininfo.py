from subprocess import run
from shutil import which
from collections import OrderedDict


def read_xwin_tree():
    """
    Read the root tree from xwininfo into a Python dict.
    """
    assert which("xwininfo") is not None, "xwininfo not found, please install it"
    result = run(["xwininfo", "-tree", "-root"], capture_output=True)
    tree_str = result.stdout
    err = result.stderr
    assert result.returncode == 0, f"xwininfo call failed.\n{err}"
    tree_dict = process_xwin_tree(tree_str)
    return tree_dict


def process_xwin_tree(tree_str):
    """
    Structure the string output from xwininfo such that indented lines (representing
    child nodes) become nested in OrderedDict collections.
    """
    tree_lines = tree_str.split(b"\n")
    tree = []
    root_indent_offset = None
    subnode_indent_step_size = 3  # Each child node is indented by 3 spaces
    initialised = False
    deepest_opened_level = None
    for line in tree_lines:
        line_indent = line.count(b" ") - line.lstrip().count(b" ")
        if not initialised:
            if line_indent == 0:
                # Skip empty or unindented lines at the start of the tree input
                continue
        elif line_indent == 0:
            # Stop processing if you reach a blank or unindented line
            break
        else:
            # Reached the main tree section, can process it according to indentation
            root_indent_offset = line_indent
            initialised = True
            deepest_opened_level = 0
        assert initialised, "Tree processing should only begin after initialisation"
        tree_indent = line_indent - root_indent_offset
        line_level = tree_indent / subnode_indent_step_size
        if line_level > deepest_opened_level:
            # Opening a new deepest level (i.e. starting a further level of subnode/s).
            # This line is not a root, so must declare how many subnodes will be listed
            e_msg = "Line parse failed: indentation deepened but no offspring declared"
            assert line.endswith(b" child:") or line.endswith(b" children:"), e_msg
            deepest_opened_level = line_level
        elif line_level < deepest_opened_level:
            # The deepest level is completed, this line is a sibling on a previous level
            deepest_opened_level = line_level
        if line_level == deepest_opened_level:
            # This line will be declaring a new entry in the deepest indentation level
    return tree
