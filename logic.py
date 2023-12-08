from PyQt6.QtWidgets import *
from gui import *
import random
import csv


class Logic(QMainWindow, Ui_BankRegistration):
    CSV_FILE = 'user_info.csv'
    user_info = {}

    def __init__(self) -> None:
        """initial GUI set up"""
        super().__init__()
        self.setupUi(self)
        self.frame1.hide()
        self.frame2.hide()
        self.frame3.hide()
        self.button_enter.clicked.connect(lambda: self.enter())
        self.button_login_create.clicked.connect(lambda: self.login_create())
        self.button_submit.clicked.connect(lambda: self.submit())
        self.button_complete.clicked.connect(lambda: self.complete())
        self.button_logout.clicked.connect(lambda: self.logout())

        self.load_user_info()

    def clear(self) -> None:
        """Clears the input contents in frame1"""
        self.input_name.clear()
        self.input_age_acct_num.clear()
        self.input_address.clear()
        self.input_pin.clear()
        self.input_set_balance.clear()
        self.label_welcome.clear()
        self.frame2.hide()
        self.frame3.hide()

    def enter(self) -> None:
        """shows frame1 and the relevant labels and inputs to
        create an account or to login"""
        if self.radioButton_create_acct.isChecked():
            self.frame1.show()
            self.clear()
            self.label_age_acct_num.setText('Age')
            self.label_address.show()
            self.input_address.show()
            self.label_set_balance.show()
            self.input_set_balance.show()
            self.button_login_create.setText('Create Account')
        elif self.radioButton_login.isChecked():
            self.frame1.show()
            self.clear()
            self.label_age_acct_num.setText('Account Number')
            self.label_address.hide()
            self.input_address.hide()
            self.label_set_balance.hide()
            self.input_set_balance.hide()
            self.button_login_create.setText('Login')

    def load_user_info(self) -> None:
        """accesses the user's information in the csvfile if user
        has a valid account number"""
        try:
            with open(self.CSV_FILE, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    account_num = int(row['account_num'])
                    Logic.user_info[account_num] = {
                        'name': row['name'],
                        'age': int(row['pin']),
                        'address': row['address'],
                        'pin': int(row['pin']),
                        'balance': float(row['balance'])
                    }
        except FileNotFoundError:
            pass

    def save_user_info(self) -> None:
        """saves user information if not already in the csvfile"""
        with open(self.CSV_FILE, 'w', newline='') as csvfile:
            fieldnames = ['account_num', 'name', 'age', 'address', 'pin', 'balance']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for account_num, user_info in Logic.user_info.items():
                writer.writerow({
                    'account_num': account_num,
                    'name': user_info['name'],
                    'age': user_info['age'],
                    'address': user_info['address'],
                    'pin': user_info['pin'],
                    'balance': user_info['balance']
                })

    def update_balance_in_csv(self, account_num: int, new_balance: float) -> None:
        """updates the user balance in the csvfile"""
        Logic.user_info[account_num]['balance'] = new_balance
        self.save_user_info()

    def login_create(self) -> None:
        """displays frame 2
        depending on which radioButton is checked, different events
        if radioButton Create Account checked, validates input information
        and send to csvfile to store
        if radioButton Login checked, validates login credentials in csvfile,
        to access account"""
        if self.radioButton_create_acct.isChecked():
            self.label_welcome.clear()
            self.name = self.input_name.text()
            self.age = self.input_age_acct_num.text()
            self.address = self.input_address.text()
            self.pin = self.input_pin.text()
            self.set_balance = self.input_set_balance.text()
            try:
                self.age = int(self.age)
                self.pin = int(self.pin)
                self.balance = float(self.set_balance)
                if self.age >= 16:
                    self.acct_num = random.randint(10000, 99999)
                    self.clear()
                    self.label_welcome.setText(f"Welcome to V.S. Banking. Your Account # is: {self.acct_num}.\n"
                                               f"Please save for future references. Happy Banking!")
                    Logic.user_info[self.acct_num] = {
                        'name': self.name,
                        'age': self.age,
                        'address': self.address,
                        'pin': self.pin,
                        'balance': float(self.balance)
                    }
                    self.save_user_info()
                    self.frame2.show()
                else:
                    self.clear()
                    self.label_welcome.setText('You are to young to open an account. Come back in a few years :)')
            except ValueError:
                self.clear()
                self.label_welcome.setText('Please enter valid information.')
        elif self.radioButton_login.isChecked():
            self.label_welcome.clear()
            self.name = self.input_name.text()
            self.acct_num = self.input_age_acct_num.text()
            self.pin = self.input_pin.text()

            try:
                self.acct_num = int(self.acct_num)
                self.pin = int(self.pin)
                if self.validate_credentials():
                    self.clear()
                    self.label_welcome.setText(f"Welcome back {self.name}. Happy Banking!")
                    self.frame2.show()

                else:
                    self.clear()
                    self.label_welcome.setText(f"Please enter valid information.")
            except ValueError:
                self.clear()
                self.label_welcome.setText(f"Invalid Credentials. Please try again.")

    def validate_credentials(self) -> bool:
        """Validates the login credentials in csvfile to access bank account information"""
        if self.acct_num and int(self.acct_num) in Logic.user_info:
            user_info = Logic.user_info[int(self.acct_num)]
            return user_info['name'] == self.name and user_info['pin'] == self.pin
        else:
            return False

    def submit(self) -> None:
        """shows frame3
        depending on which transaction type selected, displays  relevant transaction type
        or displays banker information"""
        if self.radioButton_deposit.isChecked() or self.radioButton_withdraw.isChecked():
            self.frame3.show()
            self.label_transaction_type.show()
            self.input_trans_amount.show()
            self.button_complete.show()
            if self.radioButton_deposit.isChecked():
                self.label_transaction_type.setText('Deposit Amount')
            elif self.radioButton_withdraw.isChecked():
                self.label_transaction_type.setText('Withdraw Amount')

            self.input_trans_amount.clear()
            self.label_avail_bal.hide()
        elif self.radioButton_balance.isChecked():
            self.frame3.show()
            self.label_transaction_type.hide()
            self.input_trans_amount.hide()
            self.button_complete.hide()
            self.label_avail_bal.show()
            self.label_avail_bal.setText(F"Available Balance: ${Logic.user_info[self.acct_num]['balance']}")

    def complete(self) -> None:
        """performs the relevant transaction and sends new balance to csvfile to store"""
        if self.radioButton_deposit.isChecked() or self.radioButton_withdraw.isChecked():
            self.label_avail_bal.clear()
            self.label_avail_bal.hide()

            try:
                transaction_amount = float(self.input_trans_amount.text())
                if self.radioButton_deposit.isChecked():
                    Logic.user_info[self.acct_num]['balance'] += transaction_amount
                    self.update_balance_in_csv(self.acct_num, Logic.user_info[self.acct_num]['balance'])
                    self.label_avail_bal.show()
                    self.label_avail_bal.setText(f"Transaction Successful. \n"
                                                 f"Available balance: ${Logic.user_info[self.acct_num]['balance']:.2f}")
                elif self.radioButton_withdraw.isChecked():
                    if transaction_amount > Logic.user_info[self.acct_num]['balance']:
                        self.label_avail_bal.show()
                        self.label_avail_bal.setText('Withdrawal amount exceeds available balance')
                    else:
                        Logic.user_info[self.acct_num]['balance'] -= transaction_amount
                        self.update_balance_in_csv(self.acct_num, Logic.user_info[self.acct_num]['balance'])
                        self.label_avail_bal.show()
                        self.label_avail_bal.setText(f"Transaction Successful. \n"
                                                     f"Available balance: \n"
                                                     f"${Logic.user_info[self.acct_num]['balance']:.2f}")
                self.input_trans_amount.clear()
            except ValueError:
                self.label_avail_bal.show()
                self.label_avail_bal.setText('Please enter a valid numeric amount')

    def logout(self):
        """Closes/logs out of the GUI"""
        self.close()
