from src.Debt import Debt
from datetime import datetime
import heapq


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
    # month, year = next(g)

    d1 = Debt("card 1", 4400.0, 0.13, 50.0, 60)
    d2 = Debt("auto loan 1", 3200.0, 0.0981, 30.0, 60)
    d3 = Debt("student loan", 4900.0, 0.04, 25.0, 60)

    q = []
    heapq.heappush(q, d1)
    heapq.heappush(q, d2)
    heapq.heappush(q, d3)

    # dequeue op: next_item = heapq.heappop(q)
    while q:
        pass
