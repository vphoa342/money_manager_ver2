import pandas as pd
import tkinter as tk
import funds
from tkinter.ttk import *
from tkinter import messagebox

FILE_CSV = "C:\\Users\\Van Phu Hoa\\PycharmProjects\\money_tracker\\{}\\{}_{}.csv"
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
typeList = ("necessity", "education", "financial freedom", "savings", "play")
type_account = ("BIDV", "momo", "finhay", "wallet", "investment account")
fund_dict = {
    "BIDV": funds.BIDV,
    "momo": funds.momo,
    "finhay": funds.finhay,
    "wallet": funds.wallet,
    "investment account": funds.investment_account,
}
FILE_TXT = "C:\\Users\\Van Phu Hoa\\PycharmProjects\\money_tracker\\funds_database.txt"
FILE_MONTH_DATA = (
    "C:\\Users\\Van Phu Hoa\\PycharmProjects\\money_tracker\\month_data.csv"
)


def save_data():
    global FILE_TXT
    output_string = """wage: {}
BIDV: {}
momo: {}
finhay: {}
wallet: {}
investmentAccount: {}
    """
    try:
        file = open(FILE_TXT, mode="w+")
        file.writelines(
            output_string.format(
                "5000000",
                funds.BIDV.total,
                funds.momo.total,
                funds.finhay.total,
                funds.wallet.total,
                funds.investment_account.total,
            )
        )
    finally:
        file.close()


def update_outcome_data(output, date, list_data, type_data, amount, account):
    remind_string = """remain necessity: {}
    remain play: {}
    remain savings: {}
    remain education: {}
    remain financial freedom: {}
        """

    # get month from dd/mm/yyyy
    try:
        month_name = month[date[3:5]]

        # export to csv
        database = pd.read_csv(FILE_CSV.format("outcome", month_name, "outcome"))
        database = database.append(
            {"Date": date, "List": list_data, "Type": type_data, "Amount": int(amount)},
            ignore_index=True,
        )
        database.to_csv(FILE_CSV.format("outcome", month_name, "outcome"), index=False)

        # update to fund
        fund_dict[account].deduct_money(int(amount))
        save_data()

        # create 12 month objects
        month_data = pd.read_csv(FILE_MONTH_DATA)
        month_data.loc[int(date[3:5]) - 1][type_data] += int(amount)
        month_data.to_csv(FILE_MONTH_DATA, index=False)

        # remind goal
        necessity, play, savings, education, financial_freedom = month_data.loc[
            int(date[3:5]) - 1
            ]
        necessity1, play1, savings1, education1, financial_freedom1 = month_data.loc[12]
        output.insert(
            "end",
            remind_string.format(
                necessity1 - necessity,
                play1 - play,
                savings1 - savings,
                education1 - education,
                financial_freedom1 - financial_freedom,
            ),
        )
    except:
        messagebox.showerror('Error', "Something else went wrong")


def update_income_data(date, list_data, account, amount):
    global database, month_name, fund_dict

    try:
        month_name = month[date[3:5]]

        # export to csv
        database = pd.read_csv(FILE_CSV.format("income", month_name, "income"))
        database = database.append(
            {"Date": date, "List": list_data, "Type": account, "Amount": int(amount)},
            ignore_index=True,
        )
        database.to_csv(FILE_CSV.format("income", month_name, "income"), index=False)

        # update to fund
        fund_dict[account].add_money(int(amount))
        save_data()
    except:
        messagebox.showerror('Error', "Something else went wrong")


def create_left_frame(root_window, output):
    global month_name, type_list

    # left frame
    left_frame = tk.Frame(root_window, bg="white")
    left_frame.place(relx=0.05, rely=0.05, relwidth=0.25, relheight=0.3)

    # data label
    date_label = tk.Label(left_frame, text="Date", font=('', 15))
    date_label.grid(padx=1, pady=1)
    date_entry = tk.Entry(left_frame, bg="white")
    date_entry.grid(row=1, column=0)

    # type label
    type_label = tk.Label(left_frame, text="Type")
    type_label.place(relx=0.05, rely=0.5, relwidth=0.1, relheight=0.1)
    type_entry = Combobox(left_frame, exportselection=0)
    type_entry["values"] = typeList
    type_entry.place(relx=0.15, rely=0.5, relwidth=0.15, relheight=0.1)

    # type account
    account_label = tk.Label(left_frame, text="Account")
    account_label.place(relx=0.4, rely=0.5, relwidth=0.1, relheight=0.1)
    account_entry = Combobox(left_frame)
    # exportselection=0)
    account_entry["values"] = type_account
    account_entry.place(relx=0.5, rely=0.5, relwidth=0.15, relheight=0.1)

    # list label
    list_label = tk.Label(left_frame, text="List")
    list_label.place(relx=0.05, rely=0.2, relwidth=0.1, relheight=0.075)
    list_entry = tk.Entry(left_frame, bg="white")
    list_entry.place(relx=0.15, rely=0.2, relwidth=0.15, relheight=0.075)

    # amount label
    amount_label = tk.Label(left_frame, text="Amount")
    amount_label.place(relx=0.05, rely=0.35, relwidth=0.1, relheight=0.075)
    amount_entry = tk.Entry(left_frame, bg="white")
    amount_entry.place(relx=0.15, rely=0.35, relwidth=0.15, relheight=0.075)

    # input button
    income_button = tk.Button(
        left_frame,
        text="Income",
        command=lambda: update_income_data(
            date_entry.get(), list_entry.get(), account_entry.get(), amount_entry.get()
        ),
    )
    income_button.place(relx=0.55, rely=0.05, relwidth=0.15)

    # outcome button
    outcome_button = tk.Button(
        left_frame,
        text="Outcome",
        command=lambda: update_outcome_data(
            output,
            date_entry.get(),
            list_entry.get(),
            type_entry.get(),
            amount_entry.get(),
            account_entry.get(),
        ),
    )
    outcome_button.place(relx=0.55, rely=0.2, relwidth=0.15)
