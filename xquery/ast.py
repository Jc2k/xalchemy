class Node(object):
    __slots__ = ()
    def get_string(self):
        return ""
    def validate(self):
        return True


class Expression(Node):
    __slots__ = ()


class Statement(Node):
    __slots__ = ()


class Variable(Expression):
    __slots__ = ("name", )

    def __init__(self, name):
        if not isinstance(name, basestring):
            raise ValueError("Variable name must be a string")
        self.name = name

    def get_string(self):
        return "$" + self.name


class Constant(Expression):
    __slots__ = ("value", )

    def __init__(self, value):
        self.value = value

    def get_string(self):
        if isinstance(self.value, int) or isinstance(self.value, long) or isinstance(self.value, float):
            return str(self.value)
        elif isinstance(self.value, basestring):
            return "\"" + self.value + "\""
        #elif isinstance(self.value, datetime.datetime):
        #    return "date in xquery format"
        return self.value


class Context(Expression):
    __slots__ = ()

    def get_string(self):
        return "."


class Element(Expression):
    __slots__ = ("tag", "parent")

    def __init__(self, tag, parent=None):
        if not isinstance(tag, basestring):
            raise ValueError("Tagname for an element must be a string")
        if parent and not isinstance(parent, Expression):
            raise ValueError("Parent of an element must be an expression")
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
        if not isinstance(accessor, basestring):
            raise ValueError("ElementAccess must be passed a string")
        if not isinstance(parent, Expression):
            raise ValueError("ElementAccess can only access parents that are Expressions")
        self.accessor = accessor
        self.parent = parent

    def get_string(self):
        return self.parent.get_string() + "/" + self.accessor + "()"


class Let(Statement):
    """let $thing := somexpr"""
    __slots__ = ("var", "expression")

    def __init__(self, var, expression):
        if not isinstance(var, Variable):
            raise ValueError("Can only assign to variables")
        if not isinstance(expression, Expression):
            raise ValueError("Can only assign expressions to variables")
        self.var = var
        self.expression = expression

    def get_string(self):
        return "let %s := %s" % (self.var.get_string(), self.expression.get_string())


class FLOWR(Expression):
    """ for $foo in ./exo:blah return $foo """
    __slots__ = ("var", "select", "lets", "order", "where", "ret")

    def __init__(self, var, select, ret):
        self.var = var
        self.select = select
        self.lets = []
        self.order = []
        self.where = None
        self.ret = ret

    def add_let(self, let):
        if not isinstance(let, Let):
            raise ValueError("Can only add Let statements to a FLOWR with add_let method")
        self.lets.append(let)

    def get_string(self):
        flowr = "for " + self.var.get_string() + " in " + self.select.get_string() + " "
        if self.lets:
            flowr += " ".join(x.get_string() for x in self.lets) + " "
        flowr += "return " + self.ret.get_string()
        return flowr


class XmlNode(Expression):
    __slots__ = ()


class XmlQueryFragment(XmlNode):
    """ A block of xquery with some xml nodes """
    __slots__ = ("expression")

    def __init__(self, expression):
        if not isinstance(expression, Expression):
            raise ValueError("QueryFragment can only contain expressions")
        self.expression = expression

    def get_string(self):
        return "{" + self.expression.get_string() + "}"


class XmlString(XmlNode):
    """ A chunk of string in XML """
    __slots__ = ("value",)
    def __init__(self, value):
        self.value = value

    def get_string(self):
        return self.value


class XmlElement(Expression):
    """ An xml tag """
    __slots__ = ("tag", "attrs", "contents")

    def __init__(self, tag):
        if not isinstance(tag, basestring):
            raise ValueError("Tagname of XmlElement must be a string")
        self.tag = tag
        self.attrs = {}
        self.contents = []

    def add(self, node):
        if not isinstance(node, XmlNode):
            raise ValueError("An XmlElement can only contain XmlNodes")
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

