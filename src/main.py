from src.Debt import Debt
from src.StandardAmortized import StandardAmortized
from src.CreditCard import CreditCard
from src.Heloc import Heloc
from src.DateUtilities import monthDayMap, nextMonthGen
from src.FileUtilities import loadDebtsFromJson, loadDebtsfromFile
from src.DebtDAO import DebtDAO
from datetime import datetime
from heapq import _heapify_max, heapify
import csv, os


def main(debts, discretionary, method, actionMonths):
    g = nextMonthGen()



    if method == 'avalanche':
        _heapify_max(debts)  # max-heap: (i.e. descending order)
    else:
        heapify(debts)  # min-heap

    results = []
    totalDiscretionary = discretionary
    count = 1
    month, year = next(g)
    while debts:
        termDiscretionary = totalDiscretionary
        for debt in debts:
            #logic here to differentiate loan types
            if type(debt) == StandardAmortized:
                interest = round(debt.balance * (debt.rate / 12), 2)
                principal = round(debt.minPayment - interest, 2)
                debt.balance -= principal
            elif type(debt) == CreditCard:
                # daily rate * balance * days this cycle
                interest = round(debt.balance * (debt.rate / 365) * monthDayMap.get(month),2)
                principal = round((debt.minPaymentPercentage * debt.balance) - interest, 2)
                debt.balance -= principal
            elif type(debt) == Heloc:
                interest = round((debt.balance * (debt.rate / 365)) * monthDayMap.get(month), 2)
                principal = round(debt.minPayment - interest, 2)
                debt.balance -= principal

            if termDiscretionary > 0:  # subtract extra discretionary from highest weighted debt(s)
                debt.balance -= round(termDiscretionary, 2)
                principal += termDiscretionary

            if count <= actionMonths:
                debt.actions.append([count, interest, principal])

            debt.totalInterest += interest
            debt.totalInterest = round(debt.totalInterest, 2)

            # reset balance, add metadata, and dequeue
            if debt.balance <= 0.0:
                # reset balance (add difference in balance back to discretionary) *** possible error here in else case *** should be zero?
                termDiscretionary = termDiscretionary + (debt.balance * -1) if debt.balance < 0.0 else termDiscretionary
                debt.balance = 0.0

                debt.periodsToPayoff = count
                debt.payoffDate = (month, year)
                debt.calculatePossibleInterestSavings()
                print(f"debt: {debt.name} periods: {debt.periodsToPayoff} max periods: {debt.maxInterest} payoff Date: {debt.payoffDate} total paid interest  {debt.totalInterest} max interest possible: {debt.maxInterest} interest savings: {debt.possibleInterestSavings}")
                print("actions: ")
                print(debt.actions)
                results.append([debt.name, debt.periodsToPayoff, debt.payoffDate, debt.maxPeriods, debt.totalInterest, debt.maxInterest])
                debts.remove(debt)

        month, year = next(g)
        count += 1

    return results

if __name__ == '__main__':
    file = None; jsonObj = None; userId = 1; method = 'avalanche'; actionMonths = 12; discretionary = 200.0

    if file:
        debts = loadDebtsfromFile(file, method)
    elif jsonObj:
        debts = loadDebtsFromJson(jsonObj, method)
    elif userId is not None:
        # load debts...
        debtDao = DebtDAO(userId, method)
        debts = debtDao.retrieveDebts()
    else:
        # d0 = StandardAmortized("example house", 240000, 0.0375, 1111.0, 30*12, method=method)
        # d0 = StandardAmortized("example car", 20000, 0.045, 373.0, 5 * 12, method=method)
        # d0 = StandardAmortized("example student", 25000, 0.0465, 261.0, 10*12, method=method)
        # d0 = CreditCard("example credit", 5000.0, 0.1, 0.02, 320.0,method=method)
        # d0 = Heloc("Heloc a la Gucci", 5000.0, 0.0375, 100.0)
        # d0 = Heloc("Big boi Heloc", 25000.0, 0.0375, 100.0)
        # debts = [d1, d2, d3]
        d0 = StandardAmortized("david house", 250000, 200000, 0.05, 1074.0, 30 * 12, method=method)
        debts = [d0]

    print('-----start-----')
    for debt in debts:
        print(debt)
    # method = 'snowball'
    # fomatted [name, periodsToPayoff, payoffDate, totalInterest, possibleInterestSavings]
    # [name, periodsToPayoff, debt.payoffDate, maxPeriods,totalInterest paid, maxInterest possible]
    results = main(debts, discretionary=discretionary, method='avalanche', actionMonths=actionMonths)
    print('-----finish-----')
    # print(results)