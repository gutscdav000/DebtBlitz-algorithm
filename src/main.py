from src.Debt import Debt
from src.StandardAmortized import StandardAmortized
from src.CreditCard import CreditCard
from src.utils import monthDayMap, nextMonthGen, loadDebtsFromJson, loadDebtsfromFile
from datetime import datetime
from heapq import _heapify_max, heapify
import csv, os


def main(method, file=None, jsonObj=None):
    g = nextMonthGen()


    if file:
        debts = loadDebtsfromFile(file, method)
    elif jsonObj:
        debts = loadDebtsFromJson(jsonObj, method)
    else:
        # d0 = StandardAmortized("example house", 240000, 0.0375, 1111.0, 30*12, method=method)
        # d0 = StandardAmortized("example car", 20000, 0.045, 373.0, 5 * 12, method=method)
        # d0 = StandardAmortized("example student", 25000, 0.0465, 261.0, 10*12, method=method)
        # TODO calculate daily interest paid off monthly.
        d0 = CreditCard("example credit", 5000.0, 0.1, 0.02, method=method)
        # d0 = Heloc()
        # debts = [d1, d2, d3]
        debts = [d0]

    if method == 'avalanche':
        _heapify_max(debts)  # max-heap: (i.e. descending order)
    else:
        heapify(debts)  # min-heap

    results = []
    totalDiscretionary = 200.0
    count = 1
    month, year = next(g)
    while debts:
        termDiscretionary = totalDiscretionary
        for debt in debts:
            #logic here to differentiate loan types
            if type(debt) == StandardAmortized:
                interest = debt.balance * (debt.rate / 12)
                debt.balance -= debt.minPayment - interest
            elif type(debt) == CreditCard:
                # daily rate * balance * days this cycle
                interest = (debt.balance * (debt.rate / 365)) * monthDayMap.get(month)
                debt.balance -= (debt.minPaymentPercentage * debt.balance) - interest

            if termDiscretionary > 0:  # subtract extra discretionary from highest weighted debt
                debt.balance -= termDiscretionary
            debt.totalInterest += interest

            # reset balance, add metadata, and dequeue
            if debt.balance <= 0.0:
                # reset balance (add difference in balance back to discretionary) *** possible error here in else case *** should be zero?
                termDiscretionary = termDiscretionary + (debt.balance * -1) if debt.balance < 0.0 else termDiscretionary
                debt.balance = 0.0

                debt.periodsToPayoff = count
                debt.payoffDate = (month, year)
                debt.calculatePossibleInterestSavings()
                print(f"debt: {debt.name} periods: {debt.periodsToPayoff} payoff Date: {debt.payoffDate} total paid interest  {debt.totalInterest} max interest possible: {debt.maxInterest} interest savings: {debt.possibleInterestSavings}")
                results.append([debt.name, debt.periodsToPayoff, debt.payoffDate, debt.totalInterest, debt.possibleInterestSavings])
                debts.remove(debt)

        month, year = next(g)
        count += 1

    return results

if __name__ == '__main__':

    print('-----start-----')
    # method = 'snowball'
    # fomatted [name, periodsToPayoff, payoffDate, totalInterest, possibleInterestSavings]
    results = main(method='avalanche')#, file=os.path.join('..', 'test', 'TestFiles', 'simple_test_1.csv'))
    print('-----finish-----')
    print(results)