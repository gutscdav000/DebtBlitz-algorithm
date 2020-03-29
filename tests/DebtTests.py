import unittest
from src.Debt import Debt

class MyTestCase(unittest.TestCase):
    def simple_property_tests(self):
        name = 'bob'
        balance = 500.00
        rate = 0.06
        minPayment = 45.00
        loanTerm = 12
        totalInterestt = 0.0

        debt = Debt(name, balance, rate, minPayment, loanTerm)

        self.assertEqual(debt.name, name)
        self.assertEqual(debt.balance, balance)
        self.assertEqual(debt.balance, balance)
        self.assertEqual(debt.rate, rate)
        self.assertEqual(debt.minPayment, minPayment)
        self.assertEqual(debt.loanTerm, loanTerm)
        # calculated values
        self.assertEqual(debt.totalInterest, totalInterestt)

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

    def operator_comparison_tests(self):
        name = 'bob'
        balance = 500.00
        rate = 0.06
        minPayment = 45.00
        loanTerm = 12
        totalInterestt = 0.0

        avalanche1 = Debt('bob', 1000.00, 0.06, 50.0, 50)
        avalanche2 = Debt('bill', 100.00, 0.12, 50.0, 50)
        self.assertTrue(avalanche1 < avalanche2)
        self.assertTrue(avalanche1 != avalanche2)
        self.assertFalse(avalanche1 > avalanche2)
        avalanche1.rate = 0.12
        self.assertTrue(avalanche1 == avalanche2)
        self.assertTrue(avalanche1 >= avalanche2)
        self.assertTrue(avalanche1 <= avalanche2)

        snow1 = Debt('bob', 100.00, 0.06, 50.0, 50, method='snowball')
        snow2 = Debt('bill', 2000.00, 0.12, 50.0, 50, method='snowball')
        self.assertTrue(snow1 < snow2)
        self.assertTrue(snow1 != snow2)
        self.assertFalse(snow1 > snow2)
        snow1.balance = 2000.00
        self.assertTrue(snow1 == snow2)
        self.assertTrue(snow1 >= snow2)
        self.assertTrue(snow1 <= snow2)


if __name__ == '__main__':
    unittest.main()
