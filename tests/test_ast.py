from unittest import TestCase
from xquery.ast import *

class TestAst(TestCase):

    def test_variable(self):
        self.assertEquals(Variable("foo").get_string(), "$foo")

    def test_context(self):
        self.assertEquals(Context().get_string(), ".")

    def test_element(self):
        self.assertEquals(Element("some:ele").get_string(), "some:ele")

    def test_element_access(self):
        ea = ElementAccess("text", Context())
        self.assertEquals(ea.get_string(), "./text()")

    def test_let(self):
        l = Let(Variable("foo"), ElementAccess("text", Context()))
        self.assertEquals(l.get_string(), "let $foo := ./text()")

    def test_for(self):
        foo = Variable("foo")
        f = For(foo, ElementAccess("children", Context()), foo)
        self.assertEquals(f.get_string(),
            "for $foo in ./children() return $foo")

    def test_xml_node(self):
        n = XmlElement("exo:badger")
        self.assertEquals(n.get_string(), "<exo:badger />")

    def test_xml_with_text(self):
        n = XmlElement("exo:badger")
        n.add(XmlString("abc"))
        self.assertEquals(n.get_string(), "<exo:badger>abc</exo:badger>")
