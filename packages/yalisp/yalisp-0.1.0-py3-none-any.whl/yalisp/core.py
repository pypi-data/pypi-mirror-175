from functools import partial


class Lisp:
    def __init__(self, runtime):
        for f in runtime:
            setattr(self, f, partial(runtime[f], self))

    def execute(self, src):
        if not src:
            return None
        if isinstance(src, (str, float, int, bool)):
            return src
        if isinstance(src, list):
            return list(map(self.execute, src))
        name = list(src.keys())[0]
        args = list(src.values())[0]
        obj = None
        if name.startswith('.') and args:
            obj = getattr(self.execute(args.pop(0)), name[1:])
            if args is []:
                args = None
            else:
                args = args[0]
        elif hasattr(self, name):
            obj = getattr(self, name)    
        if args is None:
            return obj
        return obj(*map(self.execute, args))

    def add_func(self, name=''):
        def _(func):
            f = partial(func, self)
            setattr(self, name or func.__name__, f)
            return f
        return _
