import unittest
from src.Debt import Debt

class MyTestCase(unittest.TestCase):
    def simple_property_tests(self):
        name = 'bob'
        balance = 500.00
        rate = 0.06
        minPayment = 45.00
        loanTerm = 12

        debt = Debt(name, balance, rate, minPayment, loanTerm)

        self.assertEqual(debt.name, name)
        self.assertEqual(debt.balance, balance)
        self.assertEqual(debt.balance, balance)
        self.assertEqual(debt.rate, rate)
        self.assertEqual(debt.minPayment, minPayment)
        self.assertEqual(debt.loanTerm, loanTerm)

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


if __name__ == '__main__':
    unittest.main()
