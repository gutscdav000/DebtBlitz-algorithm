from src.Debt import Debt
from datetime import datetime

class StandardAmortized(Debt):

    def __init__(self, name, balance, rate, minPayment, loanTerm, paymentsMade=0, method='avalanche'):
        super().__init__(name, balance, rate, method)

        self._minPayment = minPayment
        self._loanTerm = loanTerm
        self._paymentsMade = paymentsMade
        # calculation variables
        self._maxPeriods, self._maxInterest = self.calculateMaxInterest()
        # calculate forward looking interest and current balance


    @property
    def minPayment(self):
        return self._minPayment

    @minPayment.setter
    def minPayment(self, mp):
        self._minPayment = mp

    @property
    def loanTerm(self):
        return self._loanTerm

    @loanTerm.setter
    def loanTerm(self, lt):
        self._loanTerm = lt

    @property
    def possibleInterestSavings(self):
        return self._possibleInterestSavings

    @property
    def maxInterest(self):
        return self._maxInterest

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

    @property
    def paymentsMade(self):
        return self._paymentsMade

    @paymentsMade.setter
    def paymentsMade(self, pm):
        self._paymentsMade = pm

    def calculateMaxInterest(self):
        maxInterest = 0.0
        maxMonths = 0
        balance = self._originalBalance

        while balance >= 0:
            interest = round(balance * (self._rate / 12), 2)
            balance -= round(self._minPayment - interest, 2)
            maxInterest += interest
            maxInterest = round(maxInterest, 2)
            maxMonths += 1

        return maxMonths, maxInterest

    def updatePrincipleCaclulation(self):
        pass
