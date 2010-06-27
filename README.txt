If you're a library or framework creator then it is nice to be able to create
APIs that can be used *either* as decorators or context managers.

You just subclasss ``ContextDecorator`` and implement ``before`` and ``after``
methods. As an added piece of goodness the ``after`` method provides the
optional exception handling behaviour of `__exit__
<http://docs.python.org/reference/datamodel.html#object.__exit__>`_ even for
decorators.

Here's an example of how you use it::

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

Both before and after methods are optional (but providing neither is somewhat 
pointless). See the tests for more usage examples.

contextdecorator works with Python 2.4+ including Python 3.

Repository and issue tracker:

* `contextdecorator on google code <http://code.google.com/p/contextdecorator/>`_

The project is available for download from `PyPI <http://pypi.python.org/pypi/contextdecorator>`_
so it can be easily installed:

    | ``pip install -U contextdecorator``
    | ``easy_install -U contextdecorator``

The tests require `unittest2 <http://pypi.python.org/pypi/unittest2>`_
to run.
