from src.Debt import Debt

class StandardAmortized(Debt):

    def __init__(self, name, balance, rate, minPayment, loanTerm, method='avalanche'):
        super().__init__(name, balance, rate, method)

        self._minPayment = minPayment
        self._loanTerm = loanTerm
        # calculation variables
        #TODO not sure if this will be the same for credit
        self._maxInterest = self.calculateMaxInterest()


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

    def calculateMaxInterest(self):
        maxInterest = 0.0
        balance = self._originalBalance

        while balance >= 0:
            interest = balance * (self._rate / 12)
            balance -= self._minPayment - interest
            maxInterest += interest

        return maxInterest

    # def calculatePossibleInterestSavings(self):
    #     assert self._totalInterest > 0
    #     self._possibleInterestSavings = self._maxInterest - self._totalInterest