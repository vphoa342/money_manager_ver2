class Month:
    def __init__(self, necessity, play, savings, education, financial_freedom):
        self.necessity = necessity
        self.play = play
        self.savings = savings
        self.education = education
        self.financial_freedom = financial_freedom

    def add_money(self, value, type_data):
        if type_data == "necessity":
            self.necessity += value
        elif type_data == "play":
            self.play += value
        elif type_data == "savings":
            self.savings += value
        elif type_data == "education":
            self.education += value
        else:
            self.financial_freedom += value


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


FILE_TXT = "C:\\Users\\Van Phu Hoa\\PycharmProjects\\money_tracker\\funds_database.txt"
try:
    file = open(FILE_TXT, mode="r")

    line_as_string = file.readline().split()
    wage = int(line_as_string[1])

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
finally:
    file.close()

# create accounts
BIDV = Account(cur_BIDV)
momo = Account(cur_momo)
finhay = Account(cur_finhay)
wallet = Account(cur_wallet)
investment_account = Account(cur_investment_account)
