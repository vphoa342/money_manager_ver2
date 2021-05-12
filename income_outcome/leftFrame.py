import pandas as pd
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import funds

fileCSV = 'C:\\Users\\Van Phu Hoa\\PycharmProjects\\income_outcome\\{}\\{}_{}.csv'
month = {"01": 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun', '07': 'Jul',
         '08': 'Aug', '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}
typeList = ['necessity', 'education', 'financial freedom', 'savings', 'play']
typeAccount = ['BIDV', 'momo', 'finhay', 'wallet', 'investment account']
fundDict = {'BIDV': funds.BIDV, 'momo': funds.momo, 'finhay': funds.finhay,
            'wallet': funds.wallet, 'investment account': funds.investmentAccount}
fileTxt = 'C:\\Users\\Van Phu Hoa\\PycharmProjects\\income_outcome\\funds_database.txt'

def saveData():
    global fileTxt
    outputString = """wage: {}
BIDV: {}
momo: {}
finhay: {}
wallet: {}
investmentAccount: {}
    """
    try:
        file = open(fileTxt, mode='w+')
        file.writelines(outputString.format('5000000', funds.BIDV.total, funds.momo.total, funds.finhay.total,
            funds.wallet.total, funds.investmentAccount.total))
    finally:
        file.close()

def updateOutcomeData(output, date, list, type, amount, account):
    #get month from dd/mm/yyyy
    sheetName = month[date[3:5]]

    #export to csv
    database = pd.read_csv(fileCSV.format('outcome', sheetName, 'outcome'))
    database = database.append({"Date": date, "List": list, "Type": type, "Amount": int(amount)}, ignore_index=True)
    database.to_csv(fileCSV.format('outcome', sheetName, 'outcome'), index=False)

    #update to fund
    fundDict[account].minusMoney(int(amount))
    saveData()

    # create 12 month objects
    fileMonthData = 'C:\\Users\\Van Phu Hoa\\PycharmProjects\\income_outcome\\monthData.csv'
    monthData = pd.read_csv(fileMonthData)
    monthData.loc[int(date[3:5]) - 1][type] += int(amount)
    monthData.to_csv(fileMonthData, index=False)

    #remind goal
    remindString = """remain necessity: {}
    remain play: {}
    remain savings: {}
    remain education: {}
    remain financial freedom: {}
    """
    n, p, s, e, f = monthData.loc[int(date[3:5]) - 1]
    n1, p1, s1, e1, f1 = monthData.loc[12]
    output['text'] = remindString.format(n1 - n, p1 - p, s1 - s, e1 - e, f1 - f)


def updateIncomeData(date, list, account, amount):
    global database, sheetName, fundDict
    sheetName = month[date[3:5]]

    # export to csv
    database = pd.read_csv(fileCSV.format('income', sheetName, 'income'))
    database = database.append({"Date": date, "List": list, "Type": account, "Amount": int(amount)}, ignore_index=True)
    database.to_csv(fileCSV.format('income', sheetName, 'income'), index=False)

    # update to fund
    fundDict[account].addMoney(int(amount))
    saveData()

def createLeftFrame(mainWindow, output):
    global sheetName, typeList

    #left frame
    leftFrame = tk.Frame(mainWindow, bg='#aff8d8')
    leftFrame.place(relx=0.05, rely=0.05, relwidth=0.4, relheight=0.3)

    # data label
    dateLabel = tk.Label(leftFrame, text="Date")
    dateLabel.place(relx=0.05, rely=0.05, relwidth=0.1, relheight=0.075)
    dateEntry = tk.Entry(leftFrame, bg='#ff9aa2')
    dateEntry.place(relx=0.15, rely=0.05, relwidth=0.15, relheight=0.075)

    # type label
    typeLabel = tk.Label(leftFrame, text="Type")
    typeLabel.place(relx=0.05, rely=0.5, relwidth=0.1, relheight=0.4)
    typeEntry = tk.Listbox(leftFrame, bg='#ff9aa2', exportselection=0)
    for index in range(len(typeList)):
        typeEntry.insert('end', typeList[index])
    typeEntry.place(relx=0.15, rely=0.5, relwidth=0.15, relheight=0.4)

    #type account
    accountLabel = tk.Label(leftFrame, text='Account')
    accountLabel.place(relx=0.4, rely=0.5, relwidth=0.1, relheight=0.4)
    accountEntry = tk.Listbox(leftFrame, bg='#ff9aa2', exportselection=0)
    for index in range(len(typeAccount)):
        accountEntry.insert('end', typeAccount[index])
    accountEntry.place(relx=0.5, rely=0.5, relwidth=0.15, relheight=0.4)

    # list label
    listLabel = tk.Label(leftFrame, text="List")
    listLabel.place(relx=0.05, rely=0.2, relwidth=0.1, relheight=0.075)
    listEntry = tk.Entry(leftFrame, bg='#ff9aa2')
    listEntry.place(relx=0.15, rely=0.2, relwidth=0.15, relheight=0.075)

    # amount label
    amountLabel = tk.Label(leftFrame, text="Amount")
    amountLabel.place(relx=0.05, rely=0.35, relwidth=0.1, relheight=0.075)
    amountEntry = tk.Entry(leftFrame, bg='#ff9aa2')
    amountEntry.place(relx=0.15, rely=0.35, relwidth=0.15, relheight=0.075)

    # input button
    incomeButton = tk.Button(leftFrame, text='Income', command=lambda: updateIncomeData(dateEntry.get(), listEntry.get(), accountEntry.get(accountEntry.curselection()), amountEntry.get()))
    incomeButton.place(relx=0.55, rely=0.05, relwidth=0.15)

    #outcome button
    outcomeButton = tk.Button(leftFrame, text='Outcome', command=lambda: updateOutcomeData(output, dateEntry.get(), listEntry.get(), typeEntry.get(typeEntry.curselection()), amountEntry.get(), accountEntry.get(accountEntry.curselection())))
    outcomeButton.place(relx=0.55, rely= 0.2, relwidth=0.15)

