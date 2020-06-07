from datetime import datetime
from src.DbConn import DbConn
from src.StandardAmortized import StandardAmortized
from src.CreditCard import CreditCard
from src.Heloc import Heloc
from src.Debt import Debt

class DebtDAO(DbConn):
    def __init__(self, userId, method):
        super().__init__("localhost", "ApplicationDb", "postgres", "postgres")
        self._userId = userId
        self._method = method

    def retrieveDebts(self):
        result = self.execute_query(f"""SELECT d.id,
                   d.name,
                   d.user_id,
                   d.debt_type,
                   d.lender,
                   d.original_balance,
                   d.balance,
                   d.rate,
                   d.interest_paid,
                   d.periods_to_payoff,
                   d.payoff_date,
                   d.max_interest,
                   d.min_payment_value,
                   d.min_payment_percent,
                   d.loan_term,
                   d.remaining_term,
                   d.pmi,
                   d.purchase_price,
                   d.max_periods,
                   d.escrow,
                   d.max_loc
            FROM public.debt d 
            WHERE d.user_id = {self._userId}
        """)

        debts = []
        for d in result:
            if d[3] in ["Mortgage", "Auto Loan", "Student Loan"]:
                #name, purchasePrice, balance, originalBalance, rate, minPayment, loanTerm, paymentsMade = 0, pmiPayment = 0, method = 'avalanche'
                pmi = d[16] if d[16] > 0 else 0
                dbt = StandardAmortized(d[0], d[1], float(d[17]), float(d[6]), float(d[5]), float(d[7]), float(d[12]), float(d[14]), int(d[14]) - int(d[15]), self._method)
                dbt.debtHistory = d
                debts.append(dbt)
            elif d[3] == "Credit Card":
                # name, balance, originalBalance, rate, minPaymentPercentage, minPaymentValue, method='avalanche'
                dbt = CreditCard(d[0], d[1], float(d[6]), float(d[5]), float(d[7]), float(d[13]), float(d[12]), method=self._method)
                dbt.debtHistory = d
                debts.append(dbt)
            else: #Line of Credit
                # name, balance, originalBalance, rate, minPayment, method='avalanche'
                dbt = Heloc(d[0], d[1], float(d[6]), float(d[5]), float(d[7]), float(d[12]), method=self._method)
                dbt.debtHistory = d
                debts.append(dbt)

        return debts


    def updateDebt(self, debt: Debt):
        self.__insertHistory(debt.debtHistory)
        self.__updateDebt(debt)

    def updateActions(self, debt: Debt):
        userId = self.__findDebtUserId(debt.id)
        if userId is not None:
            self.__deleteActions(debt.id)
            self.__insertActions(debt.actions, debt.id, userId)

    def __insertHistory(self, debtHist: list):
        stamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        sql = f"""INSERT INTO PUBLIC.DEBT_HIST (ID, NAME, USER_ID, DEBT_TYPE, LENDER, ORIGINAL_BALANCE, BALANCE, RATE,
                                     INTEREST_PAID, PERIODS_TO_PAYOFF, PAYOFF_DATE, MAX_INTEREST, MIN_PAYMENT_VALUE,
                                     MIN_PAYMENT_PERCENT, LOAN_TERM, REMAINING_TERM, PMI, PURCHASE_PRICE, MAX_PERIODS,
                                     ESCROW, MAX_LOC, UPDATE_STAMP)
           VALUES ({debtHist[0]}, '{debtHist[1].replace("'", "''")}', {debtHist[2]}, '{debtHist[3]}', '{debtHist[4]}', {debtHist[5]}, {debtHist[6]}, {debtHist[7]},
                   {debtHist[8]}, {debtHist[9]}, '{debtHist[10]}', {debtHist[11]}, {debtHist[12]}, {debtHist[13]}, {debtHist[14]}, {debtHist[15]},
                   {debtHist[16]}, {debtHist[17]}, {debtHist[18]},{debtHist[19]}, {debtHist[20]}, '{stamp}')
        """
        self.execute_query(sql, commit=True)

    def __updateDebt(self, debt: Debt):
        sql = f"""UPDATE PUBLIC.DEBT
             SET ORIGINAL_BALANCE={debt.originalBalance},
                 -- BALANCE={debt.balance},
                 PERIODS_TO_PAYOFF={debt.periodsToPayoff},
                 PAYOFF_DATE='{debt.payoffDate.strftime("%Y-%m-%d")}',
                 MAX_INTEREST={debt.maxInterest},
                 REMAINING_TERM={debt.periodsToPayoff},
                 MAX_PERIODS={debt.maxPeriods}
              WHERE ID = {debt.id}
           """
        self.execute_query(sql, commit=True)

    def __findDebtUserId(self, debtId: int):
        sql = f"""select user_id from public.debt
                 where id = {debtId}"""
        result = self.execute_query(sql)
        return result[0][0] if result is not None else None

    def __deleteActions(self, debtId: int):
        sql = f"delete from public.action where debt_id = {debtId}"
        self.execute_query(sql, commit=True)

    def __insertActions(self, actions: list, debtId: int, userId: int):
        for action in actions:
            sql = f"""insert into public.action (debt_id, user_id, principal, interest, pay_date) 
                      values ({debtId}, {userId}, {action[1]}, {action[0]}, '0001-01-01')"""
            self.execute_query(sql, commit=True)
