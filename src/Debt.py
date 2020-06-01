from datetime import datetime

class Debt:

    def __init__(self, name, balance, rate, method='avalanche'):
        self._name = name
        self._balance = balance
        self._originalBalance = balance
        self._rate = rate
        self.method = method
        # calculation variables
        self._totalInterest = 0.00
        self._periodsToPayoff = 0
        self._payoffDate = None
        self._maxInterest = None
        self._possibleInterestSavings = None
        self.actions = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, n):
        self._name = n

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, b):
        self._balance = b

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, r):
        self._rate = r

    @property
    def totalInterest(self):
        return self._totalInterest

    @totalInterest.setter
    def totalInterest(self, interest):
        self._totalInterest = interest

    @property
    def periodsToPayoff(self):
        return self._periodsToPayoff

    @periodsToPayoff.setter
    def periodsToPayoff(self, n):
        self._periodsToPayoff = n

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
    def maxInterest(self):
        return self._maxInterest

    @property
    def payoffDate(self):
        return self._payoffDate

    @payoffDate.setter
    def payoffDate(self, tupl):
        try:
            month, year = tupl
        except ValueError:
            raise ValueError("Pass an iterable with two items: (e.g (month, year))")
        else:
            dt_str = str(year) + '-' + str(month) + '-1'
            self._payoffDate = datetime.strptime(dt_str, "%Y-%m-%d")

    # @property
    # def maxInterest(self):
    #     return self._maxInterest

    @property
    def possibleInterestSavings(self):
        return self._possibleInterestSavings

    def __eq__(self, other):
        return self.balance == other.balance and \
               self.rate == other.rate and \
               self.name == other.name and \
               self.minPayment == other.minPayment and \
               self.loanTerm == other.loanTerm

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if self.method == 'avalanche':
            return self.rate < other.rate
        else:
            return self.balance < other.balance

    def __gt__(self, other):
        if self.method == 'avalanche':
            return self.rate > other.rate
        else:
            return self.balance > other.balance

    def __ge__(self, other):
        if self.method == 'avalanche':
            return self.rate >= other.rate
        else:
            return self.balance >= other.balance

    def __le__(self, other):
        if self.method == 'avalanche':
            return self.rate <= other.rate
        else:
            return self.balance <= other.balance

    def calculatePossibleInterestSavings(self):
        assert self._totalInterest > 0
        self._possibleInterestSavings = self._maxInterest - self._totalInterest