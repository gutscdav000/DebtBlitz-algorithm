from src.Debt import Debt

class CreditCard(Debt):

    def __init__(self, name, balance, rate, minPaymentPercentage, method='avalanche'):
        super().__init__(name, balance, rate, method)
        self._minPaymentPercentage = minPaymentPercentage
        # calculation variables
        self._totalInterest = 0.00
        self._periodsToPayoff = 0
        self._payoffDate = None
        self._maxInterest = self.calculateMaxInterest()

    @property
    def minPaymentPercentage(self):
        return self._minPaymentPercentage

    @minPaymentPercentage.setter
    def minPaymentPercentage(self, mp):
        self._minPaymentPercentage = mp

    @property
    def maxInterest(self):
        return self._maxInterest

    def calculateMaxInterest(self):
        maxInterest = 0.0
        balance = self._originalBalance
        while balance >= 0:
            interest = balance * (self._rate / 12)
            if balance <= 50.0:
                balance -= balance + interest
            else:
                balance -= (self._minPaymentPercentage * balance) - interest
            maxInterest += interest

        return maxInterest

    # def calculatePossibleInterestSavings(self):
    #     assert self._totalInterest > 0
    #     self._possibleInterestSavings = self._maxInterest - self._totalInterest