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
        f = FLOWR(foo, ElementAccess("children", Context()), foo)
        self.assertEquals(f.get_string(),
            "for $foo in ./children() return $foo")

    def test_for_with_let(self):
        foo = Variable("a")
        bar = Variable("b")
        f = FLOWR(foo, ElementAccess("children", Context()), bar)
        f.add_let(Let(bar, ElementAccess("text", foo)))
        self.assertEquals(f.get_string(),
            "for $a in ./children() let $b := $a/text() return $b")

    def test_xml_node(self):
        n = XmlElement("exo:badger")
        self.assertEquals(n.get_string(), "<exo:badger />")

    def test_xml_with_text(self):
        n = XmlElement("exo:badger")
        n.add(XmlString("abc"))
        self.assertEquals(n.get_string(), "<exo:badger>abc</exo:badger>")

    def test_fragment(self):
        e = ElementAccess("text", Context())
        x = XmlElement("exo:badger")
        x.add(XmlQueryFragment(e))
        self.assertEquals(x.get_string(), "<exo:badger>{./text()}</exo:badger>")

    def test_constant_number(self):
        self.assertEquals(Constant(7.0).get_string(), "7.0")
        self.assertEquals(Constant(7.01).get_string(), "7.01")
        self.assertEquals(Constant(7).get_string(), "7")

    def test_constant_string(self):
        self.assertEquals(Constant("1").get_string(), "\"1\"")
        self.assertEquals(Constant("abc").get_string(), "\"abc\"")

