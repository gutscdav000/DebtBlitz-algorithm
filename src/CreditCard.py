from src.Debt import Debt
from src.DateUtilities import monthDayMap, nextMonthGen
from datetime import datetime

class CreditCard(Debt):

    def __init__(self, name, balance, rate, minPaymentPercentage, method='avalanche'):
        super().__init__(name, balance, rate, method)
        self._minPaymentPercentage = minPaymentPercentage
        # calculation variables
        self._maxPeriods, self._maxInterest = self.calculateMaxInterest()

    @property
    def minPaymentPercentage(self):
        return self._minPaymentPercentage

    @minPaymentPercentage.setter
    def minPaymentPercentage(self, mp):
        self._minPaymentPercentage = mp

    @property
    def maxInterest(self):
        return self._maxInterest

    @property
    def maxPeriods(self):
        return self._maxPeriods

    @property
    def maxPayoffDate(self):
        return self._maxPayoffDate

    @maxPayoffDate.setter
    def maxPayoffDate(self, tupl):
        try:
            month, year = tupl
        except ValueError:
            raise ValueError("Pass an iterable with two items: (e.g (month, year))")
        else:
            dt_str = str(year) + '-' + str(month) + '-1'
            self._payoffDate = datetime.strptime(dt_str, "%Y-%m-%d")

    def calculateMaxInterest(self):
        g = nextMonthGen()

        maxInterest = 0.0
        maxMonths = 0
        balance = self._originalBalance
        while balance >= 0:
            month, year = next(g)
            # interest = balance * (self._rate / 12)
            interest = (balance * (self.rate / 365)) * monthDayMap.get(month)
            if balance + interest <= 50.0: # NOTE: this will depend on credit card and should be parameterized
                balance -= balance + interest
            else:
                balance -= (self.minPaymentPercentage * balance) - interest

            self.maxPayoffDate = (month, year)
            maxInterest += interest
            maxMonths += 1

        return maxMonths, maxInterest
