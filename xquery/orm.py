
from .ast import *


class Query(object):
    """ Represents an unexecuted query """

    def __init__(self, cls, expression):
        self.cls = cls
        self.expression = expression

    def get_xquery(self):
        return self.expression.get_string()

    def __iter__(self):
        raise StopIteration


class Document(object):
    """ Represents an XML document stored in an XQuery store """

    def __init__(self, *args):
        pass

    @classmethod
    def find(cls, *args):
        v = Variable("retval")
        f = FLOWR(v, Context(), v)
        return Query(cls, f)

