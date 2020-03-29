from src.Debt import Debt
from datetime import datetime
import heapq
from heapq import _heapify_max, heappop, heapify

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
    # TODO fix eq operator to look at more than rate/balance
    print('-----start-----')
    g = nextMonthGen()
    # method = 'snowball'
    method = 'avalanche'

    d1 = Debt("card 1", 4400.0, 0.13, 50.0, 60, method=method)
    d2 = Debt("auto loan 1", 3200.0, 0.0981, 30.0, 60, method=method)
    d3 = Debt("student loan", 4900.0, 0.04, 25.0, 60, method=method)

    debts = [d1, d2, d3]
    if method == 'avalanche':
        _heapify_max(debts) # max-heap: (i.e. descending order)
    else:
        heapify(debts) # min-heap

    min_payment = sum(d.minPayment for d in debts)
    totalDiscretionary = 100.0
    count = 1
    month, year = next(g)
    while debts:
        # TODO (still pondering the need for the extra variable) ig for when termDisc changes while iterating debts
        termDiscretionary = totalDiscretionary
        i = 0
        for debt in debts:
            interest = debt.balance * (debt.rate / 12)
            debt.balance -= debt.minPayment - interest

            if i == 0: # subtract extra discretionary from highest weighted debt
                debt.balance -= termDiscretionary
            debt.totalInterest += interest

            # reset balance, add metadata, and dequeue
            if debt.balance <= 0.0:
                # reset balance (add difference in balance back to discretionary)
                termDiscretionary = termDiscretionary + (debt.balance * -1) if debt.balance < 0.0 else termDiscretionary
                debt.balance = 0.0
                min_payment -= debt.minPayment

                # TODO add metadata to debt (e.g. pay off month-year, periods count, total interest)
                # not using heapop to ensure correct debt is being removed
                debts.remove(debt)
                print(f"debt: {debt.name} bal: {debt.balance} cnt: {count} month-year: {str(month)+'-'+str(year)}")

            i += 1

        month, year = next(g)
        count += 1

    print('-----finish-----')
