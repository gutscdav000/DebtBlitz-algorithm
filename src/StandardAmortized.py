from src.Debt import Debt

class StandardAmortized(Debt):

    def __init__(self, name, purchasePrice, balance, originalBalance, rate, minPayment, loanTerm, paymentsMade=0, pmiPayment=0, method='avalanche'):
        super().__init__(name, balance, originalBalance, rate, method)

        self._minPayment = minPayment
        self._loanTerm = loanTerm
        self._paymentsMade = paymentsMade
        self._pmiPayment = pmiPayment
        self._purchasePrice = purchasePrice
        # calculation variables
        self.__endPmiValue = purchasePrice * 0.2
        self.updatePrincipleCaclulation()
        self._maxPeriods, self._maxInterest = self.calculateMaxInterest()


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
    def maxPeriods(self):
        return self._maxPeriods

    @property
    def paymentsMade(self):
        return self._paymentsMade

    @paymentsMade.setter
    def paymentsMade(self, pm):
        self._paymentsMade = pm

    @property
    def pmiPayment(self):
        return self._pmiPayment

    @pmiPayment.setter
    def pmiPayment(self, pmi):
        self._pmiPayment = pmi

    @property
    def purchasePrice(self):
        return self._purchasePrice

    @purchasePrice.setter
    def purchasePrice(self, pp):
        self._purchasePrice = pp


    def calculateMaxInterest(self):
        maxInterest = 0.0
        maxMonths = 0
        balance = self._originalBalance

        while balance > 0:

            if balance <= self.__endPmiValue:
                self.__endPmiValue = 0

            interest = round(balance * (self._rate / 12), 2)
            balance -= round(self._minPayment - interest, 2)
            maxInterest += interest
            maxInterest = round(maxInterest, 2)
            maxMonths += 1

        return maxMonths, maxInterest

    def updatePrincipleCaclulation(self):
        for i in range(self.paymentsMade):
            interest = round(self.balance * (self.rate / 12), 2)
            self.balance -= round(self.minPayment - interest, 2)
            # not sure if we want to include past interest
            # self.totalInterest += interest
            # self.totalInterest = round(self.totalInterest, 2)
