from src.DbConn import DbConn
from src.StandardAmortized import StandardAmortized
from src.CreditCard import CreditCard
from src.Heloc import Heloc

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
        # print(result)
        # for it in result[0]:
        #     print(it, type(it))

        debts = []
        for d in result:
            if d[3] in ["Mortgage", "Auto Loan", "Student Loan"]:
                #name, purchasePrice, balance, originalBalance, rate, minPayment, loanTerm, paymentsMade = 0, pmiPayment = 0, method = 'avalanche'
                pmi = d[16] if d[16] > 0 else 0
                dbt = StandardAmortized(d[1], float(d[17]), float(d[6]), float(d[5]), float(d[7]), float(d[12]), float(d[14]), int(d[14]) - int(d[15]), self._method)
                debts.append(dbt)
            elif d[3] == "Credit Card":
                # name, balance, originalBalance, rate, minPaymentPercentage, minPaymentValue, method='avalanche'
                dbt = CreditCard(d[1], float(d[6]), float(d[5]), float(d[7]), float(d[13]), float(d[12]), method=self._method)
                debts.append(dbt)
            else: #Line of Credit
                # name, balance, originalBalance, rate, minPayment, method='avalanche'
                dbt = Heloc(d[1], float(d[6]), float(d[5]), float(d[7]), float(d[12]), method=self._method)
                debts.append(dbt)

        return debts

