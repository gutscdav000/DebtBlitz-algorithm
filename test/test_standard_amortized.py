import unittest
from src.Debt import Debt
from src.StandardAmortized import StandardAmortized
from datetime import datetime

class TestDebt(unittest.TestCase):
    def test_simple_property(self):
        id = 1
        name = 'bob'
        balance = 500.00
        purchasePrice = 2500.00
        rate = 0.06
        minPayment = 45.00
        loanTerm = 12
        totalInterestt = 0.0
        periodsToPayoff = 0
        payoffDate = None

        debt = StandardAmortized(id, name, purchasePrice, balance, balance, rate, minPayment, loanTerm)

        self.assertEqual(debt.name, name)
        self.assertEqual(debt.balance, balance)
        self.assertEqual(debt.balance, balance)
        self.assertEqual(debt._originalBalance, balance)
        self.assertEqual(debt.rate, rate)
        self.assertEqual(debt.minPayment, minPayment)
        self.assertEqual(debt.loanTerm, loanTerm)
        self.assertEqual(debt.purchasePrice, purchasePrice)
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

        purchasePrice = 3000.00
        debt.purchasePrice = purchasePrice
        self.assertEqual(debt.purchasePrice, purchasePrice)

    def test_inequality_comparison(self):
        id = 0
        name = 'bob'
        balance = 500.00
        purchasePrice = 2500.00
        rate = 0.06
        minPayment = 45.00
        loanTerm = 12
        totalInterestt = 0.0

        avalanche1 = StandardAmortized(id, 'bob', purchasePrice, 1000.00, 1000.00, 0.06, 50.0, 50)
        avalanche2 = StandardAmortized(id, 'bill', purchasePrice, 100.00, 1000.00, 0.12, 50.0, 50)
        self.assertTrue(avalanche1 < avalanche2)
        self.assertFalse(avalanche1 > avalanche2)
        avalanche1.rate = 0.12
        self.assertTrue(avalanche1 >= avalanche2)
        self.assertTrue(avalanche1 <= avalanche2)

        snow1 = StandardAmortized(id, 'bob', purchasePrice, 100.00, 100.00, 0.06, 50.0, 50, method='snowball')
        snow2 = StandardAmortized(id, 'bill', purchasePrice, 2000.00, 2000.00, 0.12, 50.0, 50, method='snowball')
        self.assertTrue(snow1 < snow2)
        self.assertFalse(snow1 > snow2)
        snow1.balance = 2000.00
        self.assertTrue(snow1 >= snow2)
        self.assertTrue(snow1 <= snow2)

    def test_equality_comparison(self):

        d1 = StandardAmortized(0, 'bob', 4000.0, 1000.00, 1000.00, 0.06, 50.0, 50)
        d2 = StandardAmortized(0, 'bill', 400.0, 100.00, 100.00, 0.12, 50.0, 50)
        d3 = StandardAmortized(0, 'bill', 400.0,100.00, 1000.00, 0.12, 50.0, 50)
        self.assertTrue(d1 != d2)
        self.assertFalse(d1 == d2)
        self.assertTrue(d2 == d3)
        self.assertFalse( d2 != d3)

    def test_compute_interest_savings(self):
        # name, purchasePrice, balance, originalBalance, rate, minPayment, loanTerm, paymentsMade = 0, pmiPayment = 0, method = 'avalanche'):
        d3 = StandardAmortized(0, 'bill', 400.0, 100.00, 100.00, 0.12, 50.0, 50)
        self.assertIsNone(d3.possibleInterestSavings)

        d3.totalInterest = 500
        d3.calculatePossibleInterestSavings()
        self.assertEqual(d3._possibleInterestSavings, -498.47)

    def test_compute_max_interest(self):
        d1 = StandardAmortized(0,'bob', 4000.0, 1000.00, 1000.00, 0.06, 50.0, 50)
        self.assertAlmostEqual(d1.maxInterest, 56.25, places=1)
        d2 = StandardAmortized(0, 'bill', 400.0, 100.00, 100.00, 0.12, 50.0, 50)
        self.assertAlmostEqual(d2.maxInterest, 1.53, places=1)

    def test_remaining_principle_calculator(self):
        d = StandardAmortized(0, 'Xavier', 250000.0, 200000.00, 200000.00, 0.05, 1000.00, 3600, paymentsMade=36, method='avalanche')
        self.assertAlmostEqual(d.balance, 193541.11, delta=5.0)

        d = StandardAmortized(0, 'James', 250000.0,150000.00, 150000.00, 0.08, 1438.00, 3600, paymentsMade=72, method='avalanche')
        self.assertAlmostEqual(d.balance, 109692.91, delta=5.0)


if __name__ == '__main__':
    unittest.main()
