import pandas as pd
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter.ttk import *
from tkinter import messagebox

FILE_CSV = "C:\\Users\\Van Phu Hoa\\PycharmProjects\\money_tracker\\{}\\{}_{}.csv"
months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
month = {
    "01": "Jan",
    "02": "Feb",
    "03": "Mar",
    "04": "Apr",
    "05": "May",
    "06": "Jun",
    "07": "Jul",
    "08": "Aug",
    "09": "Sep",
    "10": "Oct",
    "11": "Nov",
    "12": "Dec",
}


def view_by_type(output, value_input):
    global database, month_name, FILE_CSV, month

    try:
        # find month_name from input
        if len(value_input) == 10:
            month_name = month[value_input[3:5]]
            type_data = 0
        else:
            month_name = month[value_input]
            type_data = 1

        # print data to output
        database = pd.read_csv(FILE_CSV.format("outcome", month_name, "outcome"))
        if type_data == 0:
            output.insert('end', database[database["Date"] == value_input].to_string())
        else:
            output.insert('end', database.to_string())
    except:
        messagebox.showerror('Error', "Something else went wrong")


def create_pie_chart(field, month_pie_chart, date_pie_chart, root_window, clear_chart_button):
    global database, month_name, month, FILE_CSV
    labels_pie = ["necessity", "education", "financial freedom", "savings", "play"]
    color_pie = ["#C7CEEA", "#FFDAC1", "white", "#FFFFD8", "#B5EAD7"]
    fig = plt.figure(figsize=(4, 4), dpi=100)
    type_data = [0]

    try:
        month_name = month[month_pie_chart]
        database = pd.read_csv(FILE_CSV.format("outcome", month_name, "outcome"))

        # create date base on date_pie_chart and month_pie_chart
        if len(field) > 0 and field[-1] == 0:
            date_input = date_pie_chart + "/" + month_pie_chart + "/2021"
        for i in range(5):
            if field[-1] == 0:
                type_data.append(
                    database[
                        (database["Type"] == labels_pie[i]) & (database["Date"] == date_input)
                    ]["Amount"].sum(axis=0)
                )
            else:
                type_data.append(
                    database[database["Type"] == labels_pie[i]]["Amount"].sum(axis=0)
                )

        plt.pie(type_data[1:6], labels=labels_pie, colors=color_pie, autopct="%.2f %%")
        canvas = FigureCanvasTkAgg(fig, master=root_window)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.6, rely=0.4)
        toolbar = NavigationToolbar2Tk(canvas, root_window)
        toolbar.update()
        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().place(relx=0.6, rely=0.4)
    except:
        messagebox.showerror('Error', 'Something else went wrong')
    clear_chart_button['command'] = lambda: canvas.get_tk_widget().delete('all')


def create_bar_chart(root_window, clear_chart_button):
    global month, FILE_CSV, months

    bar_data = np.zeros(shape=(2, 12))
    index = 0

    for file in range(12):
        outcome_file = pd.read_csv(FILE_CSV.format("outcome", months[file], "outcome"))
        income_file = pd.read_csv(FILE_CSV.format("income", months[file], "income"))
        income = income_file["Amount"].sum(axis=0)
        outcome = outcome_file["Amount"].sum(axis=0)
        bar_data[0, index] = income
        bar_data[1, index] = outcome
        index += 1
    bar_dataframe = pd.DataFrame(
        {"Income": bar_data[0, :], "Outcome": bar_data[1, :]}, index=months
    )

    # display bar chart
    fig = plt.figure(figsize=(12, 4), dpi=100)
    # bar_dataFrame.plot.bar()
    bar1 = np.arange(len(months))
    bar2 = [i for i in bar1]
    plt.bar(bar1, bar_dataframe["Income"], width=-0.4, align="edge")
    plt.bar(bar2, bar_dataframe["Outcome"], width=0.4, align="edge")
    plt.xticks(bar1, months)
    canvas = FigureCanvasTkAgg(fig, master=root_window)
    canvas.draw()
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().place(relx=0.1, rely=0.4)
    clear_chart_button['command'] = lambda: canvas.get_tk_widget().delete('all')


def create_right_frame(root_window, output):
    # right frame
    right_frame = tk.Frame(root_window, bg="white")
    right_frame.place(relx=0.32, rely=0.05, relwidth=0.25, relheight=0.3)

    # value input
    view_listbox = Combobox(right_frame)
    view_listbox["values"] = ("Date", "Month")
    view_listbox.place(relx=0.05, rely=0.05, relwidth=0.2, relheight=0.075)

    # input entry
    view_entry = tk.Entry(right_frame)
    view_entry.place(relx=0.3, rely=0.05, relwidth=0.2)

    # input view button
    view_button = tk.Button(
        right_frame, text="View", command=lambda: view_by_type(output, view_entry.get())
    )
    view_button.place(relx=0.55, rely=0.05, relwidth=0.2, relheight=0.075)

    # date label input for plot
    date_label = tk.Label(right_frame, text="Date")
    date_label.place(relx=0.05, rely=0.2, relwidth=0.2, relheight=0.075)

    # month label input for plot
    month_label = tk.Label(right_frame, text="Month")
    month_label.config(font=("Transformers Movie", 10))
    month_label.place(relx=0.3, rely=0.2, relwidth=0.2)

    # type List box input for plot
    type_box = Combobox(right_frame)
    type_box["values"] = ("Date", "Month")
    type_box.place(relx=0.55, rely=0.2, relwidth=0.2, relheight=0.075)

    # Date input for plot
    date_plot = tk.Entry(right_frame, bd=0)
    date_plot.place(relx=0.05, rely=0.3, relwidth=0.2, relheight=0.075)

    # Month input for plot
    month_plot = tk.Entry(right_frame)
    month_plot.place(relx=0.3, rely=0.3, relwidth=0.2)

    #clear plot button
    clear_chart_button = tk.Button(right_frame, text='Clear chart')
    clear_chart_button.place(relx=0.7, rely=0.7)

    # plot button
    pie_chart_button = tk.Button(
        right_frame, text="Pie Plot",
        command=lambda: create_pie_chart(
            type_box.get(), month_plot.get(), date_plot.get(), root_window,
            clear_chart_button
        ),

    )
    pie_chart_button.place(relx=0.55, rely=0.3, relwidth=0.2, relheight=0.075)

    # bar plot button
    bar_chart_button = tk.Button(
        right_frame, text="Bar chart", command=lambda: create_bar_chart(root_window, clear_chart_button)
    )
    bar_chart_button.place(relx=0.55, rely=0.4, relwidth=0.2, relheight=0.075)


