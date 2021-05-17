import pandas as pd
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
import collections

FILE_CSV = "C:\\Users\\Van Phu Hoa\\PycharmProjects\\money_tracker\\{}\\{}_{}.csv"
month = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec",
}


def get_month_name(input_data):
    # find month_name from input
    month = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec",
    }
    try:
        if len(input_data) < 3:
            month_name = month[int(input_data)]
        else:
            input_data = clear_not_need_zeros(input_data)
            first_slash = input_data.find('/')
            second_slash = input_data[first_slash + 1:].find('/') + first_slash + 1
            month_name = month[int(input_data[first_slash + 1: second_slash])]
        return month_name
    except KeyError:
        messagebox.showerror('Error', 'Invalid data')


def clear_not_need_zeros(date):
    year = date[date.rfind('/') + 1:]
    date = date[:-4]
    temp_string = '0{}'
    for i in range(1, 9):
        date = date.replace(temp_string.format(i), str(i))
    return date + year


def view_by_type(output, input_data):
    global database, month_name, FILE_CSV

    try:
        # clear current output
        output.delete('1.0', 'end')
        month_name = get_month_name(input_data)
        # print data to output
        database = pd.read_csv(FILE_CSV.format("outcome", month_name, "outcome"))
        if len(input_data) > 2:
            output.insert('end', database[database["Date"] == input_data].to_string())
        else:
            output.insert('end', database.to_string())
    except (IOError, OSError, KeyError, ValueError):
        messagebox.showerror('Error', "Something else went wrong")


def create_pie_chart(input_data, clear_chart_button):
    global database, month_name, month, FILE_CSV
    labels_pie = ["necessity", "education", "financial freedom", "savings", "play"]
    color_pie = ["#C7CEEA", "#FFDAC1", "#C1E7E3", "#FFFFD8", "#B5EAD7"]
    fig = plt.figure(figsize=(8, 4), dpi=100)
    type_data = [0]

    try:
        # get month as string from input data
        month_name = get_month_name(input_data)

        database = pd.read_csv(FILE_CSV.format("outcome", month_name, "outcome"))
        for i in range(5):
            if len(input_data) > 3:
                type_data.append(
                    database[
                        (database["Type"] == labels_pie[i]) & (database["Date"] == input_data)
                    ]["Amount"].sum(axis=0)
                )
            else:
                type_data.append(
                    database[database["Type"] == labels_pie[i]]["Amount"].sum(axis=0)
                )

        plt.pie(type_data[1:6], labels=labels_pie, colors=color_pie, autopct="%.2f %%")

        chart_window = tk.Tk()
        chart_window.title('Chart View')
        chart_window.geometry('800x400')
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()

        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().grid(row=0, column=0)
        clear_chart_button['command'] = lambda: canvas.get_tk_widget().delete('all')
    except (IOError, ValueError, OSError):
        messagebox.showerror('Error', 'Something else went wrong')


def edit_list(array):
    # dd/mm/yyyy to dd, sort

    # dd/mm/yyyy to dd
    for i in range(len(array)):
        date = array[i]
        array[i] = int(date[:date.find('/')])

    # sort
    array.sort()
    return array


def edit_dict(date, amount):
    # create dict
    dict_temp = {}

    # add value for dict
    for i in range(len(date)):
        temp = date[i]
        if dict_temp.get(temp) is None:
            dict_temp[temp] = amount[i]
        else:
            dict_temp[temp] += amount[i]

    # add zeros amount date
    for date in range(1, 32):
        if dict_temp.get(date) is None:
            dict_temp[date] = 0
    return dict_temp


def create_bar_chart(clear_chart_button, input_data):
    global month, FILE_CSV

    bar_data = np.zeros(shape=(2, 12))

    # display bar chart
    fig = plt.figure(figsize=(12, 4), dpi=100)
    if len(input_data) <= 2:
        index = 0
        # create bar chart to compare 12 months
        for file in range(1, 13):
            # open file
            try:
                outcome_file = pd.read_csv(FILE_CSV.format("outcome", month[file], "outcome"))
                income_file = pd.read_csv(FILE_CSV.format("income", month[file], "income"))

                # calculate total base on amount
                income = income_file["Amount"].sum(axis=0)
                outcome = outcome_file["Amount"].sum(axis=0)
                bar_data[0, index] = income
                bar_data[1, index] = outcome
                index += 1
            except (IOError, OSError):
                messagebox.showerror('Error', "File not found")

        bar_dataframe = pd.DataFrame(
            {"Income": bar_data[0, :], "Outcome": bar_data[1, :]}, index=month.values()
        )
        bar1 = np.arange(len(month))
        bar2 = [i for i in bar1]
        plt.bar(bar1, bar_dataframe["Income"], width=-0.4, align="edge")
        plt.bar(bar2, bar_dataframe["Outcome"], width=0.4, align="edge")
        plt.xticks(bar1, month.values())
    else:
        try:
            month_name = get_month_name(input_data)
            outcome_file = pd.read_csv(FILE_CSV.format("outcome", month_name, "outcome"))
            income_file = pd.read_csv(FILE_CSV.format("income", month_name, "income"))

            # set up for outcome file
            outcome_date_list = list(outcome_file['Date'])
            outcome_date_list = edit_list(outcome_date_list)
            outcome_amount_list = list(outcome_file['Amount'])
            outcome_dict = edit_dict(outcome_date_list, outcome_amount_list)
            outcome_dict_ordered = collections.OrderedDict(sorted(outcome_dict.items()))

            # set up for income file
            income_date_list = list(income_file['Date'])
            income_date_list = edit_list(income_date_list)
            income_amount_list = list(income_file['Amount'])
            income_dict = edit_dict(income_date_list, income_amount_list)
            income_dict_ordered = collections.OrderedDict(sorted(income_dict.items()))

            # display chart
            x = np.arange(1, 32)
            width = 0.4
            plt.bar(x - 0.2, outcome_dict_ordered.values(), width)
            plt.bar(x + 0.2, income_dict_ordered.values(), width)
            plt.xticks(x, [str(x) for x in outcome_dict_ordered.keys()])

        except (IOError, OSError):
            messagebox.showerror('Error', "File not found")

    # bar_dataFrame.plot.bar()
    chart_window = tk.Tk()
    chart_window.title('Chart View')
    chart_window.geometry('1200x400')
    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()

    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().place(relx=0, rely=0)
    clear_chart_button['command'] = lambda: canvas.get_tk_widget().delete('all')


def create_right_frame(root_window, output):
    # right frame
    right_frame = tk.Frame(root_window, bg="white")
    right_frame.place(relx=0.32, rely=0.05, relwidth=0.25, relheight=0.3)

    # input label
    input_label = tk.Label(right_frame, text='Input', font=('Transformers Movie', 10, 'bold'), bg='white')
    input_label.grid(row=0, column=0, padx=4, pady=2, sticky='news')

    # input entry
    view_entry = tk.Entry(right_frame, font=('Transformers Movie', 10, 'bold'))
    view_entry.grid(row=0, column=1, padx=4, pady=2, sticky='news')

    # input view button
    view_button = tk.Button(
        right_frame, text="View", command=lambda: view_by_type(output, view_entry.get()),
        font=('Transformers Movie', 10, 'bold')
    )
    view_button.grid(row=0, column=2, padx=4, pady=2, sticky='news')

    # date label input for plot
    chart_data_label = tk.Label(right_frame, text="Chart data", font=('Transformers Movie', 10, 'bold'), bg='white')
    chart_data_label.grid(row=1, column=0, padx=4, pady=2, sticky='news')

    # Date input for plot
    chart_data_entry = tk.Entry(right_frame, bd=1, font=('Transformers Movie', 10, 'bold'))
    chart_data_entry.grid(row=1, column=1, padx=4, pady=2, sticky='news', columnspan=2)

    # clear plot button
    clear_chart_button = tk.Button(right_frame, text='Clear chart', font=('Transformers Movie', 10, 'bold'))
    clear_chart_button.grid(row=2, column=2, padx=4, pady=2, sticky='news')

    # plot button
    pie_chart_button = tk.Button(
        right_frame, text="Pie Chart",
        command=lambda: create_pie_chart(chart_data_entry.get(), clear_chart_button),
        font=('Transformers Movie', 10, 'bold')
    )
    pie_chart_button.grid(row=2, column=0, padx=4, pady=2, sticky='news')

    # bar plot button
    bar_chart_button = tk.Button(
        right_frame, text="Bar chart",
        command=lambda: create_bar_chart(clear_chart_button, chart_data_entry.get()),
        font=('Transformers Movie', 10, 'bold')
    )
    bar_chart_button.grid(row=2, column=1, padx=4, pady=2, sticky='news')
