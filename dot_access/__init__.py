__project__ = "dot_access"
__version__ = "0.0.1"
__repo__ = "https://github.com/kootenpv/dot_access"

from functools import wraps


class Dot(object):
    """
    A class which will help querying of data in a json manner.
    Does not allow assignment (read-only).
    """

    def __init__(self, original_object):
        self.original_object = original_object

    def __getitem__(self, x):
        if isinstance(self.original_object, dict):
            try:
                res = self.original_object.get(x)
            except:
                res = None
        elif isinstance(self.original_object, list):
            try:
                res = self.original_object[x]
            except:
                res = None
        else:
            res = self.original_object
        return Dot(res)

    def __call__(self):
        return self.original_object()

    def __iter__(self):
        return iter(self.original_object)

    def __setitem__(self, x, v):
        raise TypeError("Cannot change a key on a read-only view dot directly.")

    def __setattr__(self, x, v):
        try:
            super(Dot, self).__getattribute__("original_object")
            raise TypeError("Cannot assign to a read-only view dot object directly.")
        # only allow original_object to be set if not set
        except AttributeError:
            super(Dot, self).__setattr__(x, v)

    def __getattr__(self, x):
        if hasattr(self.original_object, x):
            return Dot(getattr(self.original_object, x))
        try:
            return Dot(self.original_object.get(x))
        except:
            return Dot(None)

    def __bool__(self):
        return bool(self.original_object)

    def __hash__(self):
        return hash(self.original_object)

    def __eq__(self, other):
        return self.original_object == other

    def __repr__(self):
        return "Dot({})".format(self.original_object.__repr__())

    def __str__(self):
        return self.original_object.__str__()

    def _asdict(self):
        return self.original_object


def dot(fn):
    """ Allows decorating functions for which the return value will be wrapped by 'Dot'. """
    def new_function(*args, **kwargs):
        return Dot(fn(*args, **kwargs))
    return new_function


def trydot(exception_types):
    """
    Allows decorating functions for which the return value will be wrapped by 'Dot'.
    If an exception occurs, return Dot(None)
    This is a terrible idea.
    """
    def real_decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                return Dot(fn(*args, **kwargs))
            except exception_types:
                return Dot(None)
        return wrapper
    return real_decorator
