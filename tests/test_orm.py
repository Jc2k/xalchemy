import unittest
from xquery.orm import Document, Query

class TestOrm(unittest.TestCase):

    def test_proxy(self):
        p = Document.find()
        self.assertEquals(isinstance(p, Query), True)
