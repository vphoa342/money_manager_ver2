import pandas as pd

class Month:
    def __init__(self, necessity, play, savings, education, financialFreedom):
        self.necessity = necessity
        self.play = play
        self.savings = savings
        self.education = education
        self.financialFreedom = financialFreedom
    def addMoney(self, value, type):
        if type == 'necessity': self.necessity += value
        elif type == 'play': self.play += value
        elif type == 'savings': self.savings += value
        elif type == 'education': self.education += value
        else: self.financialFreedom += value


class Account:
    def __init__(self, total):
        self.total = total
    def addMoney(self, amount):
        self.total += amount
    def minusMoney(self, amount):
        self.total -= amount
    def updateMoney(self, newValue):
        self.total = newValue
    def transferMoney(self, other, value):
        self.total -= value
        other.total += value

fileTxt = 'C:\\Users\\Van Phu Hoa\\PycharmProjects\\income_outcome\\funds_database.txt'
try:
    file = open(fileTxt, mode='r')

    string = file.readline().split()
    wage = int(string[1])

    #read bidv, momo, finhay, wallet
    string = file.readline().split()
    curBIDV = int(string[1])

    string = file.readline().split()
    curMomo = int(string[1])

    string = file.readline().split()
    curFinhay = int(string[1])

    string = file.readline().split()
    curWallet = int(string[1])

    string = file.readline().split()
    curInvestmentAccount = int(string[1])
finally:
    file.close()


#create accounts
BIDV = Account(curBIDV)
momo = Account(curMomo)
finhay = Account(curFinhay)
wallet = Account(curWallet)
investmentAccount = Account(curInvestmentAccount)
"# moneyTracker" 
