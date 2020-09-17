# unittest_fixtures.py
import random
import unittest


def setUpModule():
    print("In setupModule()")


def tearDownModule():
    print("In tearDownModule()")


class FixturesTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("In setUpClass()")
        cls.good_range = range(1, 10)

    @classmethod
    def tearDownClass(cls) -> None:
        print("In tearDownClass()")
        del cls.good_range

    def setUp(self) -> None:
        super().setUp()
        print("\nIn setUp()")
        # 확실하게 범위 안에 있는 한 숫자를 선택한다.
        # 범위는 stop 값이 포함되지 않게 정의되므로, 이 값은 선택을 위한 값 집합에 포함돼서는 안된다.
        self.value = random.randint(self.good_range.start, self.good_range.stop - 1)

    def tearDown(self) -> None:
        print("In tearDown()")
        del self.value
        super().tearDown()

    def test1(self):
        print("In test1()")
        self.assertIn(self.value, self.good_range)

    def test2(self):
        print("In test2()")
        self.assertIn(self.value, self.good_range)
