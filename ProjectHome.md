If you're a library or framework creator then it is nice to be able to create
APIs that can be used _either_ as decorators or context managers.

The contextdecorator module is a backport of new features added to the
[contextlib module](http://docs.python.org/library/contextlib.html) in
Python 3.2. contextdecorator works with Python 2.4+ including Python 3.

Context managers inheriting from `ContextDecorator` have to implement
`__enter__` and `__exit__` as normal.
[\_\_exit\_\_](http://docs.python.org/reference/datamodel.html#object.__exit__)
retains its optional exception handling even when used as a decorator.

Example:
```
   from contextdecorator import ContextDecorator

   class mycontext(ContextDecorator):
      def __enter__(self):
         print 'Starting'
         return self

      def __exit__(self, *exc):
         print 'Finishing'
         return False

   @mycontext()
   def function():
      print 'The bit in the middle'
   
   with mycontext():
      print 'The bit in the middle'
```
Existing context managers that already have a base class can be extended by
using `ContextDecorator` as a mixin class
```
   from contextdecorator import ContextDecorator

   class mycontext(ContextBaseClass, ContextDecorator):
      def __enter__(self):
         return self

      def __exit__(self, *exc):
         return False
```
contextdecorator also contains an implementation of [contextlib.contextmanager](http://docs.python.org/library/contextlib.html#contextlib.contextmanager)
that uses `ContextDecorator`. The context managers it creates can be used as
decorators as well as in statements.   from contextdecorator import ContextDecorator

   class mycontext(ContextBaseClass, ContextDecorator):
      def __enter__(self):
         return self

      def __exit__(self, *exc):
         return False
}}}
   from contextdecorator import contextmanager
   
   @contextmanager
   def mycontext(*args):
      print 'started'
      try:
         yield
      finally:
         print 'finished!'
   
   @mycontext('some', 'args')
   def function():
      print 'In the middle'
      
   with mycontext('some', 'args'):
      print 'In the middle'
}}}

The project is available for download from [http://pypi.python.org/pypi/contextdecorator PyPI] so it can be easily installed:
{{{
    pip install -U contextdecorator
    easy_install -U contextdecorator
}}}
The tests require [http://pypi.python.org/pypi/unittest2 unittest2]
to run.```