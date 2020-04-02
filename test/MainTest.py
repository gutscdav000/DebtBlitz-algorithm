from unittest import TestLoader, TextTestRunner, TestSuite
from test.test_debt import TestDebt
from test.test_utilities import TestUtilities

if __name__ == "__main__":

    loader = TestLoader()
    tests = [ loader.loadTestsFromTestCase(test) for test in (TestDebt, TestUtilities)]
    suite = TestSuite(tests)

    runner = TextTestRunner(verbosity=2)
    runner.run(suite)