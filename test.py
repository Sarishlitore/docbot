"""
Tests for documentsbot
"""
import unittest


class TestBot(unittest.TestCase):

    def test_show_docs(self):
        def show_docs(docs, filter_=lambda doc: doc):
            return [d for d in docs if filter_(d)]

        # print(show_docs(['per1', 'per2'], lambda name: name == 'per1'))
        self.assertListEqual(['per1'], show_docs(['per1', 'per2'], lambda name: name == 'per1'))
