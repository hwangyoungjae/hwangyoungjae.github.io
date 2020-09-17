# unittest_equality_container.py
import textwrap
import unittest


class ContainerEqualityTest(unittest.TestCase):
    def testCount(self):
        self.assertCountEqual(['a', 'b', 'c', 'b'], ['a', 'c', 'b', 'c'])

    def testDict(self):
        self.assertDictEqual({'a': 1, 'b': 2}, {'a': 1, 'b': 3})

    def testList(self):
        self.assertListEqual(['a', 'b', 'c'], ['a', 'c', 'b'])

    def testMultiLineString(self):
        self.assertMultiLineEqual(
            textwrap.dedent("""
            This string
            has more than one
            line.
            """),
            textwrap.dedent("""
            This string has
            more than two
            lines.
            """)
        )

    def testSequence(self):
        self.assertSequenceEqual(['a', 'b', 'c'], ['a', 'c', 'b'])

    def testSet(self):
        self.assertSetEqual(set(['a', 'b', 'c']), set(['a', 'c', 'b', 'd']))

    def testTuple(self):
        self.assertTupleEqual((1, 'a'), (1, 'b'))
