#! /usr/bin/env python

# Copyright (C) 2007-2010 Michael Foord
# E-mail: michael AT voidspace DOT org DOT uk
# http://pypi.python.org/pypi/contextdecorator
from __future__ import with_statement

import sys

if sys.version_info >= (3, 2):
    import unittest as unittest2
else:
    import unittest2

from contextdecorator import ContextDecorator

class mycontext(ContextDecorator):
    started = False
    exc = None
    catch = False
    
    def before(self):
        self.started = True
        return self
    
    def after(self, *exc):
        self.exc = exc
        return self.catch


class TestContext(unittest2.TestCase):

    def test_context(self):
        context = mycontext()
        with context as result:
            self.assertIs(result, context)
            self.assertTrue(context.started)
            
        self.assertEqual(context.exc, (None, None, None))
    
    def test_context_with_exception(self):
        context = mycontext()
        
        with self.assertRaisesRegexp(NameError, 'foo'):
            with context:
                raise NameError('foo')
        
        context = mycontext()
        context.catch = True
        with context:
            raise NameError('foo')
        self.assertIsNotNone(context.exc)
        
    def test_decorator(self):
        context = mycontext()
        
        @context
        def test():
            self.assertIsNone(context.exc)
            self.assertTrue(context.started)
        test()
        self.assertEqual(context.exc, (None, None, None))
    
    def test_decorator_with_exception(self):
        context = mycontext()
        
        @context
        def test():
            self.assertIsNone(context.exc)
            self.assertTrue(context.started)
            raise NameError('foo')
        
        with self.assertRaisesRegexp(NameError, 'foo'):
            test()
        self.assertNotEqual(context.exc, (None, None, None))

    def test_decorating_method(self):
        context = mycontext()
        
        class Test(object):
            
            @context
            def method(self, a, b, c=None):
                self.a = a
                self.b = b
                self.c = c
        
        test = Test()
        test.method(1, 2)
        self.assertEqual(test.a, 1)
        self.assertEqual(test.b, 2)
        self.assertEqual(test.c, None)

        test.method('a', 'b', 'c')
        self.assertEqual(test.a, 'a')
        self.assertEqual(test.b, 'b')
        self.assertEqual(test.c, 'c')


if __name__ == '__main__':
    unittest2.main()