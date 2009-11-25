from unittest import TestCase
from xquery.ast import *

class TestAst(TestCase):

    def test_variable(self):
        self.assertEquals(Variable("foo").get_string(), "$foo")

    def test_context(self):
        self.assertEquals(Context().get_string(), ".")

    def test_element(self):
        self.assertEquals(Element("some:ele").get_string(), "some:ele")
