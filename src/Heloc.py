from src.Debt import Debt
from src.DateUtilities import monthDayMap, nextMonthGen
from datetime import datetime

class Heloc(Debt):

    def __init__(self, name, balance, rate, minPayment, method='avalanche'):
        super().__init__(name, balance, rate, method)
        self._minPayment = minPayment
        # calculation variables
        self._maxPeriods, self._maxInterest = self.calculateMaxInterest()

    @property
    def minPayment(self):
        return self._minPayment

    @minPayment.setter
    def minPayment(self, mp):
        self._minPayment = mp

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

            interest = round((balance * (self.rate / 365)) * monthDayMap.get(month), 2)
            if balance + interest <= 0.01:
                balance -= balance + interest
            else:
                balance -= round(self.minPayment - interest, 2)

            maxInterest += interest
            maxInterest = round(maxInterest, 2)
            maxMonths += 1

        self.maxPayoffDate = (month, year)
        return maxMonths, maxInterest