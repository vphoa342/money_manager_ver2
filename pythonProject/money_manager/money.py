import sys
import numpy as np
import pyqtgraph as pg
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import collections
import random

ROOT_PATH = "C:\\Users\\Van Phu Hoa\\PycharmProjects\\pythonProject\\money_manager\\"
FILE_CSV = ROOT_PATH + "{}\\{}_{}.csv"
FILE_TXT = ROOT_PATH + "funds_database.txt"
FILE_MONTH_DATA = ROOT_PATH + "month_data.csv"
MONTH = {
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


class Account:
    def __init__(self, total):
        self.total = total

    def add_money(self, amount):
        self.total += amount

    def deduct_money(self, amount):
        self.total -= amount

    def update_money(self, new_value):
        self.total = new_value

    def transfer_money(self, other, value):
        self.total -= value
        other.total += value


def save_data():
    output_string = (
        """BIDV: {}\nmomo: {}\nfinhay: {}\nwallet: {}\ninvestment_account: {}"""
    )
    try:
        file = open(FILE_TXT, mode="w+")
        file.writelines(
            output_string.format(
                BIDV.total,
                momo.total,
                finhay.total,
                wallet.total,
                investment_account.total,
            )
        )
        file.close()
    except (IOError, OSError):
        pass


def create_object():
    try:
        file = open(FILE_TXT, mode="r")

        # read bidv, momo, finhay, wallet
        line_as_string = file.readline().split()
        cur_BIDV = int(line_as_string[1])

        line_as_string = file.readline().split()
        cur_momo = int(line_as_string[1])

        line_as_string = file.readline().split()
        cur_finhay = int(line_as_string[1])

        line_as_string = file.readline().split()
        cur_wallet = int(line_as_string[1])

        line_as_string = file.readline().split()
        cur_investment_account = int(line_as_string[1])
        file.close()
        return tuple(
            (cur_BIDV, cur_momo, cur_finhay, cur_wallet, cur_investment_account)
        )
    except IOError:
        return tuple((0, 0, 0, 0, 0))


def print_data(table, remain_table, percent_table, account_table, date):
    month_name = MONTH[int(date[3:5])]
    try:
        # open and write to csv
        database1 = pd.read_csv(FILE_CSV.format("income", month_name, "income"))
        database2 = pd.read_csv(FILE_CSV.format("outcome", month_name, "outcome"))
        database = pd.concat([database1, database2])

        # reset table
        table.setRowCount(0)
        table.setRowCount(100)
        for index, row in database.iterrows():
            table.setItem(index, 0, QtWidgets.QTableWidgetItem(str(row["Date"])))
            table.setItem(index, 1, QtWidgets.QTableWidgetItem(str(row["List"])))
            table.setItem(index, 2, QtWidgets.QTableWidgetItem(str(row["Type"])))
            table.setItem(index, 3, QtWidgets.QTableWidgetItem(str(row["Amount"])))
    except (IOError, OSError):
        pass

    remain_database = pd.read_csv(FILE_MONTH_DATA)

    # print first line of 2 table
    # remain table
    (
        cur_necessity,
        cur_play,
        cur_savings,
        cur_education,
        cur_financial_freedom,
    ) = remain_database.iloc[int(date[3:5])]

    remain_table.setItem(
        0, 0, QtWidgets.QTableWidgetItem(str(NECESSITY - cur_necessity))
    )
    remain_table.setItem(0, 1, QtWidgets.QTableWidgetItem(str(PLAY - cur_play)))
    remain_table.setItem(0, 2, QtWidgets.QTableWidgetItem(str(SAVINGS - cur_savings)))
    remain_table.setItem(
        0, 3, QtWidgets.QTableWidgetItem(str(EDUCATION - cur_education))
    )
    remain_table.setItem(
        0, 4, QtWidgets.QTableWidgetItem(str(FINANCIAL_FREEDOM - cur_financial_freedom))
    )

    # percentage table
    percent_table.setItem(0, 0, QtWidgets.QTableWidgetItem(str(100)))
    percent_table.setItem(0, 1, QtWidgets.QTableWidgetItem(str(100)))
    percent_table.setItem(0, 2, QtWidgets.QTableWidgetItem(str(100)))
    percent_table.setItem(0, 3, QtWidgets.QTableWidgetItem(str(100)))
    percent_table.setItem(0, 4, QtWidgets.QTableWidgetItem(str(100)))

    for index, row in remain_database.iterrows():
        # remain table
        remain_table.setItem(
            index + 1, 0, QtWidgets.QTableWidgetItem(str(row["necessity"]))
        )
        remain_table.setItem(index + 1, 1, QtWidgets.QTableWidgetItem(str(row["play"])))
        remain_table.setItem(
            index + 1, 2, QtWidgets.QTableWidgetItem(str(row["savings"]))
        )
        remain_table.setItem(
            index + 1, 3, QtWidgets.QTableWidgetItem(str(row["education"]))
        )
        remain_table.setItem(
            index + 1, 4, QtWidgets.QTableWidgetItem(str(row["financial freedom"]))
        )

        # percentage table
        percent_table.setItem(
            index + 1,
            0,
            QtWidgets.QTableWidgetItem(str(row["necessity"] / NECESSITY * 100)),
        )
        percent_table.setItem(
            index + 1, 1, QtWidgets.QTableWidgetItem(str(row["play"] / PLAY * 100))
        )
        percent_table.setItem(
            index + 1,
            2,
            QtWidgets.QTableWidgetItem(str(row["savings"] / SAVINGS * 100)),
        )
        percent_table.setItem(
            index + 1,
            3,
            QtWidgets.QTableWidgetItem(str(row["education"] / EDUCATION * 100)),
        )
        percent_table.setItem(
            index + 1,
            4,
            QtWidgets.QTableWidgetItem(
                str(row["financial freedom"] / FINANCIAL_FREEDOM * 100)
            ),
        )

    # account table
    AMOUNT = (
        BIDV.total + momo.total + finhay.total + wallet.total + investment_account.total
    )
    account_table.setItem(0, 0, QtWidgets.QTableWidgetItem(str(AMOUNT)))
    account_table.setItem(0, 1, QtWidgets.QTableWidgetItem(str(100)))
    account_table.setItem(1, 0, QtWidgets.QTableWidgetItem(str(BIDV.total)))
    account_table.setItem(
        1, 1, QtWidgets.QTableWidgetItem(str(BIDV.total / AMOUNT * 100))
    )
    account_table.setItem(2, 0, QtWidgets.QTableWidgetItem(str(momo.total)))
    account_table.setItem(
        2, 1, QtWidgets.QTableWidgetItem(str(momo.total / AMOUNT * 100))
    )
    account_table.setItem(3, 0, QtWidgets.QTableWidgetItem(str(finhay.total)))
    account_table.setItem(
        3, 1, QtWidgets.QTableWidgetItem(str(finhay.total / AMOUNT * 100))
    )
    account_table.setItem(4, 0, QtWidgets.QTableWidgetItem(str(wallet.total)))
    account_table.setItem(
        4, 1, QtWidgets.QTableWidgetItem(str(wallet.total / AMOUNT * 100))
    )
    account_table.setItem(
        5, 0, QtWidgets.QTableWidgetItem(str(investment_account.total))
    )
    account_table.setItem(
        5, 1, QtWidgets.QTableWidgetItem(str(investment_account.total / AMOUNT * 100))
    )


def update_data(
    table,
    remain_table,
    percent_table,
    account_table,
    date,
    list_data,
    type_data,
    account,
    amount,
    income_check,
    outcome_check,
):
    month_name = MONTH[int(date[3:5])]
    try:
        # open and write to csv
        if income_check:
            database = pd.read_csv(FILE_CSV.format("income", month_name, "income"))
        else:
            database = pd.read_csv(FILE_CSV.format("outcome", month_name, "outcome"))

        database = database.append(
            {"Date": date, "List": list_data, "Type": type_data, "Amount": int(amount)},
            ignore_index=True,
        )

        # export to csv
        database.to_csv(FILE_CSV.format("income", month_name, "income"), index=False)

        # update to fund
        if income_check:
            FUND_DICT[account].add_money(int(amount))
        elif outcome_check:
            FUND_DICT[account].deduct_money(int(amount))

        # save to month_data.csv
        if outcome_check:
            remain_database = pd.read_csv(FILE_MONTH_DATA)
            remain_database.iloc[int(date[3:5])-1][type_data] += int(amount)
            remain_database.to_csv(FILE_MONTH_DATA, index=False)

        # save data to funds_database.txt
        save_data()
    except (ValueError, IOError, OSError):
        pass

    # print data to date table
    print_data(table, remain_table, percent_table, account_table, date)


def view_function(table, remain_table, percent_table, account_table, date, date_check):
    print_data(table, remain_table, percent_table, account_table, date)

    # if date check, rewrite the table follow day input
    if date_check:
        month_name = MONTH[int(date[3:5])]
        try:
            # open and write to csv
            database1 = pd.read_csv(FILE_CSV.format("income", month_name, "income"))
            database2 = pd.read_csv(FILE_CSV.format("outcome", month_name, "outcome"))
            database = pd.concat([database1, database2])
            database = database.loc[database["Date"] == date].drop_duplicates()
            table.setRowCount(0)
            table.setRowCount(100)
            for index, row in database.iterrows():
                table.setItem(index, 0, QtWidgets.QTableWidgetItem(str(row["Date"])))
                table.setItem(index, 1, QtWidgets.QTableWidgetItem(str(row["List"])))
                table.setItem(index, 2, QtWidgets.QTableWidgetItem(str(row["Type"])))
                table.setItem(index, 3, QtWidgets.QTableWidgetItem(str(row["Amount"])))
        except (IOError, OSError):
            pass


def create_pie_chart(date, graphics_view):

    try:
        colours = []
        for count in range(5):
            number = []
            for _ in range(3):
                number.append(random.randrange(0, 255))
            colours.append(Qt.QColor(number[0], number[1], number[2]))
        month_database = pd.read_csv(FILE_MONTH_DATA)
        type_data = list(month_database.iloc[int(date[3:5])-1])
        scene = pg.PlotWidget(graphics_view, background='w')
        set_angle = count1 = 0
        print(type_data)
        total = sum(type_data)
        for temp in type_data:
            # Max span is 5760, so we have to calculate corresponding span angle
            angle = round(float(temp * 5760) / total)
            ellipse = QtWidgets.QGraphicsEllipseItem(0, 0, 400, 400)
            ellipse.setPos(0, 0)
            ellipse.setStartAngle(set_angle)
            ellipse.setSpanAngle(angle)
            ellipse.setBrush(colours[count1])
            set_angle += angle
            count1 += 1
            scene.addItem(ellipse)
            scene.scale(0.05, 0.05)
    except (IOError, ValueError, OSError):
        pass


def edit_list(array):
    # dd/mm/yyyy to dd, sort

    # dd/mm/yyyy to dd
    for i in range(len(array)):
        date = array[i]
        array[i] = int(date[: date.find("/")])

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


def create_bar_chart(graphics_view, month_check, date):
    global bar_plot, bar_graph_1, bar_graph_2

    if bar_plot is not None:
        bar_plot.removeItem(bar_graph_1)
        bar_plot.removeItem(bar_graph_2)

    bar_data = np.zeros(shape=(2, 12))

    # display bar chart
    if month_check:
        index = 0
        # create bar chart to compare 12 months
        for file in range(1, 13):
            # open file
            try:
                outcome_file = pd.read_csv(
                    FILE_CSV.format("outcome", MONTH[file], "outcome")
                )
                income_file = pd.read_csv(
                    FILE_CSV.format("income", MONTH[file], "income")
                )

                # calculate total base on amount
                income = income_file["Amount"].sum(axis=0)
                outcome = outcome_file["Amount"].sum(axis=0)
                bar_data[0, index] = income
                bar_data[1, index] = outcome
                index += 1
            except (IOError, OSError):
                pass

        bar_dataframe = pd.DataFrame(
            {"Income": bar_data[0, :], "Outcome": bar_data[1, :]}, index=MONTH.values()
        )
        bar1 = np.arange(12)
        bar_graph_1 = pg.BarGraphItem(
            x=bar1 - 0.15, height=bar_dataframe["Income"], width=0.3, brush="g"
        )
        bar_graph_2 = pg.BarGraphItem(
            x=bar1 + 0.15, height=bar_dataframe["Outcome"], width=0.3, brush="r"
        )
        bar_plot = pg.PlotWidget(graphics_view, background="w")
        bar_plot.addItem(bar_graph_1)
        bar_plot.addItem(bar_graph_2)
        bar_plot.scale(0.05, 0.05)

    else:
        try:
            month_name = MONTH[int(date[3:5])]
            outcome_file = pd.read_csv(
                FILE_CSV.format("outcome", month_name, "outcome")
            )
            income_file = pd.read_csv(FILE_CSV.format("income", month_name, "income"))

            # set up for outcome file
            outcome_date_list = list(outcome_file["Date"])
            outcome_date_list = edit_list(outcome_date_list)
            outcome_amount_list = list(outcome_file["Amount"])
            outcome_dict = edit_dict(outcome_date_list, outcome_amount_list)
            outcome_dict_ordered = collections.OrderedDict(sorted(outcome_dict.items()))

            # set up for income file
            income_date_list = list(income_file["Date"])
            income_date_list = edit_list(income_date_list)
            income_amount_list = list(income_file["Amount"])
            income_dict = edit_dict(income_date_list, income_amount_list)
            income_dict_ordered = collections.OrderedDict(sorted(income_dict.items()))

            bar1 = np.arange(1, 32)
            bar_graph_1 = pg.BarGraphItem(
                x=bar1 - 0.15,
                height=list(income_dict_ordered.values()),
                width=0.3,
                brush="g",
            )
            bar_graph_2 = pg.BarGraphItem(
                x=bar1 + 0.15,
                height=list(outcome_dict_ordered.values()),
                width=0.3,
                brush="r",
            )
            bar_plot = pg.PlotWidget(graphics_view, background="w")
            bar_plot.addItem(bar_graph_1)
            bar_plot.addItem(bar_graph_2)
            bar_plot.scale(0.05, 0.065)

        except (IOError, OSError):
            pass


class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(1115, 923)
        main_window.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        # left frame
        self.input_group_box = QtWidgets.QGroupBox(self.central_widget)
        self.input_group_box.setGeometry(QtCore.QRect(10, 10, 391, 351))
        self.input_group_box.setMinimumSize(QtCore.QSize(391, 0))
        self.input_group_box.setMaximumSize(QtCore.QSize(391, 361))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.input_group_box.setFont(font)
        self.input_group_box.setCheckable(False)
        self.input_group_box.setObjectName("input_group_box")
        self.date_input = QtWidgets.QDateEdit(self.input_group_box)
        self.date_input.setGeometry(QtCore.QRect(100, 40, 181, 22))
        self.date_input.setMinimumDate(QtCore.QDate(1752, 10, 14))
        self.date_input.setCalendarPopup(False)
        self.date_input.setDate(QtCore.QDate(2021, 5, 23))
        self.date_input.setObjectName("date_input")
        self.date_label = QtWidgets.QLabel(self.input_group_box)
        self.date_label.setGeometry(QtCore.QRect(20, 40, 51, 21))
        self.date_label.setObjectName("date_label")
        self.list_entry = QtWidgets.QLineEdit(self.input_group_box)
        self.list_entry.setGeometry(QtCore.QRect(100, 80, 181, 22))
        self.list_entry.setMouseTracking(False)
        self.list_entry.setText("")
        self.list_entry.setClearButtonEnabled(True)
        self.list_entry.setObjectName("list_entry")
        self.list_table = QtWidgets.QLabel(self.input_group_box)
        self.list_table.setGeometry(QtCore.QRect(20, 80, 51, 21))
        self.list_table.setObjectName("list_table")
        self.type_label = QtWidgets.QLabel(self.input_group_box)
        self.type_label.setGeometry(QtCore.QRect(20, 120, 51, 21))
        self.type_label.setObjectName("type_label")
        self.type_combo_box = QtWidgets.QComboBox(self.input_group_box)
        self.type_combo_box.setGeometry(QtCore.QRect(100, 120, 181, 22))
        self.type_combo_box.setObjectName("type_combo_box")
        self.type_combo_box.addItem("")
        self.type_combo_box.addItem("")
        self.type_combo_box.addItem("")
        self.type_combo_box.addItem("")
        self.type_combo_box.addItem("")
        self.account_label = QtWidgets.QLabel(self.input_group_box)
        self.account_label.setGeometry(QtCore.QRect(20, 160, 71, 21))
        self.account_label.setObjectName("account_label")
        self.account_combo_box = QtWidgets.QComboBox(self.input_group_box)
        self.account_combo_box.setGeometry(QtCore.QRect(100, 160, 181, 22))
        self.account_combo_box.setObjectName("account_combo_box")
        self.account_combo_box.addItem("")
        self.account_combo_box.addItem("")
        self.account_combo_box.addItem("")
        self.account_combo_box.addItem("")
        self.account_combo_box.addItem("")
        self.amount_label = QtWidgets.QLabel(self.input_group_box)
        self.amount_label.setGeometry(QtCore.QRect(20, 200, 71, 21))
        self.amount_label.setObjectName("amount_label")
        self.amount_entry = QtWidgets.QLineEdit(self.input_group_box)
        self.amount_entry.setGeometry(QtCore.QRect(100, 200, 181, 22))
        self.amount_entry.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.amount_entry.setText("")
        self.amount_entry.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.amount_entry.setClearButtonEnabled(True)
        self.amount_entry.setObjectName("amount_entry")
        self.income_check_box = QtWidgets.QCheckBox(self.input_group_box)
        self.income_check_box.setGeometry(QtCore.QRect(20, 250, 81, 20))
        self.income_check_box.setObjectName("income_check_box")
        self.outcome_check_box = QtWidgets.QCheckBox(self.input_group_box)
        self.outcome_check_box.setGeometry(QtCore.QRect(190, 250, 91, 20))
        self.outcome_check_box.setObjectName("outcome_check_box")
        self.ok_button = QtWidgets.QPushButton(
            self.input_group_box,
            clicked=lambda: update_data(
                self.date_table_widget,
                self.type_table_widget,
                self.percent_table,
                self.account_table_widget,
                self.date_input.date().toPyDate().strftime("%d/%m/%Y"),
                self.list_entry.text(),
                self.type_combo_box.currentText(),
                self.account_combo_box.currentText(),
                self.amount_entry.text(),
                self.income_check_box.isChecked(),
                self.outcome_check_box.isChecked(),
            ),
        )
        self.ok_button.setGeometry(QtCore.QRect(10, 310, 93, 28))
        self.ok_button.setObjectName("ok_button")
        self.wage_label = QtWidgets.QLabel(self.input_group_box)
        self.wage_label.setGeometry(QtCore.QRect(140, 310, 51, 21))
        self.wage_label.setObjectName("wage_label")
        self.wage_entry = QtWidgets.QLineEdit(self.input_group_box)
        self.wage_entry.setGeometry(QtCore.QRect(200, 310, 181, 22))
        self.wage_entry.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.wage_entry.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.wage_entry.setClearButtonEnabled(True)
        self.wage_entry.setObjectName("wage_entry")

        # low frame
        self.tab_widget = QtWidgets.QTabWidget(self.central_widget)
        self.tab_widget.setGeometry(QtCore.QRect(10, 370, 1071, 521))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tab_widget.setFont(font)
        self.tab_widget.setObjectName("tab_widget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.date_table_widget = QtWidgets.QTableWidget(self.tab)
        self.date_table_widget.setGeometry(QtCore.QRect(10, 30, 561, 451))
        self.date_table_widget.setRowCount(100)
        self.date_table_widget.setObjectName("date_table_widget")
        self.date_table_widget.setColumnCount(4)
        item = QtWidgets.QTableWidgetItem()
        self.date_table_widget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.date_table_widget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.date_table_widget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.date_table_widget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.date_table_widget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.date_table_widget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.date_table_widget.setHorizontalHeaderItem(3, item)
        self.account_table_widget = QtWidgets.QTableWidget(self.tab)
        self.account_table_widget.setGeometry(QtCore.QRect(580, 280, 471, 201))
        self.account_table_widget.setObjectName("account_table_widget")
        self.account_table_widget.setColumnCount(2)
        self.account_table_widget.setRowCount(6)
        item = QtWidgets.QTableWidgetItem()
        self.account_table_widget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.account_table_widget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.account_table_widget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.account_table_widget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.account_table_widget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.account_table_widget.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.account_table_widget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.account_table_widget.setHorizontalHeaderItem(1, item)
        self.tab_remain_widget = QtWidgets.QTabWidget(self.tab)
        self.tab_remain_widget.setGeometry(QtCore.QRect(580, 0, 481, 271))
        self.tab_remain_widget.setObjectName("tab_remain_widget")
        self.number_tab_remain_widget = QtWidgets.QWidget()
        self.number_tab_remain_widget.setObjectName("number_tab_remain_widget")
        self.type_table_widget = QtWidgets.QTableWidget(self.number_tab_remain_widget)
        self.type_table_widget.setGeometry(QtCore.QRect(0, 0, 471, 241))
        self.type_table_widget.setObjectName("type_table_widget")
        self.type_table_widget.setColumnCount(5)
        self.type_table_widget.setRowCount(13)
        item = QtWidgets.QTableWidgetItem()
        self.type_table_widget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.type_table_widget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.type_table_widget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.type_table_widget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.type_table_widget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.type_table_widget.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.type_table_widget.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.type_table_widget.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.type_table_widget.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.type_table_widget.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.type_table_widget.setVerticalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.type_table_widget.setVerticalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.type_table_widget.setVerticalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.type_table_widget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.type_table_widget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.type_table_widget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.type_table_widget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.type_table_widget.setHorizontalHeaderItem(4, item)
        self.tab_remain_widget.addTab(self.number_tab_remain_widget, "")
        self.percent_tab_remain_widget = QtWidgets.QWidget()
        self.percent_tab_remain_widget.setObjectName("percent_tab_remain_widget")
        self.percent_table = QtWidgets.QTableWidget(self.percent_tab_remain_widget)
        self.percent_table.setGeometry(QtCore.QRect(0, 0, 471, 241))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.percent_table.setFont(font)
        self.percent_table.setObjectName("percent_table")
        self.percent_table.setColumnCount(5)
        self.percent_table.setRowCount(13)
        item = QtWidgets.QTableWidgetItem()
        self.percent_table.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.percent_table.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.percent_table.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.percent_table.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.percent_table.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.percent_table.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.percent_table.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.percent_table.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.percent_table.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.percent_table.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.percent_table.setVerticalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.percent_table.setVerticalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.percent_table.setVerticalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.percent_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.percent_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.percent_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.percent_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.percent_table.setHorizontalHeaderItem(4, item)
        self.tab_remain_widget.addTab(self.percent_tab_remain_widget, "")
        self.tab_widget.addTab(self.tab, "")
        self.graphic_tab_widget = QtWidgets.QWidget()
        self.graphic_tab_widget.setObjectName("graphic_tab_widget")
        self.graphics_view = QtWidgets.QGraphicsView(self.graphic_tab_widget)
        self.graphics_view.setGeometry(QtCore.QRect(10, 10, 1031, 461))
        self.graphics_view.setObjectName("graphics_view")
        self.tab_widget.addTab(self.graphic_tab_widget, "")
        # right frame
        self.function_group_box = QtWidgets.QGroupBox(self.central_widget)
        self.function_group_box.setGeometry(QtCore.QRect(430, 10, 651, 351))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.function_group_box.setFont(font)
        self.function_group_box.setObjectName("function_group_box")
        self.calendar_widget = QtWidgets.QCalendarWidget(self.function_group_box)
        self.calendar_widget.setGeometry(QtCore.QRect(10, 40, 451, 301))
        self.calendar_widget.setObjectName("calendar_widget")
        self.view_group_box = QtWidgets.QGroupBox(self.function_group_box)
        self.view_group_box.setGeometry(QtCore.QRect(480, 30, 161, 101))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.view_group_box.setFont(font)
        self.view_group_box.setObjectName("view_group_box")
        self.date_check_box = QtWidgets.QCheckBox(self.view_group_box)
        self.date_check_box.setGeometry(QtCore.QRect(10, 30, 81, 20))
        self.date_check_box.setObjectName("date_check_box")
        self.month_check_box = QtWidgets.QCheckBox(self.view_group_box)
        self.month_check_box.setGeometry(QtCore.QRect(10, 60, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.month_check_box.setFont(font)
        self.month_check_box.setObjectName("month_check_box")
        self.view_button = QtWidgets.QPushButton(
            self.view_group_box,
            clicked=lambda: view_function(
                self.date_table_widget,
                self.type_table_widget,
                self.percent_table,
                self.account_table_widget,
                self.calendar_widget.selectedDate().toPyDate().strftime("%d/%m/%Y"),
                self.date_check_box.isChecked(),
            ),
        )
        self.view_button.setGeometry(QtCore.QRect(90, 20, 61, 61))
        self.view_button.setObjectName("view_button")
        self.chart_group_box = QtWidgets.QGroupBox(self.function_group_box)
        self.chart_group_box.setGeometry(QtCore.QRect(480, 160, 161, 181))
        self.chart_group_box.setObjectName("chart_group_box")
        self.date_chart_check_box = QtWidgets.QCheckBox(self.chart_group_box)
        self.date_chart_check_box.setGeometry(QtCore.QRect(10, 30, 81, 20))
        self.date_chart_check_box.setObjectName("date_chart_check_box")
        self.month_chart_check_box = QtWidgets.QCheckBox(self.chart_group_box)
        self.month_chart_check_box.setGeometry(QtCore.QRect(80, 30, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.month_chart_check_box.setFont(font)
        self.month_chart_check_box.setObjectName("month_chart_check_box")
        self.pie_button = QtWidgets.QPushButton(
            self.chart_group_box,
            clicked=lambda: create_pie_chart(
                self.calendar_widget.selectedDate().toPyDate().strftime("%d/%m/%Y"),
                self.graphics_view,
            ),
        )
        self.pie_button.setGeometry(QtCore.QRect(10, 70, 141, 31))
        self.pie_button.setObjectName("pie_button")
        self.bar_button = QtWidgets.QPushButton(
            self.chart_group_box,
            clicked=lambda: create_bar_chart(
                self.graphics_view,
                self.month_chart_check_box.isChecked(),
                self.calendar_widget.selectedDate().toPyDate().strftime("%d/%m/%Y"),
            ),
        )
        self.bar_button.setGeometry(QtCore.QRect(10, 120, 141, 31))
        self.bar_button.setObjectName("bar_button")
        self.tab_widget.raise_()
        self.input_group_box.raise_()
        self.function_group_box.raise_()
        main_window.setCentralWidget(self.central_widget)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)
        self.retranslateUi(main_window)
        self.tab_widget.setCurrentIndex(0)
        self.tab_remain_widget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "MainWindow"))
        self.input_group_box.setTitle(_translate("main_window", "INPUT"))
        self.date_input.setDisplayFormat(_translate("main_window", "dd/MM/yyyy"))
        self.date_label.setText(
            _translate("main_window", "<html><head/><body><p>Date</p></body></html>")
        )
        self.list_table.setText(
            _translate("main_window", "<html><head/><body><p>List</p></body></html>")
        )
        self.type_label.setText(
            _translate("main_window", "<html><head/><body><p>Type</p></body></html>")
        )
        self.type_combo_box.setItemText(0, _translate("main_window", "necessity"))
        self.type_combo_box.setItemText(1, _translate("main_window", "play"))
        self.type_combo_box.setItemText(2, _translate("main_window", "savings"))
        self.type_combo_box.setItemText(3, _translate("main_window", "education"))
        self.type_combo_box.setItemText(
            4, _translate("main_window", "financial freedom")
        )
        self.account_label.setText(
            _translate(
                "main_window",
                "<html><head/><body><p>Account</p><p><br/></p><p><br/></p></body></html>",
            )
        )
        self.account_combo_box.setItemText(0, _translate("main_window", "BIDV"))
        self.account_combo_box.setItemText(1, _translate("main_window", "momo"))
        self.account_combo_box.setItemText(2, _translate("main_window", "finhay"))
        self.account_combo_box.setItemText(3, _translate("main_window", "wallet"))
        self.account_combo_box.setItemText(
            4, _translate("main_window", "investment account")
        )
        self.amount_label.setText(
            _translate("main_window", "<html><head/><body><p>Amount</p></body></html>")
        )
        self.income_check_box.setText(_translate("main_window", "Income"))
        self.outcome_check_box.setText(_translate("main_window", "Outcome"))
        self.ok_button.setText(_translate("main_window", "OK"))
        self.wage_label.setText(
            _translate("main_window", "<html><head/><body><p>Wage</p></body></html>")
        )
        self.wage_entry.setText(_translate("main_window", "5000000"))
        item = self.date_table_widget.verticalHeaderItem(0)
        item.setText(_translate("main_window", "0"))
        item = self.date_table_widget.verticalHeaderItem(1)
        item.setText(_translate("main_window", "1"))
        item = self.date_table_widget.verticalHeaderItem(2)
        item.setText(_translate("main_window", "2"))
        item = self.date_table_widget.horizontalHeaderItem(0)
        item.setText(_translate("main_window", "Date"))
        item = self.date_table_widget.horizontalHeaderItem(1)
        item.setText(_translate("main_window", "List"))
        item = self.date_table_widget.horizontalHeaderItem(2)
        item.setText(_translate("main_window", "Type"))
        item = self.date_table_widget.horizontalHeaderItem(3)
        item.setText(_translate("main_window", "Amount"))
        item = self.account_table_widget.verticalHeaderItem(0)
        item.setText(_translate("main_window", "Amount"))
        item = self.account_table_widget.verticalHeaderItem(1)
        item.setText(_translate("main_window", "BIDV"))
        item = self.account_table_widget.verticalHeaderItem(2)
        item.setText(_translate("main_window", "momo"))
        item = self.account_table_widget.verticalHeaderItem(3)
        item.setText(_translate("main_window", "finhay"))
        item = self.account_table_widget.verticalHeaderItem(4)
        item.setText(_translate("main_window", "wallet"))
        item = self.account_table_widget.verticalHeaderItem(5)
        item.setText(_translate("main_window", "investment account"))
        item = self.account_table_widget.horizontalHeaderItem(0)
        item.setText(_translate("main_window", "Total"))
        item = self.account_table_widget.horizontalHeaderItem(1)
        item.setText(_translate("main_window", "Percentage"))
        item = self.type_table_widget.verticalHeaderItem(0)
        item.setText(_translate("main_window", "Remain"))
        item = self.type_table_widget.verticalHeaderItem(1)
        item.setText(_translate("main_window", "Jan"))
        item = self.type_table_widget.verticalHeaderItem(2)
        item.setText(_translate("main_window", "Feb"))
        item = self.type_table_widget.verticalHeaderItem(3)
        item.setText(_translate("main_window", "Mar"))
        item = self.type_table_widget.verticalHeaderItem(4)
        item.setText(_translate("main_window", "Apr"))
        item = self.type_table_widget.verticalHeaderItem(5)
        item.setText(_translate("main_window", "May"))
        item = self.type_table_widget.verticalHeaderItem(6)
        item.setText(_translate("main_window", "Jun"))
        item = self.type_table_widget.verticalHeaderItem(7)
        item.setText(_translate("main_window", "Jul"))
        item = self.type_table_widget.verticalHeaderItem(8)
        item.setText(_translate("main_window", "Aug"))
        item = self.type_table_widget.verticalHeaderItem(9)
        item.setText(_translate("main_window", "Sep"))
        item = self.type_table_widget.verticalHeaderItem(10)
        item.setText(_translate("main_window", "Oct"))
        item = self.type_table_widget.verticalHeaderItem(11)
        item.setText(_translate("main_window", "Nov"))
        item = self.type_table_widget.verticalHeaderItem(12)
        item.setText(_translate("main_window", "Dec"))
        item = self.type_table_widget.horizontalHeaderItem(0)
        item.setText(_translate("main_window", "necessity"))
        item = self.type_table_widget.horizontalHeaderItem(1)
        item.setText(_translate("main_window", "play"))
        item = self.type_table_widget.horizontalHeaderItem(2)
        item.setText(_translate("main_window", "savings"))
        item = self.type_table_widget.horizontalHeaderItem(3)
        item.setText(_translate("main_window", "education"))
        item = self.type_table_widget.horizontalHeaderItem(4)
        item.setText(_translate("main_window", "financial freedom"))
        self.tab_remain_widget.setTabText(
            self.tab_remain_widget.indexOf(self.number_tab_remain_widget),
            _translate("main_window", "Number"),
        )
        item = self.percent_table.verticalHeaderItem(0)
        item.setText(_translate("main_window", "Remain"))
        item = self.percent_table.verticalHeaderItem(1)
        item.setText(_translate("main_window", "Jan"))
        item = self.percent_table.verticalHeaderItem(2)
        item.setText(_translate("main_window", "Feb"))
        item = self.percent_table.verticalHeaderItem(3)
        item.setText(_translate("main_window", "Mar"))
        item = self.percent_table.verticalHeaderItem(4)
        item.setText(_translate("main_window", "Apr"))
        item = self.percent_table.verticalHeaderItem(5)
        item.setText(_translate("main_window", "May"))
        item = self.percent_table.verticalHeaderItem(6)
        item.setText(_translate("main_window", "Jun"))
        item = self.percent_table.verticalHeaderItem(7)
        item.setText(_translate("main_window", "Jul"))
        item = self.percent_table.verticalHeaderItem(8)
        item.setText(_translate("main_window", "Aug"))
        item = self.percent_table.verticalHeaderItem(9)
        item.setText(_translate("main_window", "Sep"))
        item = self.percent_table.verticalHeaderItem(10)
        item.setText(_translate("main_window", "Oct"))
        item = self.percent_table.verticalHeaderItem(11)
        item.setText(_translate("main_window", "Nov"))
        item = self.percent_table.verticalHeaderItem(12)
        item.setText(_translate("main_window", "Dec"))
        item = self.percent_table.horizontalHeaderItem(0)
        item.setText(_translate("main_window", "necessity"))
        item = self.percent_table.horizontalHeaderItem(1)
        item.setText(_translate("main_window", "play"))
        item = self.percent_table.horizontalHeaderItem(2)
        item.setText(_translate("main_window", "savings"))
        item = self.percent_table.horizontalHeaderItem(3)
        item.setText(_translate("main_window", "education"))
        item = self.percent_table.horizontalHeaderItem(4)
        item.setText(_translate("main_window", "financial freedom"))
        self.tab_remain_widget.setTabText(
            self.tab_remain_widget.indexOf(self.percent_tab_remain_widget),
            _translate("main_window", "Percentage"),
        )
        self.tab_widget.setTabText(
            self.tab_widget.indexOf(self.tab), _translate("main_window", "TABLE")
        )
        self.tab_widget.setTabText(
            self.tab_widget.indexOf(self.graphic_tab_widget),
            _translate("main_window", "GRAPHIC"),
        )
        self.function_group_box.setTitle(_translate("main_window", "FUNCTION"))
        self.view_group_box.setTitle(_translate("main_window", "View By"))
        self.date_check_box.setText(_translate("main_window", "Date"))
        self.month_check_box.setText(_translate("main_window", "Month"))
        self.view_button.setText(_translate("main_window", "view"))
        self.chart_group_box.setTitle(_translate("main_window", "Chart"))
        self.date_chart_check_box.setText(_translate("main_window", "Date"))
        self.month_chart_check_box.setText(_translate("main_window", "Month"))
        self.pie_button.setText(_translate("main_window", "Pie Chart"))
        self.bar_button.setText(_translate("main_window", "Bar Chart"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    cur_data = create_object()
    BIDV = Account(cur_data[0])
    momo = Account(cur_data[1])
    finhay = Account(cur_data[2])
    wallet = Account(cur_data[3])
    investment_account = Account(cur_data[4])

    bar_plot = bar_graph_1 = bar_graph_2 = None

    FUND_DICT = {
        "BIDV": BIDV,
        "momo": momo,
        "finhay": finhay,
        "wallet": wallet,
        "investment account": investment_account,
    }

    ui = Ui_main_window()
    ui.setupUi(MainWindow)

    WAGE = int(ui.wage_entry.text())
    NECESSITY = 0.55 * WAGE
    PLAY = 0.1 * WAGE
    SAVINGS = 0.1 * WAGE
    EDUCATION = 0.1 * WAGE
    FINANCIAL_FREEDOM = 0.15 * WAGE

    MainWindow.show()
    sys.exit(app.exec_())
