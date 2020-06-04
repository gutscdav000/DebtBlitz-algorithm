from src.Debt import Debt
from src.Heloc import Heloc
from src.CreditCard import CreditCard
from src.StandardAmortized import StandardAmortized
from datetime import datetime
import os, csv

def loadDebtsfromFile(fileName, method):
    with open(fileName, 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')

        debts = []; expected_results = []; i = 0
        for row in csv_reader:
            if i == 0:
                discretionary = float(row[0])
                i += 1
                continue

            if row[1] == "StandardAmortized":
                #amortized,StandardAmortized,250000.0,200000,200000,0.05,1074.0, 360, 186342.64, 0.0, 360, 0
                #name, purchasePrice, balance, originalBalance, rate, minPayment, loanTerm, paymentsMade=0, pmiPayment=0, method='avalanche'
                debts.append(StandardAmortized(str(row[0]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]), int(row[7]), method=method))
                expected_results.append((float(row[8]), float(row[9]), int(row[10]), int(row[11])))
            elif row[1] == "CreditCard":
                debts.append(CreditCard(str(row[0]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]), method=method))
                expected_results.append((float(row[7]), float(row[8]), int(row[9]), int(row[10])))
            elif row[1] == "Heloc":
                # name, balance, originalBalance, rate, minPayment, method='avalanche'
                debts.append(Heloc(str(row[0]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), method=method))
                expected_results.append((float(row[6]), float(row[7]), int(row[8]), int(row[9])))

            i += 1

        return debts, expected_results, discretionary


# probably will be implemented for the web service. . . Eventually
def loadDebtsFromJson(jsonObj, method):
    pass