#!/usr/bin/python
# coding=utf-8
import functools

def withTest(a, b='b', c=0):
    """
    :param markname:
    :return:the decorator with specific db connection
    """
    def wrapped(fun):
        @functools.wraps(fun)
        def wrapper(*args, **kwargs):
            print fun.func_name
            print fun.__name__
            print dir(fun)
            res = fun(*args, **kwargs)
            return res
        return wrapper
    return wrapped
    
@withTest(0)
def at():
    pass

@withTest(0)
def bt():
    at()

if __name__ == '__main__':
  bt()