import unittest
import fib

class TestFib(unittest.TestCase):

    def test_correctnes(self):
        for i in range(100_000):
            print
            self.assertEqual(fib.my_fib(i), fib.fib(i))


if __name__ == '__main__':
    unittest.main()
