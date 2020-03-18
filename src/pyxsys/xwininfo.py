from subprocess import run
from shutil import which
from x_tree import WindowTree


def read_xwin_tree():
    """
    Read the root tree from xwininfo into a Python dict.
    """
    assert which("xwininfo") is not None, "xwininfo not found, please install it"
    result = run(["xwininfo", "-tree", "-root"], capture_output=True)
    assert result.returncode == 0, f"xwininfo call failed.\n{result.stderr}"
    tree = process_xwin_tree(result.stdout)
    return tree


def process_xwin_tree(tree_str):
    """
    Structure the string output from xwininfo such that indented lines (representing
    child nodes) become nested in OrderedDict collections.
    """
    tree_lines = tree_str.split(b"\n")
    tree = WindowTree()
    for line in tree_lines:
        line_indent = line.count(b" ") - line.lstrip().count(b" ")
        if not tree.source_initialised:
            if line_indent == 0:
                if line == b"":
                    # Skip empty unindented lines at the start of the tree source
                    continue
                # Handle one non-empty unindented line at the start of the tree source
                # Only one opening line, so initialise and skip to indentation
                tree.initialise_source(line)
        elif not tree.root_initialised:
            if line == b"":
                # Skip empty unindented lines after the start of the tree input
                continue
            # Reached the main tree section, can process it according to indentation
            tree.initialise_root(line, line_indent)
            continue
        elif tree.root_initialised and line_indent == 0:
            # Stop processing if you reach a blank or unindented line
            break
        # If/else block finished: the following will run for the indented tree section
        line_level = (line_indent - tree.root_indent_offset) / tree.indent_step_size
        if line_level > tree.deepest_opened_level:
            # Opening a new deepest level (i.e. starting a further level of subnode/s).
            # This line will declare how many subnodes will be listed
            if line_level == 1:
                # Subnode(s) of the source node
                pass
            else:
                # Subnode(s) more than one level below a source nodes
                pass
            # DEPRECATED: TODO access the open path directly
            tree.deepest_opened_level = line_level
        elif line_level < tree.deepest_opened_level:
            # The deepest level is completed, this line is a sibling on a previous level
            # DEPRECATED: TODO access the open path directly
            tree.deepest_opened_level = line_level
        if line_level == tree.deepest_opened_level:
            # This line will be declaring a new entry in the deepest indentation level
            if line_level == 0:
                # This is the parent of the source window
                tree.source.assign_parent(line)
                continue
            # TODO
    return tree
