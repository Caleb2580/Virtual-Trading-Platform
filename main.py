import PyQt5
from PyQt5.QtCore import QSize, QRect
from PyQt5.QtGui import QIcon, QPixmap, QTransform, QFont, QCursor, QImage, QDoubleValidator


from PyQt5.QtWidgets import QScrollArea, QLabel, QGraphicsScene
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer

from mainwindow import Ui_MainWindow
from CustomWidgets import ChartPopup, PaddedItemDelegate

import PIL
from PIL import Image, ImageDraw
import json
from math import floor, ceil
from pymongo import MongoClient
import random
import datetime

from grab import get_data, get_data_date

OPEN = 0
CLOSE = 1
LOW = 2
HIGH = 3
VOLUME = 4

reset_tickers = [
            "AAPL", "MSFT", "AMZN", "GOOGL", "TSLA", "FB", "NVDA", "JPM", "V", "JNJ", "PG", "UNH", "MA", "INTC", "HD",
            "BAC", "DIS", "CMCSA", "VZ", "ADBE", "NFLX", "PYPL", "T", "CRM", "PEP", "CSCO", "ABBV", "KO", "XOM", "MRK", "WMT",
            "ABT", "PFE", "CVX", "NKE", "TMO", "ACN", "COST", "DHR", "AMGN", "NEE", "MDT", "AVGO", "UNP", "TXN", "QCOM", "HON",
            "LIN", "PM", "LLY", "UPS", "SBUX", "LOW", "BA", "ORCL", "AMD", "IBM", "NOW", "GS", "INTU", "CHTR", "AMAT", "CAT",
            "FIS", "MMM", "BDX", "GILD", "CVS", "MO", "SPGI", "ANTM", "ISRG", "ADP", "CME", "MMC", "VRTX", "ZTS", "CSX", "RTX",
            "TGT", "LMT", "SCHW", "BIIB", "CI", "SYK", "PNC", "AXP", "APD", "FDX", "BKNG", "TMUS", "COP", "DUK", "DOW", "ECL",
            "SO", "ADI", "AGN", "BDX", "D", "EMR", "EW", "EXC", "HUM", "ICE", "KLAC", "MCD", "MCK", "MET", "MS", "NEE", "NSC",
            "PLD", "PSX", "SPG", "TJX", "WBA", "WFC", "AIG", "ALL", "APTV", "BIIB", "BSX", "COF", "DAL", "DE", "DXCM", "EQR",
            "ETN", "GD", "ITW", "JCI", "KMB", "KR", "MAR", "MTD", "MU", "NEM", "ORLY", "PKG", "RMD", "SWK", "UAL", "VRTX",
            "WELL", "YUM", "BIO", "BSX", "CTSH", "DRI", "EBAY", "FISV", "FLT", "GPN", "IDXX", "ILMN", "IQV",
            "KHC", "MNST", "MSCI", "NTAP", "NUE", "PAYX", "REGN", "ROST", "STZ", "TT", "VRSK", "WST", "XLNX", "ALGN", "ANSS",
            "APH", "CERN", "EXPE", "FLIR", "FTNT", "KEYS", "LEN", "LRCX", "MXIM", "NTRS", "ODFL", "OKTA", "POOL", "SNPS",
            "TFX", "TTWO", "UAL", "ULTA", "URI", "VRSN", "ZBRA", "ZG", "AAP", "DLTR", "ETSY", "FOXA",
            "HCA", "HOLX", "IDXX", "INCY", "IR", "JKHY", "MKTX", "MNST", "MTCH", "NTES", "NTNX", "NWSA",
            "PEAK", "PENN", "PTON", "ROKU", "SEDG", "SPLK", "TTD", "TWTR", "UAA", "VRSK", "WYNN",
        ]


sty = """
QWidget[objectName="centralwidget"] {
    background-color: rgb(25, 25, 25);
}

QFrame[objectName="trade_frame"] {
    background-color: rgb(50, 50, 50);
}

QLabel[objectName="trade_log_title"] {
    background-color: transparent;
    color: white;
    font-size: 18px;
}

QLabel[objectName="trade_log"] {
    background-color: rgba(0, 0, 0, .5);
    color: white;
}

QPushButton[objectName="buy_button"] {
    font-size: 20px;
    color: rgb(250, 250, 250);
    background-color: rgb(75, 150, 75);
    border: none;
}
QPushButton[objectName="buy_button"]:hover {
    background-color: rgb(100, 200, 100);
    border: none;
}
QPushButton[objectName="buy_button"]:pressed {
    border: 2px solid white;
}

QPushButton[objectName="sell_button"] {
    font-size: 20px;
    color: rgb(250, 250, 250);
    background-color: rgb(150, 75, 75);
    border: none;
}
QPushButton[objectName="sell_button"]:hover {
    background-color: rgb(255, 75, 75);
    border: none;
}
QPushButton[objectName="sell_button"]:pressed {
    border: 2px solid white;
}

QPushButton[objectName="step_button"] {
    font-size: 15px;
    color: rgb(10, 10, 10);
    background-color: rgb(250, 250, 250);
    border: none;
}

QFrame[objectName="trade_options_frame"] {
    background-color: rgba(0, 0, 0, .25);
}

QLineEdit[objectName="amt_line_edit"] {
    background-color: transparent;
    border: none;
    font-size: 20px;
    color: white;
    border-bottom: 2px solid white;
    padding-left: 50px;
}

QLabel[objectName="dollar_sign"] {
    background-color: transparent;
    color: white;
    font-size: 25px;
}

QComboBox[objectName="call_put_combo_box"] {
    color: white;
    background-color: rgb(50, 50, 50);
    padding: 5px;
    border: none;
    font-size: 15px;
    text-align: center;
}

QComboBox[objectName="call_put_combo_box"] QAbstractItemView {
    color: white;
    background-color: rgb(50, 50, 50);
}

QComboBox[objectName="call_put_combo_box"]::drop-down {
    border: none;
}


QProgressBar[objectName="day_progress_bar"] {
    color: white;
}


QFrame[objectName="bought_frame"] {
    border: none;
    background-color: rgba(0, 0, 0, .25);
}

QLabel[objectName="bought_call_label"] {
    color: rgb(100, 150, 100);
    font-size: 18px;
}
QLabel[objectName="bought_put_label"] {
    color: rgb(175, 100, 100);
    font-size: 18px;
}
QLabel[objectName="bought_invested_label"] {
    color: white;
    font-size: 18px;
}


QLabel[objectName="username_label"] {
    color: white;
    background-color: transparent;
    font-size: 30px;
}

QLabel[objectName="money_label"] {
    color: white;
    background-color: transparent;
    font-size: 30px;
}


QPushButton[objectName="new_chart_button"] {
    background-color: rgb(150, 150, 150);
    color: white;
    font-size: 30px;
    border: none;
}
QPushButton[objectName="new_chart_button"]:hover {
    background-color: rgb(175, 175, 175);
}
QPushButton[objectName="new_chart_button"]:pressed {
    border: 2px solid rgb(50, 50, 50);
}

QPushButton[objectName="open_chart_button"] {
    background-color: rgb(150, 150, 150);
    color: white;
    font-size: 13px;
    border: none;
}
QPushButton[objectName="open_chart_button"]:hover {
    background-color: rgb(175, 175, 175);
}
QPushButton[objectName="open_chart_button"]:pressed {
    border: 2px solid rgb(50, 50, 50);
}

"""

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)

        self.setWindowTitle("Intellitrade")

        self.db = MongoClient('<server-link>')['options']['people']
        
        if not self.login():
            sys.exit()

        print(f'${self.user["balance"]}')

        self.balance = self.user['balance']

        self.tickers = reset_tickers.copy()
        self.chart_scene = QGraphicsScene()

        self.active_charts = []

        self.chart_popup = None
        # self.chart_popup = ChartPopup('AAPL', '2024-02-27')
        # self.chart_popup.show()

        self.investments = [0, 0, None]
        self.investments_stocks = [0, 0, 0, 0]

        if True:  #  Basic Setup
            # validator = QDoubleValidator()
            # validator.setNotation(QDoubleValidator.StandardNotation)
            # self.amt_line_edit.setValidator(validator)

            padded_dg = PaddedItemDelegate()
            self.call_put_combo_box.setItemDelegate(padded_dg)
            self.call_put_combo_box.addItem('Call')
            self.call_put_combo_box.addItem('Put')

            self.username_label.setText(self.user['username'])
            self.money_label.setText(f'${self.user["balance"]:.2f}')

            self.new_chart_button.clicked.connect(self.new_chart)
            self.open_chart_button.clicked.connect(self.open_chart)

            self.buy_button.clicked.connect(self.buy)
            self.sell_button.clicked.connect(self.sell)

        self.money_timer = QTimer()
        self.money_timer.timeout.connect(self.update_balance)
        self.money_timer.start(100)

        self.step_button.clicked.connect(self.step)

        self.day_progress_bar.setMaximum(390)
        self.day_progress_bar.setMinimum(0)
        self.day_progress_bar.setValue(0)

    def login(self):
        try:
            self.login_info = json.load(open('./login_info.json', 'r+'))
        except Exception:
            print('Error logging in: Missing file or file corrupt { login_info.json }')
            return False
        
        res = self.db.find_one(
            {
                'username': self.login_info['username'],
            })
        
        if res is not None:
            if res['password'] == self.login_info['password']:
                print(f'User {self.login_info["username"]} logged in successfully')
                self.user = res
            return True

        print(f'User {self.login_info["username"]} not found')
        return False
    
    def update_balance(self):
        self.money_label.setText(f'${self.balance:.2f}')

        self.bought_call_label.setText(f'Call: ${self.investments[0]:.4f}')
        self.bought_put_label.setText(f'Put: ${self.investments[1]:.4f}')
        self.bought_invested_label.setText(f'Invested: ${self.investments[0] + self.investments[1]:.4f}')

    def upload_data(self):
        self.user['balance'] = self.balance + self.investments[0] + self.investments[1]
        self.db.update_one({"username": self.user['username'], 'password': self.user['password']}, {"$set": {"balance": self.user['balance']}})
        self.db.update_one({"username": self.user['username'], 'password': self.user['password']}, {"$set": {"trades": self.user["trades"]}})

    def step(self):
        if self.chart_popup is not None:
            if self.chart_popup.step():
                print('Game Over')
                self.investments = self.investments = [0, 0, None]
                self.investments_stocks = [0, 0]
                self.balance = self.user['balance']
                self.chart_popup.hide()
                self.chart_popup = None
                return
            else:
                self.chart_popup.update()
            
            d = self.chart_popup.data[self.chart_popup.last_index]
            
            if self.investments[2] is None:
                self.investments[2] = d[1][CLOSE]
            else:
                self.investments[2] = d[1][CLOSE]

                call_dif = (self.investments_stocks[0] * self.investments[2]) - self.investments_stocks[2]
                put_dif = self.investments_stocks[3] - (self.investments_stocks[1] * self.investments[2])

                self.investments[0] = (self.investments_stocks[2] + call_dif*100)
                self.investments[1] = (self.investments_stocks[3] + put_dif*100)

                self.investments[0] = max(0, self.investments[0])
                self.investments[1] = max(0, self.investments[1])

                if self.investments[0] > 0 or self.investments[1] > 0:
                    # self.user['trades'] = self.user['trades'] + [self.balance + self.investments[0] + self.investments[1]]
                    self.upload_data()
            self.day_progress_bar.setValue(self.chart_popup.get_progress())

            # print(self.investments_stocks, self.investments)

    def buy(self):
        if self.chart_popup is not None:
            d = self.chart_popup.data[self.chart_popup.last_index]
            
            amt = self.amt_line_edit.text()
            c_or_p = self.call_put_combo_box.currentIndex()

            if amt != '':
                try:
                    amt = float(amt)
                    if 0 < amt <= self.balance:
                        self.investments[2] = d[1][CLOSE]
                        self.investments_stocks[0 if c_or_p == 0 else 1] += amt/d[1][CLOSE]
                        self.investments_stocks[2 if c_or_p == 0 else 3] += amt
                        # Call and Put dif
                        call_dif = (self.investments_stocks[0] * self.investments[2]) - self.investments_stocks[2]
                        put_dif = self.investments_stocks[3] - (self.investments_stocks[1] * self.investments[2])

                        self.investments[0] = (self.investments_stocks[2] + call_dif*100)
                        self.investments[1] = (self.investments_stocks[3] + put_dif*100)

                        self.balance -= amt

                        text = self.trade_log.text()
                        text = f'<span style="color: {"green" if c_or_p == 0 else "red"};">Bought ${amt:.4f} of {"Call" if c_or_p == 0 else "Put"}  @  ${d[1][CLOSE]:.4f}</span><br>' + text
                        self.trade_log.setText(text)
                except:
                    pass

    def sell(self):
        print('ss')
        if self.chart_popup is not None:
            amt = self.amt_line_edit.text()
            c_or_p = self.call_put_combo_box.currentIndex()

            if amt != '':
                try:
                    if amt == 'all' or amt == 'a':
                        amt = self.investments[0 if c_or_p == 0 else 1]
                    else:
                        amt = float(amt)
                    if self.investments[0 if c_or_p == 0 else 1] >= amt:

                        per = amt / self.investments[0 if c_or_p == 0 else 1]

                        self.investments_stocks[0 if c_or_p == 0 else 1] -= per * self.investments_stocks[0 if c_or_p == 0 else 1]
                        self.investments_stocks[2 if c_or_p == 0 else 3] -= per * self.investments_stocks[2 if c_or_p == 0 else 3]

                        call_dif = (self.investments_stocks[0] * self.investments[2]) - self.investments_stocks[2]
                        put_dif = self.investments_stocks[3] - (self.investments_stocks[1] * self.investments[2])

                        self.investments[0] = (self.investments_stocks[2] + call_dif*100)
                        self.investments[1] = (self.investments_stocks[3] + put_dif*100)

                        self.investments[0] = max(0, self.investments[0])
                        self.investments[1] = max(0, self.investments[1])

                        self.balance += amt

                        text = self.trade_log.text()
                        text = f'<span style="color: {"green" if c_or_p == 0 else "red"};">Sold ${amt:.4f} of {"Call" if c_or_p == 0 else "Put"}  @  ${self.investments[2]:.4f}</span><br>' + text
                        self.trade_log.setText(text)

                        self.user['trades'] = self.user['trades'] + [self.balance + self.investments[0] + self.investments[1]]
                        self.upload_data()
                except:
                    pass
            print(self.investments)

    def new_chart(self):
        # for i in self.investments:
        #     if i[1][1] is None:
        #         i[1][1] = self.chart_popup[self.last_index-1]
        #     self.balance += i[0] * i[1][1]/i[1][0]

        self.investments = [0, 0, None]
        self.investments_stocks = [0, 0, 0, 0]
        self.balance = self.user['balance']

        self.random_ticker()
        date = self.get_random_date()
        self.date = date
        
        # self.ticker = 'AMAT'
        # self.date = '2024-02-17'
        # self.ticker = "TTWO"
        # self.date = '2024-02-27'

        # Low
        # self.ticker = 'UAA'
        # self.date = '2024-03-10'
        print(self.ticker)
        print(self.date)

        self.day_progress_bar.setValue(0)

        if self.chart_popup is not None:
            self.chart_popup.close()

        self.chart_popup = ChartPopup(self.ticker, self.date)
        self.chart_popup.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.chart_popup.show()

    def open_chart(self):
        if self.chart_popup is not None:
            self.chart_popup.show()

    def random_ticker(self):
        self.ticker = random.choice(self.tickers)
        self.tickers.remove(self.ticker)

        if len(self.tickers) == 0:
            self.tickers = reset_tickers.copy()

    def get_random_date(self, delta=22):
        date = str(datetime.datetime.today() - datetime.timedelta(days=random.randint(0, delta))).split(' ')[0]
        return date

    def closeEvent(self, event):
        if self.chart_popup is not None:
            self.chart_popup.close()
        if self.investments[0] > 0 or self.investments[1] > 0:
            self.user['trades'] = self.user['trades'] + [self.balance + self.investments[0] + self.investments[1]]
            self.upload_data()
        # for c in range(0, 2):
            # try:
            #     amt = self.investments[c]
                
            #     if self.investments[c] >= amt:

            #         per = amt / self.investments[c]

            #         self.investments_stocks[c] -= per * self.investments_stocks[c]
            #         self.investments_stocks[c+2] -= per * self.investments_stocks[c+2]

            #         call_dif = (self.investments_stocks[c] * self.investments[2]) - self.investments_stocks[c+2]
            #         put_dif = self.investments_stocks[c+2] - (self.investments_stocks[c] * self.investments[2])

            #         self.investments[c] = (self.investments_stocks[c+2] + call_dif*100)
            #         self.investments[c] = (self.investments_stocks[c+2] + put_dif*100)

            #         self.investments[c] = max(0, self.investments[c])
            #         self.investments[c] = max(0, self.investments[c])

            #         self.balance += amt

            #         text = self.trade_log.text()
            #         text = f'<span style="color: {"green" if c == 0 else "red"};">Sold ${amt:.4f} of {"Call" if c == 0 else "Put"}  @  ${self.investments[2]:.4f}</span><br>' + text
            #         self.trade_log.setText(text)
            # except:
            #     pass
        event.accept()



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # with open('style.css', 'r+') as style:
    #     app.setStyleSheet(style.read())
    app.setStyleSheet(sty)
    
    w = MainWindow()
    w.show()

    sys.exit(app.exec_())































