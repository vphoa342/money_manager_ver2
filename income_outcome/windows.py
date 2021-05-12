import pandas as pd
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import funds
import leftFrame as lf
import rightFrame as rf
import lowerFrame as lowf


image = 'C:\\Users\\Van Phu Hoa\\PycharmProjects\\venv\\0c4fad724c81bcdfe590.png'
month = {"01": 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Aug', '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}
database = sheetName = None


def createWindow():
    global mainWindow, image, database, sheetName

    mainWindow = tk.Tk()
    mainWindow.title('Income & Outcome')

    backgroundImage = tk.PhotoImage(file=image)
    backgroundLabel = tk.Label(mainWindow, image=backgroundImage)
    backgroundLabel.place(relx=0, rely=0, relheight=1, relwidth=1)

    output = lowf.createLowerFrame(mainWindow)
    rf.createRightFrame(mainWindow, output)
    lf.createLeftFrame(mainWindow, output)

    mainWindow.mainloop()


