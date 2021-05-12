import pandas as pd
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import leftFrame as lf
import rightFrame as rf

def createLowerFrame(mainWindow):
    global output
    # lower frame
    lowerFrame = tk.Frame(mainWindow, bg='#aff8d8')
    lowerFrame.place(relx=0.05, rely=0.4, relwidth=0.9, relheight=0.5)
    output = tk.Label(lowerFrame)
    output.place(relx=0, rely=0)
    return output