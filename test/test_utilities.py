import unittest
from src.DateUtilities import monthDayMap, nextMonthGen
from datetime import datetime

class TestUtilities(unittest.TestCase):
    def test_next_month_generator(self):
        g = nextMonthGen()
        now = str(datetime.date(datetime.now()))
        year, month, _ = now.split('-')
        year = int(year)
        month = int(month)

        # prepare compare dates
        for i in range(25):
            year = year + 1 if month == 12 else year
            month = 1 if month == 12 else month + 1
            genMonth, genYear = next(g)
            self.assertEqual(genMonth, month)
            self.assertEqual(genYear, year)



if __name__ == '__main__':
    unittest.main()
