import pymel.core as pmc

GREEN = 14
BLUE = 6
YELLOW = 17

def safe_setparent(node, parent):
    """'node.setParent(parent)' if 'parent' is not the same
    as 'node''s existing parent.
    """
    if node.getParent() != parent:
        node.setParent(parent)

def _convert_to_joint(node, parent, prefix, jnt_size, lcol, rcol, ccol):
    j = pmc.joint(name=prefix + node.name())
    safe_setparent(j, parent)
    j.translate.set(rootnode.translate.get())
    j.rotate.set(rootnode.rotate.get())
    j.setRadius(jnt_size)
    def calc_wirecolor():
        x = j.translateX.get()
        if x < 0.001:
            return rcol
        elif x > 0.001:
            return lcol
        else:
            return ccol
    j.overrideColor.set(calc_wirecolor())
    return j

def convert_to_skeleton(rootnode, prefix='skel_',
                        joint_size=1.0,
                        lcol=BLUE,
                        rcol=GREEN,
                        ccol=YELLOW,
                        _parent=None):
    """Converts a hierarchy of nodes into joints that have the same transform, 
    with their name prefixed with 'prefix'.
    Return the newly created root node.
    The new hierarchy will share the same parent as rootnode.

    :param rootnode: The root PyNode.
        Everything under it will be converted.
    :param prefix: String to prefix newly created nodes with.
    """
    if _parent is None:
        _parent = rootnode.getParent()
    j = _convert_to_joint(rootnode, _parent, prefix, joint_size, lcol, rcol, ccol)    
    for c in rootnode.children():
        convert_to_skeleton(c, prefix, joint_size, lcol, rcol, ccol, j)
    return j

def ancestors(node):
    """Return a list of ancestors, starting with the direct parent
    and ending with the top-level (root) parent."""
    result = []
    parent = node.getParent()
    while parent is not None:
        result.append(parent)
        parent = parent.getParent()
    return result

def uniqueroots(nodes):
    """Returns a list of the nodes in 'nodes' that are not
    children of any node in 'nodes'."""
    result = []
    def handle_node(n):
        """If any of the ancestors of n are in realroots,
        just return, otherwise, append n to realroots
        """
        for ancestor in ancestors(n):
            if ancestor in nodes:
                return
        result.append(n)
    for node in nodes:
        handle_node(node)
    return result    