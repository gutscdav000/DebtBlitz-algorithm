from src.Debt import Debt
from src.DateUtilities import monthDayMap, nextMonthGen
from datetime import datetime

class CreditCard(Debt):

    def __init__(self, id, name, balance, originalBalance, rate, minPaymentPercentage, minPaymentValue, method='avalanche'):
        super().__init__(id, name, balance, originalBalance, rate, method)
        self._minPaymentPercentage = minPaymentPercentage
        self._minPaymentValue = minPaymentValue
        # calculation variables
        self._maxPeriods, self._maxInterest = self.calculateMaxInterest()

    @property
    def minPaymentPercentage(self):
        return self._minPaymentPercentage

    @minPaymentPercentage.setter
    def minPaymentPercentage(self, mp):
        self._minPaymentPercentage = mp

    @property
    def minPaymentValue(self):
        return self._minPaymentValue

    @minPaymentValue.setter
    def minPaymentValue(self, mp):
        self._minPaymentValue = mp

    @property
    def maxPeriods(self):
        return self._maxPeriods

    def calculateMaxInterest(self):
        g = nextMonthGen()

        maxInterest = 0.0
        maxMonths = 0
        balance = self.originalBalance
        while balance > 0:
            month, year = next(g)
            # interest = balance * (self._rate / 12)
            interest = (balance * (self.rate / 365)) * monthDayMap.get(month)
            interest = round(interest, 2)
            if balance + interest <= self.minPaymentValue: # NOTE: this will depend on credit card and should be parameterized
                balance -= balance + interest
            else:
                balance -= round((self.minPaymentPercentage * balance) - interest, 2)

            self.maxPayoffDate = (month, year)
            maxInterest += interest
            maxInterest = round(maxInterest, 2)
            maxMonths += 1

        return maxMonths, maxInterest
