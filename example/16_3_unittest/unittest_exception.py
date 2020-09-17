# unittest_exception.py
import unittest


def raises_error(*args, **kwargs):
    raise ValueError(f"Invalid value: {args} {kwargs}")


class ExceptionTest(unittest.TestCase):
    def testTrapLocally(self):
        try:
            raises_error('a', b='c')
        except ValueError:
            pass
        else:
            self.fail("Did not see ValueError")

    def testAssertRaises(self):
        self.assertRaises(ValueError, raises_error, 'a', b='c')
