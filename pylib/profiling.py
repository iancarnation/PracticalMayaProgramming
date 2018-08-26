import types
import time
import errno
import traceback

_reporting_enabled = True

def _getkey(func):
    if isinstance(func, types.FunctionType):
        return '%s.%s' % (func.__module__, func.__name__)
    if isinstance(func, types.MethodType):
        return '%s.%s.%s' % (func.__module__,
                             func.im_class.__name__,
                             func.__name__)
    raise TypeError('%s must be a function or method' % func)

def _report_duration(key, duration):
    global _reporting_enabled
    if not _reporting_enabled:
        return
    try:
        with open('durations.txt', 'a') as f:
            f.write('%s: %s\n' % (key, duration))
    except OSError as ex:
        if ex.errno == errno.EACCES:
            print 'durations.txt in use, cannot record.'
        else:
            _reporting_enabled = False
            traceback.print_exc()
            print 'Disabling metrics recording.'

def record_duration(func):
    key = _getkey(func)
    def inner(*args, **kwargs):
        starttime = time.clock()
        result = func(*args, **kwargs)
        endtime = time.clock()
        duration = endtime - starttime
        _report_duration(key, duration)
        print '%s took %ss' % (key, duration)
        return result
    return inner

