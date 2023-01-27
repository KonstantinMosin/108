from src.messageTools import parseDelimited

import unittest

class ParseDelimitedTest(unittest.TestCase):
    def setUp(self):
        parseDelimited(1, 2)
    
    def test_nulldata(self):
        self.assertIsNone(parseDelimited(1,2))
