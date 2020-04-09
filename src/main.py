from src.Debt import Debt
from src.StandardAmortized import StandardAmortized
from src.CreditCard import CreditCard
from datetime import datetime
from heapq import _heapify_max, heapify
import csv, os

def nextMonthGen():
    now = str(datetime.date(datetime.now()))
    year, month, _ = now.split('-')
    year = int(year)
    month = int(month)
    while True:
        if month >= 12:
            month = 1
            year += 1
            yield month, year
        else:
            month += 1
            yield month, year

def loadDebtsfromFile(fileName, method):
    with open(fileName, 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')

        return [Debt(str(row[0]), float(row[1]), float(row[2]), float(row[3]), int(row[4]), method=method) for row in csv_reader ]


# probably will be implemented for the web service. . . Eventually
def loadDebtsFromJson(jsonObj, method):
    pass

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
        d0 = CreditCard("example credit", 5000.0, 0.1, 0.02, method=method)
        # d1 = Debt("card 1", 4400.0, 0.13, 50.0, 60, method=method)
        # d2 = Debt("auto loan 1", 3200.0, 0.0981, 30.0, 60, method=method)
        # d3 = Debt("student loan", 4900.0, 0.04, 25.0, 60, method=method)
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
                interest = debt.balance * (debt.rate / 12)
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