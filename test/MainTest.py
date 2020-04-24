from unittest import TestLoader, TextTestRunner, TestSuite
from test.test_standard_amortized import TestDebt
from test.test_utilities import TestUtilities
from test.test_heloc_algorithm import HelocTestCase

if __name__ == "__main__":

    loader = TestLoader()
    tests = [ loader.loadTestsFromTestCase(test) for test in (TestDebt, TestUtilities, HelocTestCase)]
    suite = TestSuite(tests)

    runner = TextTestRunner(verbosity=2)
    runner.run(suite)