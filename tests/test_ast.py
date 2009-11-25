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
