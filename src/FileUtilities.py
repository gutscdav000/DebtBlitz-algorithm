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
                debts.append(StandardAmortized(str(row[0]), float(row[2]), float(row[3]), float(row[4]), int(row[5]), method=method))
                #TODO expected
            elif row[1] == "CreditCard":
                debts.append(CreditCard(str(row[0]), float(row[2]), float(row[3]), float(row[4]), method=method))
                # TODO expected
            elif row[1] == "Heloc":
                debts.append(Heloc(str(row[0]), float(row[2]), float(row[3]), float(row[4]), method=method))
                expected_results.append((float(row[5]), float(row[6]), int(row[7]), int(row[8])))

            i += 1

        return debts, expected_results, discretionary


# probably will be implemented for the web service. . . Eventually
def loadDebtsFromJson(jsonObj, method):
    pass