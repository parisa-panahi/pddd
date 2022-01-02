import inspect


class Entity(object):
    def __init__(self, *args, **kwargs):
        ...

    def __iter__(self):
        for name in dir(self):
            value = getattr(self, name)
            if not name.startswith("__") and not inspect.ismethod(value):
                yield name, value
