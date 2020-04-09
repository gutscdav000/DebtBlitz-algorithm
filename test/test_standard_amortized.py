import unittest
from src.Debt import Debt
from src.StandardAmortized import StandardAmortized
from datetime import datetime

class TestDebt(unittest.TestCase):
    def test_simple_property(self):
        name = 'bob'
        balance = 500.00
        rate = 0.06
        minPayment = 45.00
        loanTerm = 12
        totalInterestt = 0.0
        periodsToPayoff = 0
        payoffDate = None

        debt = StandardAmortized(name, balance, rate, minPayment, loanTerm)

        self.assertEqual(debt.name, name)
        self.assertEqual(debt.balance, balance)
        self.assertEqual(debt.balance, balance)
        self.assertEqual(debt.rate, rate)
        self.assertEqual(debt.minPayment, minPayment)
        self.assertEqual(debt.loanTerm, loanTerm)
        # calculated values
        self.assertEqual(debt.totalInterest, totalInterestt)
        self.assertEqual(debt.periodsToPayoff, periodsToPayoff)
        self.assertEqual(debt.payoffDate, payoffDate)

        name = 'tim'
        debt.name = name
        self.assertEqual(debt.name, name)

        balance = 400.00
        debt.balance = balance
        self.assertEqual(debt.balance, balance)

        rate = 0.12
        debt.rate = rate
        self.assertEqual(debt.rate, rate)

        minPayment = 60.00
        debt.minPayment = minPayment
        self.assertEqual(debt.minPayment, minPayment)

        loanTerm = 10
        debt.loanTerm = loanTerm
        self.assertEqual(debt.loanTerm, loanTerm)

        totalInterestt = 10
        debt.totalInterest = totalInterestt
        self.assertEqual(debt.totalInterest, totalInterestt)

        periodsToPayoff = 50
        debt.periodsToPayoff = periodsToPayoff
        self.assertEqual(debt.periodsToPayoff, periodsToPayoff)

        payoffDate = datetime.strptime("2030-5-01", "%Y-%m-%d")
        debt.payoffDate = (5, 2030)
        self.assertEqual(debt.payoffDate, payoffDate)

    def test_inequality_comparison(self):
        name = 'bob'
        balance = 500.00
        rate = 0.06
        minPayment = 45.00
        loanTerm = 12
        totalInterestt = 0.0

        avalanche1 = StandardAmortized('bob', 1000.00, 0.06, 50.0, 50)
        avalanche2 = StandardAmortized('bill', 100.00, 0.12, 50.0, 50)
        self.assertTrue(avalanche1 < avalanche2)
        self.assertFalse(avalanche1 > avalanche2)
        avalanche1.rate = 0.12
        self.assertTrue(avalanche1 >= avalanche2)
        self.assertTrue(avalanche1 <= avalanche2)

        snow1 = StandardAmortized('bob', 100.00, 0.06, 50.0, 50, method='snowball')
        snow2 = StandardAmortized('bill', 2000.00, 0.12, 50.0, 50, method='snowball')
        self.assertTrue(snow1 < snow2)
        self.assertFalse(snow1 > snow2)
        snow1.balance = 2000.00
        self.assertTrue(snow1 >= snow2)
        self.assertTrue(snow1 <= snow2)

    def test_equality_comparison(self):

        d1 = StandardAmortized('bob', 1000.00, 0.06, 50.0, 50)
        d2 = StandardAmortized('bill', 100.00, 0.12, 50.0, 50)
        d3 = StandardAmortized('bill', 100.00, 0.12, 50.0, 50)
        self.assertTrue(d1 != d2)
        self.assertFalse(d1 == d2)
        self.assertTrue(d2 == d3)
        self.assertFalse( d2 != d3)

    def test_compute_interest_savings(self):
        d3 = StandardAmortized('bill', 100.00, 0.12, 50.0, 50)
        self.assertIsNone(d3.possibleInterestSavings)
        with self.assertRaises(AssertionError):
            d3.calculatePossibleInterestSavings()

        d3.totalInterest = 500
        d3.calculatePossibleInterestSavings()
        self.assertEqual(d3._possibleInterestSavings, -498.4749)

    def test_compute_max_interest(self):
        d1 = StandardAmortized('bob', 1000.00, 0.06, 50.0, 50)
        self.assertAlmostEqual(d1.maxInterest, 56.25, places=2)
        d2 = StandardAmortized('bill', 100.00, 0.12, 50.0, 50)
        self.assertAlmostEqual(d2.maxInterest, 1.53, places=2)



if __name__ == '__main__':
    unittest.main()
