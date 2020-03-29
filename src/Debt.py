

class Debt:

    def __init__(self, name, balance, rate, minPayment, loanTerm, method='avalanche'):
        self._name = name
        self._balance = balance
        self._rate = rate
        self._minPayment = minPayment
        self._loanTerm = loanTerm
        self.method = method

        # calculation variables
        self._totalInterest = 0.00

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
    def totalInterest(self):
        return self._totalInterest

    @totalInterest.setter
    def totalInterest(self, interest):
        self._totalInterest = interest

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