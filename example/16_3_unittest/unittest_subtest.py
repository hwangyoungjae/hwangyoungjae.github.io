# unittest_subtest.py
import unittest


class SubTest(unittest.TestCase):
    def test_combined(self):
        self.assertRegex('abc', 'a')
        self.assertRegex('abc', 'B')
        # 다음 것은 검증되지 않는다.
        self.assertRegex('abc', 'c')
        self.assertRegex('abc', 'd')

    def test_with_subtest(self):
        for pat in 'aBcd':
            with self.subTest(pattern=pat):
                self.assertRegex('abc', pat)
