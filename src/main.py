from src.Debt import Debt
from datetime import datetime
from heapq import _heapify_max, heapify

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



if __name__ == '__main__':

    print('-----start-----')
    g = nextMonthGen()
    method = 'snowball'
    # method = 'avalanche'

    d1 = Debt("card 1", 4400.0, 0.13, 50.0, 60, method=method)
    d2 = Debt("auto loan 1", 3200.0, 0.0981, 30.0, 60, method=method)
    d3 = Debt("student loan", 4900.0, 0.04, 25.0, 60, method=method)

    debts = [d1, d2, d3]
    if method == 'avalanche':
        _heapify_max(debts) # max-heap: (i.e. descending order)
    else:
        heapify(debts) # min-heap


    totalDiscretionary = 100.0
    count = 1
    month, year = next(g)
    while debts:
        termDiscretionary = totalDiscretionary
        for debt in debts:
            interest = debt.balance * (debt.rate / 12)
            debt.balance -= debt.minPayment - interest

            if termDiscretionary > 0: # subtract extra discretionary from highest weighted debt
                debt.balance -= termDiscretionary
            debt.totalInterest += interest

            # reset balance, add metadata, and dequeue
            if debt.balance <= 0.0:
                # reset balance (add difference in balance back to discretionary)
                termDiscretionary = termDiscretionary + (debt.balance * -1) if debt.balance < 0.0 else termDiscretionary
                debt.balance = 0.0

                debt.periodsToPayoff = count
                debt.payoffDate = (month, year)
                debt.calculatePossibleInterestSavings()
                debts.remove(debt)
                print(f"debt: {debt.name} periods: {debt.periodsToPayoff} payoff Date: {debt.payoffDate} total paid interest  {debt.totalInterest} interest savings: {debt.possibleInterestSavings}")


        month, year = next(g)
        count += 1

    print('-----finish-----')
