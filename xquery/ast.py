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


class Fragment(Expression):
    """ A block of xquery with some xml nodes """
    __slots__ = ("expression")

    def __init__(self, expression):
        self.expression = expression

    def get_string(self):
        return "{" + self.expression.get_string() + "}"


class String(Expression):
    """ A chunk of string in XML """
    __slots__ = ("value",)
    def __init__(self, value):
        self.value = value

    def get_string(self):
        return self.value

class XmlNode(Expression):
    """ An xml tag """
    __slots__ = ("tag", "attrs", "contents")

    def __init__(self, tag):
        self.tag = tag
        self.attrs = {}
        self.contents = []

    def add(self, node):
        self.contents.append(node)

    def get_string(self):
        #FIXME: Too many code paths. do not want.
        attrs = " ".join(x.get_string() for x in self.attrs.iteritems())
        if not self.contents:
            if not attrs:
                return "<%s />" % self.tag
            return "<%s %s/>" % (self.tag, attrs)
        contents = "".join(x.get_string() for x in self.contents)
        if not attrs:
            return "<%s>%s</%s>" % (self.tag, contents, self.tag)
        return "<%s %s>%s</%s>" % (self.tag, attrs, contents, self.tag)

