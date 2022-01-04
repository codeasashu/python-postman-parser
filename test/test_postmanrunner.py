import unittest, inspect
from postmanrunner.postmanrunner import PostmanRunner

class TestPostmanCollection(unittest.TestCase):

    def setUp(self):
        self.runner = PostmanRunner("a.json")

    def test_verifyCollection(self):
        self.assertIsNotNone(self.runner.json)
        self.assertTrue(self.runner.verifyCollection())

    def test_parseCollection(self):
        self.assertIn('item', self.runner.json.keys())
