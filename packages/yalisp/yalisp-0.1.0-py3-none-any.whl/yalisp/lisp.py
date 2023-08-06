from functools import reduce
import operator as ops
from .core import Lisp


functions = {
    'add': lambda self, *args: sum(args),
    'mul': lambda self, *args: reduce(ops.mul, args),
    'sub': lambda self, *args: reduce(ops.sub, args),
    'div': lambda self, *args: reduce(ops.truediv, args),
    'print': lambda self, *args: print(*args),
    'setv': lambda self, var, value: setattr(self, var, value),
}

interpriter = Lisp(functions)

@interpriter.add_func('if')
def cond(self, condition, body, orelse):
    return body if condition else orelse

@interpriter.add_func('for')
def _iter(self, func, iterable):
    return list(map(func, iterable))
