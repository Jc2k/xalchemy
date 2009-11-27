from unittest import TestCase
from xquery.ast import *

class TestAst(TestCase):

    def test_variable(self):
        self.assertRaises(ValueError, Variable, 1)

    def test_element(self):
        self.assertRaises(ValueError, Element, 1)

    def test_element_access(self):
        self.assertRaises(ValueError, ElementAccess, 1, Context())
        self.assertRaises(ValueError, ElementAccess, "test", 1)

    def test_let(self):
        self.assertRaises(ValueError, Let, 1, Context())
        self.assertRaises(ValueError, Let, Variable("a"), 1)

    def test_for(self):
        pass

    def test_xml(self):
        self.assertRaises(ValueError, XmlElement, 1)
        self.assertRaises(ValueError, XmlElement("foo").add, "blah")

    def test_fragment(self):
        self.assertRaises(ValueError, XmlQueryFragment, "a")
