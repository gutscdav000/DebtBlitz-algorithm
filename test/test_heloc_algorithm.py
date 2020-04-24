import unittest, os
from src.FileUtilities import loadDebtsfromFile
from src.Heloc import Heloc
from src.main import main

class HelocTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)

    def test_heloc_0(self):
        # balance: 5000, rate: 3.75, min payment: 100, EXTRA PAYMENT 200
        # total interest: 445, with payment: 142, periods: 55, periods with payment: 18
        debts, expected_results, discretionary = loadDebtsfromFile(os.path.join('TestFiles', 'low_balance_heloc.csv'), "avalanche")

        actual_results = main(debts, discretionary, "avalanche")

        # [name, periodsToPayoff, payoffDate, maxPeriods,totalInterest paid, maxInterest possible]
        self.assertAlmostEqual(expected_results[0][0], actual_results[0][5], delta=3.0)
        self.assertAlmostEqual(expected_results[0][1], actual_results[0][4], delta=3.0)
        self.assertEqual(expected_results[0][2], actual_results[0][3])
        self.assertEqual(expected_results[0][3], actual_results[0][1])


    def test_heloc_1(self):
        # balance: 25000, rate: 0.0375, minPayment: 100.0 EXTRA PAYMENT: 200
        # total interest: 23710, with payment: 4005, periods: 488, periods with payment: 97
        debts, expected_results, discretionary = loadDebtsfromFile(os.path.join('TestFiles', 'avg_balance_heloc.csv'),
                                                                   "avalanche")

        actual_results = main(debts, discretionary, "avalanche")

        # [name, periodsToPayoff, payoffDate, maxPeriods,totalInterest paid, maxInterest possible]
        self.assertAlmostEqual(expected_results[0][0], actual_results[0][5], delta=25.0)
        self.assertAlmostEqual(expected_results[0][1], actual_results[0][4], delta=25.0)
        self.assertEqual(expected_results[0][2], actual_results[0][3])
        self.assertEqual(expected_results[0][3], actual_results[0][1])




if __name__ == '__main__':
    unittest.main()
