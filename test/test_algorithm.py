import unittest, os
from src.FileUtilities import loadDebtsfromFile
from src.Heloc import Heloc
from src.main import main
from src.StandardAmortized import StandardAmortized

class AlgorithmTestCase(unittest.TestCase):

    def test_heloc_0(self):
        # balance: 5000, rate: 3.75, min payment: 100, EXTRA PAYMENT 200
        # total interest: 445, with payment: 142, periods: 55, periods with payment: 18
        debts, expected_results, discretionary = loadDebtsfromFile(os.path.join('TestFiles', 'low_balance_heloc.csv'), "avalanche")

        actual_results, _ = main(debts, discretionary, actionMonths=12, method="avalanche")

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

        actual_results, _ = main(debts, discretionary, actionMonths=12, method="avalanche")

        # [name, periodsToPayoff, payoffDate, maxPeriods,totalInterest paid, maxInterest possible]
        self.assertAlmostEqual(expected_results[0][0], actual_results[0][5], delta=25.0)
        self.assertAlmostEqual(expected_results[0][1], actual_results[0][4], delta=25.0)
        self.assertEqual(expected_results[0][2], actual_results[0][3])
        self.assertEqual(expected_results[0][3], actual_results[0][1])

    def test_credit_card_1(self):
        debts, expected_results, discretionary = loadDebtsfromFile(os.path.join('TestFiles', 'low_balance_credit_card.csv'),
                                                                   "avalanche")

        actual_results, _ = main(debts, discretionary, actionMonths=12, method="avalanche")
        # [name, periodsToPayoff, payoffDate, maxPeriods,totalInterest paid, maxInterest possible]
        self.assertAlmostEqual(expected_results[0][0], actual_results[0][5], delta=350.0) #TODO fix not sure why these are here.
        self.assertAlmostEqual(expected_results[0][1], actual_results[0][4], delta=150.0) #TODO fix
        self.assertAlmostEqual(expected_results[0][2], actual_results[0][3], delta=5)
        self.assertEqual(expected_results[0][3], actual_results[0][1])

    def test_remaining_principle_calculator(self):
        debts, expected_results, discretionary = loadDebtsfromFile(
            os.path.join('TestFiles', 'heloc_vs_amortized.csv'),
            "avalanche")

        print(debts)
        heloc = debts[0]
        amortized = debts[1]

        print('\nresults')
        print(expected_results)

        actual_amortized, _ = main([amortized], 0.0, actionMonths=12, method="avalanche")

        print(actual_amortized)
        self.assertAlmostEqual(expected_results[1][0], actual_amortized[0][5], delta=5.0)
        self.assertEqual(expected_results[1][2], actual_amortized[0][3])

        actual_heloc, _ = main([heloc], 0.0, actionMonths=12, method="avalanche")
        print(actual_heloc)
        self.assertAlmostEqual(expected_results[0][0], actual_heloc[0][5], delta=125.0)
        self.assertEqual(expected_results[0][2], actual_heloc[0][3])




if __name__ == '__main__':
    unittest.main()
