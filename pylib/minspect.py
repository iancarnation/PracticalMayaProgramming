import pymel.core as pmc
import sys

def syspath():
    print 'sys.path:'
    for p in sys.path:
        print '  ' + p

def info(obj):
    """Prints information about the object."""

    lines = ['Info for %s' % obj.name(), 'Attributes:']
    # Get the name of all attributes
    for a in obj.listAttr():
        lines.append('  ' + a.name())
    # Get relatives
    lines.append('-------------------------')
    lines.append('Relatives:')
    for r in obj.listRelatives():
        lines.append('  ' + r.name())
    
    lines.append('MEL type: %s' % obj.type())
    lines.append('MRO: ')
    lines.extend(['  ' + t.__name__ for t in type(obj).__mro__])

    result = '\n'.join(lines)

    print result