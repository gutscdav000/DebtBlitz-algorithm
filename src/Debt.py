

class Debt:

    def __init__(self, name, balance, rate, minPayment, loanTerm):
        self._name = name
        self._balance = balance
        self._rate = rate
        self._minPayment = minPayment
        self._loanTerm = loanTerm

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