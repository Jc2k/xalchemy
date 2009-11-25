class Node(object):
    __slots__ = ()


class Expression(Node):
    __slots__ = ()


class Statement(Node):
    __slots__ = ()


class Variable(Expression):
    __slots__ = ("name", )

    def __init__(self, name):
        self.name = name

    def get_string(self):
        return "$" + self.name

class Context(Expression):
    __slots__ = ()

    def get_string(self):
        return "."


class Element(Expression):
    __slots__ = ("tag", "parent")

    def __init__(self, tag, parent=None):
        self.tag = tag
        self.parent = parent

    def get_string(self):
        if self.parent:
            return self.parent.get_string() + "/" + self.tag
        return self.tag


class ElementAccess(Expression):
    """ e.g. ./text() """
    __slots__ = ("accessor", "parent")

    def __init__(self, accessor, parent):
        self.accessor = accessor
        self.parent = parent

    def get_string(self):
        return self.parent.get_string() + "/" + self.accessor + "()"

class Let(Statement):
    """let $thing := somexpr"""
    __slots__ = ("var", "expression")

    def __init__(self, var, expression):
        self.var = var
        self.expression = expression

    def get_string(self):
        return "let %s := %s" % (self.var.get_string(), self.expression.get_string())

class For(Expression):
    """ for $foo in ./exo:blah return $foo """
    __slots__ = ("var", "select", "ret")

    def __init__(self, var, select, ret):
        self.var = var
        self.select = select
        self.ret = ret

    def get_string(self):
        return "for " + self.var.get_string() + \
            " in " + self.select.get_string() + \
            " return " + self.ret.get_string()


if __name__ == "__main__":
    print ElementAccess("text", Element("exo:foobar", Element("exo:document", Context()))).get_string()
