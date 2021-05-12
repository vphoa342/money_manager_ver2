import pandas as pd
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import funds

fileCSV = 'C:\\Users\\Van Phu Hoa\\PycharmProjects\\income_outcome\\{}\\{}_{}.csv'
monthList = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
month = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Aug', '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}


def viewBy(output, inputValue):
    global database, sheetName, fileCSV, month

    #find sheetname from input
    if len(inputValue) == 10:
        sheetName = month[inputValue[3:5]]
        type = 0
    else:
        sheetName = month[inputValue]
        type = 1

    #print data to output
    database = pd.read_csv(fileCSV.format('outcome', sheetName, 'outcome'))
    if type == 0: output['text'] = database[database['Date'] == inputValue].to_string()
    else: output['text'] = database.to_string()

def exportExcel(output, sheetName):
    global database, fileCSV
    workbook = load_workbook(fileCSV)
    workbook.remove(workbook[sheetName])
    workbook.save(fileCSV)
    with pd.ExcelWriter(fileCSV, mode='a') as writer:
        database.to_excel(writer, sheet_name=sheetName)
    output["text"] = database.to_string()
    writer.save()

def piePlot(field, monthPieplot, datePieplot, mainWindow):
    global database, sheetName, month, fileCSV
    labelsPie = ['necessity', 'education', 'financial freedom', 'savings', 'play']
    colorPie = ['#C7CEEA', '#FFDAC1', '#FF9AA2', '#FFFFD8', '#B5EAD7']
    fig = plt.figure(figsize=(4, 4), dpi=100)
    sheetName = month[monthPieplot]
    database = pd.read_csv(fileCSV.format('outcome', sheetName, 'outcome'))
    type = [0]

    #create date base on datePieplot and monthPieplot
    if len(field) > 0 and field[-1] == 0:
        inputDate = datePieplot + '/' + monthPieplot + '/2021'
    for i in range(5):
        if field[-1] == 0:
            type.append(database[(database['Type'] == labelsPie[i]) & (database['Date'] == inputDate)]['Amount'].sum(axis=0))
        else:
            type.append(database[database['Type'] == labelsPie[i]]['Amount'].sum(axis=0))

    plt.pie(type[1:6], labels=labelsPie, colors=colorPie, autopct='%.2f %%')
    canvas = FigureCanvasTkAgg(fig, master=mainWindow)
    canvas.draw()
    canvas.get_tk_widget().place(relx=0.6, rely=0.4)
    toolbar = NavigationToolbar2Tk(canvas, mainWindow)
    toolbar.update()
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().place(relx=0.6, rely=0.4)

def barChart(mainWindow):
    global month, fileCSV, monthList

    barData = np.zeros(shape=(2, 12))
    index = 0

    for file in range(12):
        outcomeFile = pd.read_csv(fileCSV.format('outcome', monthList[file], 'outcome'))
        incomeFile = pd.read_csv(fileCSV.format('income', monthList[file], 'income'))
        income = incomeFile['Amount'].sum(axis=0)
        outcome = outcomeFile['Amount'].sum(axis=0)
        barData[0, index] = income
        barData[1, index] = outcome
        index += 1
    barDataFrame = pd.DataFrame({'Income': barData[0, : ], 'Outcome': barData[1, : ]}, index=monthList)

    #display bar chart
    fig = plt.figure(figsize=(12, 4), dpi=100)
    #barDataFrame.plot.bar()
    bar1 = np.arange(len(monthList))
    bar2 = [i for i in bar1]
    plt.bar(bar1, barDataFrame['Income'], width=-0.4, align='edge')
    plt.bar(bar2, barDataFrame['Outcome'], width = 0.4, align='edge')
    plt.xticks(bar1, monthList)
    canvas = FigureCanvasTkAgg(fig, master=mainWindow)
    canvas.draw()
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().place(relx=0.1, rely=0.4)


def createRightFrame(mainWindow, output):
    # right frame
    rightFrame = tk.Frame(mainWindow, bg='#aff8d8')
    rightFrame.place(relx=0.55, rely=0.05, relwidth=0.4, relheight=0.3)

    #export button
    exportButton = tk.Button(rightFrame, text='Export excel', command=lambda: exportExcel(output, sheetName))
    exportButton.place(relx=0.85, rely=0.05, relwidth=0.125, relheight=0.075)

    # value input
    scrollbar = tk.Scrollbar(orient="vertical")
    viewListbox = tk.Listbox(rightFrame, yscrollcommand=scrollbar.set)
    viewListbox.insert('end', "Date")
    viewListbox.insert('end', "Month")
    viewListbox.place(relx=0.05, rely=0.05, relwidth=0.2, relheight=0.075)

    # input entry
    viewEntry = tk.Entry(rightFrame)
    viewEntry.place(relx=0.3, rely=0.05, relwidth=0.2)

    # input view button
    viewButton = tk.Button(rightFrame, text='View', command=lambda: viewBy(output, viewEntry.get()))
    viewButton.place(relx=0.55, rely=0.05, relwidth=0.2, relheight=0.075)

    #date label input for plot
    dateLabel = tk.Label(rightFrame, text='Date')
    dateLabel.place(relx=0.05, rely=0.2, relwidth=0.2, relheight=0.075)

    #month label input for plot
    monthLabel = tk.Label(rightFrame, text='Month')
    monthLabel.place(relx=0.3, rely=0.2, relwidth=0.2)

    #type List box input for plot
    typeLisbox = tk.Listbox(rightFrame, yscrollcommand=scrollbar.set)
    typeLisbox.insert(1, 'Date')
    typeLisbox.insert(2, 'Month')
    typeLisbox.place(relx=0.55, rely=0.2, relwidth=0.2, relheight=0.075)

    #Date input for plot
    datePlot = tk.Entry(rightFrame)
    datePlot.place(relx=0.05, rely=0.3, relwidth=0.2, relheight=0.075)


    #Month input for plot
    monthPLot = tk.Entry(rightFrame)
    monthPLot.place(relx=0.3, rely=0.3, relwidth=0.2)

    # plot button
    piePlotButton = tk.Button(rightFrame, command=lambda: piePlot(typeLisbox.curselection(), monthPLot.get(), datePlot.get(), mainWindow), text='Pie Plot')
    piePlotButton.place(relx=0.55, rely=0.3, relwidth=0.2, relheight=0.075)

    #bar plot button
    barPlotButton = tk.Button(rightFrame, text='Bar chart', command=lambda: barChart(mainWindow))
    barPlotButton.place(relx=0.55, rely=0.4, relwidth=0.2, relheight=0.075)

