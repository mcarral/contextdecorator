# Copyright (C) 2007-2010 Michael Foord
# E-mail: michael AT voidspace DOT org DOT uk
# http://pypi.python.org/pypi/contextdecorator
'''
Create objects that act as both context managers *and* as decorators, and behave the same in both cases.

Example:

    from contextdecorator import ContextDecorator

    class mycontext(ContextDecorator):
    
        def __init__(self, *args):
            """Normal initialiser"""

        def before(self):
            """
            Called on entering the with block or starting the decorated function.
        
            If used in a with statement whatever this method returns will be the
            context manager.
            """
    
        def after(self, *exc):
            """
            Called on exit. Arguments and return value of this method have
            the same meaning as the __exit__ method of a normal context
            manager.
            """

    @mycontext('some', 'args')
    def function():
        pass

    with mycontext('some', 'args') as something:
        pass

Both before and after methods are optional (but providing neither is somewhat pointless).
See the tests for more usage examples.
'''

import sys

try:
    from functools import wraps
except ImportError:
    # Python 2.4 compatibility
    def wraps(original):
        def inner(f):
            f.__name__ = original.__name__
            return f
        return inner

# horrible reraise code for compatibility
# with Python 2 & 3
if sys.version_info >= (3,0):
    exec ("""
def _reraise(cls, val, tb):
    raise val
""")
else:
    exec ("""
def _reraise(cls, val, tb):
    raise cls, val, tb
""")

__all__ = ['__version__', 'ContextDecorator']
__version__ = '1.0'


EXC = (None, None, None)

class ContextDecorator(object):
    before = None
    after = None
        
    def __call__(self, f):
        @wraps(f)
        def inner(*args, **kw):
            if self.before is not None:
                self.before()
            
            exc = EXC
            try:
                result = f(*args, **kw)
            except Exception:
                exc = sys.exc_info()
            
            catch = False
            if self.after is not None:
                catch = self.after(*exc)
            
            if not catch and exc is not EXC:
                _reraise(*exc)
            return result
        return inner
            
    def __enter__(self):
        if self.before is not None:
            return self.before()
    
    def __exit__(self, *exc):
        catch = False
        if self.after is not None:
            catch = self.after(*exc)
        return catch
