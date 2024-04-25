import PyQt5
from PyQt5.QtCore import QSize, QRect
from PyQt5.QtGui import QIcon, QPixmap, QTransform, QFont, QCursor, QImage, QPainter, QColor, QImage, QPen


from PyQt5.QtWidgets import QScrollArea, QLabel, QGraphicsScene, QGraphicsView, QWidget, QProxyStyle, QFrame, QVBoxLayout
from PyQt5.QtWidgets import QPushButton, QComboBox, QStyledItemDelegate, QStyleOptionViewItem, QStyle, QListView
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer, QPoint

import PIL
from PIL import Image, ImageDraw, ImageQt

import random, json
from math import floor, ceil
from grab import get_data, get_data_date
import numpy as np


OPEN = 0
CLOSE = 1
LOW = 2
HIGH = 3


# def create_graph(data, candle_width=10):

#     data_min = min(min(data))
#     data_max = max(max(data))

#     width = int(ceil(len(data) * (candle_width)))
    
#     height = int((data_max - data_min) * 100)
#     image = Image.new("RGB", (width, height), (25, 25, 25))
#     draw = ImageDraw.Draw(image)

#     mi, ma = data_min - (data_max / 20), data_max + (data_max / 20)

#     dif = ma - mi

#     for i, d in enumerate(data):
#         rect = (
#             (
#                 i * (candle_width),
#                 (1 - (d[OPEN] - mi) / dif) * height
#             ),
#             (
#                 i * (candle_width) + candle_width - 1,
#                 (1 - (d[CLOSE] - mi) / dif) * height
#             )
#         )
#         draw.rectangle(rect, ((100, 255, 150) if d[OPEN] < d[CLOSE] else (255, 100, 100)))

#     # image.show()
#     return image


def create_graph2(data, candle_width=10):

    data_min = min([min(i[:-1]) for d, i in data])
    data_max = max([max(i[:-1]) for d, i in data])

    mi, ma = data_min - ((data_max - data_min) / 20), data_max + ((data_max - data_min) / 20)
    # ma = data_max
    # mi = data_min

    dif = ma - mi

    width = int(ceil(len(data) * (candle_width)))

    print(width, len(data), candle_width)
    
    # height = int((data_max - data_min) * 100)
    # print('----')
    # print(dif)
    # if dif > 20:
    #     height = int(dif / .01)
    # else:
    #     height = int(dif / .001)
    # print(height)

    height = 8000
    
    image = Image.new("RGB", (width, height), (25, 25, 25))
    draw = ImageDraw.Draw(image)

    for i, (d, info) in enumerate(data):

        rect = (
            (
                i * (candle_width),
                (1 - (info[HIGH] - mi) / dif) * height
            ),
            (
                i * (candle_width) + candle_width - 1,
                (1 - (info[LOW] - mi) / dif) * height
            )
        )
        draw.rectangle(rect, (150, 150, 150))

        rect = (
            (
                i * (candle_width),
                (1 - (info[OPEN] - mi) / dif) * height
            ),
            (
                i * (candle_width) + candle_width - 1,
                (1 - (info[CLOSE] - mi) / dif) * height
            )
        )
        draw.rectangle(rect, ((100, 255, 150) if info[OPEN] < info[CLOSE] else (255, 100, 100)))

    # image.show()
    return image, mi, ma


def create_graph(data, candle_width=10, ma7=None, ma30=None, ma60=None):

    data_min = min([min(i[:-1]) for d, i in data])
    data_max = max([max(i[:-1]) for d, i in data])

    mi, ma = data_min - ((data_max - data_min) / 20), data_max + ((data_max - data_min) / 20)
    # ma = data_max
    # mi = data_min

    dif = ma - mi

    width = int(ceil(len(data) * (candle_width)))

    print(width, len(data), candle_width)
    
    # height = int((data_max - data_min) * 100)
    # print('----')
    # print(dif)
    # if dif > 20:
    #     height = int(dif / .01)
    # else:
    #     height = int(dif / .001)
    # print(height)

    height = 8000
    
    image = Image.new("RGBA", (width, height), (25, 25, 25))
    indicators_image = Image.new("RGBA", (width*5, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw_indicators = ImageDraw.Draw(indicators_image)

    for i, (d, info) in enumerate(data):
        
        # Indicators

        if i > 0:
            if ma7 is not None:
                last_avg = np.mean([inf[CLOSE] for dat, inf in data[i-7: i]])
                avg = np.mean([inf[CLOSE] for dat, inf in data[i-6: i+1]])
                # draw.line([((i-1) * (candle_width) + 3, (1 - (last_avg - mi) / dif) * height), (i * (candle_width) + 3, (1 - (avg - mi) / dif) * height)], fill=f"rgba{ma7}")
                draw_indicators.line([(((i-1) * (candle_width) + 3) * 5, (1 - (last_avg - mi) / dif) * height), ((i * (candle_width) + 3) * 5, (1 - (avg - mi) / dif) * height)], fill=f"rgba{ma7}")
            if ma30 is not None:
                last_avg = np.mean([inf[CLOSE] for dat, inf in data[i-30: i]])
                avg = np.mean([inf[CLOSE] for dat, inf in data[i-29: i+1]])
                # draw.line([((i-1) * (candle_width) + 3, (1 - (last_avg - mi) / dif) * height), (i * (candle_width) + 3, (1 - (avg - mi) / dif) * height)], fill=f"rgba{ma30}")
                draw_indicators.line([(((i-1) * (candle_width) + 3) * 5, (1 - (last_avg - mi) / dif) * height), ((i * (candle_width) + 3) * 5, (1 - (avg - mi) / dif) * height)], fill=f"rgba{ma30}")
            if ma60 is not None:
                last_avg = np.mean([inf[CLOSE] for dat, inf in data[i-60: i]])
                avg = np.mean([inf[CLOSE] for dat, inf in data[i-59: i+1]])
                # draw.line([((i-1) * (candle_width) + 3, (1 - (last_avg - mi) / dif) * height), (i * (candle_width) + 3, (1 - (avg - mi) / dif) * height)], fill=f"rgba{ma60}")
                draw_indicators.line([(((i-1) * (candle_width) + 3) * 5, (1 - (last_avg - mi) / dif) * height), ((i * (candle_width) + 3) * 5, (1 - (avg - mi) / dif) * height)], fill=f"rgba{ma60}")


        # Candles

        rect = (
            (
                i * (candle_width) + 1,
                (1 - (info[HIGH] - mi) / dif) * height
            ),
            (
                i * (candle_width) + candle_width - 2,
                (1 - (info[LOW] - mi) / dif) * height
            )
        )
        draw.rectangle(rect, (150, 150, 150, 128))

        rect = (
            (
                i * (candle_width),
                (1 - (info[OPEN] - mi) / dif) * height
            ),
            (
                i * (candle_width) + candle_width - 1,
                (1 - (info[CLOSE] - mi) / dif) * height
            )
        )

        draw.rectangle(rect, ((100, 255, 150) if info[OPEN] < info[CLOSE] else (255, 100, 100)))

    # image.show()
    return image, indicators_image, mi, ma



def create_blank_cursor():
    pixmap = QPixmap(1, 1)
    pixmap.fill(Qt.transparent)
    cursor = QCursor(pixmap)
    return cursor


def compare_dates(d1, d2):
    # print(d1[:4], d1[5:7], d1[8:10], d1[11:13], d1[14:16], d1[17:19])
    if int(d1[:4]) == int(d2[:4]):
        if int(d1[5:7]) == int(d2[5:7]):
            if int(d1[8:10]) == int(d2[8:10]):
                if int(d1[11:13]) == int(d2[11:13]):
                    if int(d1[14:16]) == int(d2[14:16]):
                        if int(d1[17:19]) == int(d2[17:19]):
                            return -1
                        elif int(d1[17:19]) > int(d2[17:19]):
                            return 0
                        else:
                            return 1
                    elif int(d1[14:16]) > int(d2[14:16]):
                        return 0
                    else:
                        return 1
                elif int(d1[11:13]) > int(d2[11:13]):
                    return 0
                else:
                    return 1
            elif int(d1[8:10]) > int(d2[8:10]):
                return 0
            else:
                return 1
        elif int(d1[5:7]) > int(d2[5:7]):
            return 0
        else:
            return 1
    elif int(d1[:4]) > int(d2[:4]):
        return 0
    else:
        return 1



class PaddedItemDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        option_copy = QStyleOptionViewItem(option)
        self.initStyleOption(option_copy, index)
        widget = option.widget

        # Customize the appearance of the item
        painter.save()
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, QColor(50, 50, 50))
        else:
            painter.fillRect(option.rect, option.palette.base())

        painter.setPen(QColor(255, 255, 255))

        text_rect = option.rect.adjusted(10, 0, -10, 0)  # Adjusted for padding
        painter.drawText(text_rect, Qt.AlignCenter, index.data())
        painter.restore()

    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        # Add padding to the size of each item
        size.setHeight(size.height() + 2)  # Add 10 pixels of padding to the height
        return size


class NoAnimationStyle(QProxyStyle):
    def pixelMetric(self, metric, option=None, widget=None):
        if metric == QStyle.PM_MenuButtonIndicator:
            return 1  # Set a very small value to remove the animation
        return super().pixelMetric(metric, option, widget)


class ChartPopup(QWidget):
    def __init__(self, ticker, date, width=800, height=600, candle_width=3):
        super().__init__()
        self.setWindowTitle("Chart")
        self.setGeometry(100, 100, width, height)
        self.setMouseTracking(True)
        self.setCursor(create_blank_cursor())
        self.bg_color = 'rgb(25, 25, 25)'
        self.setStyleSheet(f'background-color: {self.bg_color}')

        self.step_counter = 0
        self.cur_image = None
        self.ind_image = None

        self.start = True  # Used for setting last_index
        self.stored_price_lines = []
        self.stored_diagonal_lines = []
        self.current_diagonal = None
        self.candle_width = candle_width
        self.ticker = ticker
        self.date = date
        self.interval = '1m'

        # Indicators
        self.ma7 = None
        self.ma30 = None
        self.ma60 = None

        self.ma7C = '(50, 50, 100, 255)'
        self.ma30C = '(50, 100, 50, 255)'
        self.ma60C = '(100, 50, 50, 255)'

        self.last_mouse_pos = None

        # Make Menu Bar
        if True:
            self.change_interval_dd = QComboBox(self)
            self.change_interval_dd.setObjectName('change_interval_dd')
            self.change_interval_dd.setGeometry(int(self.width()/2) - 85, self.height() - 40, 100, 30)
            self.change_interval_dd.setCursor(Qt.ArrowCursor)
            # self.change_interval_dd.setStyle(NoAnimationStyle())
            
            self.change_interval_dd.addItem('1 minute')
            self.change_interval_dd.addItem('2 minute')
            self.change_interval_dd.addItem('5 minute')
            self.change_interval_dd.addItem('15 minute')
            self.change_interval_dd.addItem('30 minute')
            self.change_interval_dd.addItem('1 hour (lag)')
            self.change_interval_dd.addItem('1 day (lag)')
            self.change_interval_dd.addItem('1 week')
            
            padded_dg = PaddedItemDelegate()
            self.change_interval_dd.setItemDelegate(padded_dg)
            self.change_interval_dd.setStyleSheet(
                '''
                QComboBox {
                    border: 0px solid white;
                    color: white;
                    padding: 5px;
                    background-color: rgb(50, 50, 50);
                }

                QComboBox::drop-down {
                    border: none;
                }
                
                '''
            )
            
            self.change_interval_button = QPushButton(self)
            self.change_interval_button.setObjectName('change_interval_button')
            self.change_interval_button.clicked.connect(self.change_interval)
            self.change_interval_button.setGeometry(int(self.width()/2) + 35, self.height() - 40, 50, 30)
            self.change_interval_button.setCursor(Qt.ArrowCursor)
            self.change_interval_button.setText('Set')
            self.change_interval_button.setStyleSheet(
                '''
                border: 1px solid white;
                color: white;
                '''
            )

            self.grabbing_data_label = QLabel(self)
            self.grabbing_data_label.setObjectName('grabbing_data_label')
            self.grabbing_data_label.setGeometry(0, 0, self.width(), self.height())
            self.grabbing_data_label.setText('Grabbing Data...')
            self.grabbing_data_label.setAlignment(Qt.AlignCenter)
            self.grabbing_data_label.setCursor(Qt.ArrowCursor)
            self.grabbing_data_label.setStyleSheet(
                '''
                QLabel {
                    color: white;
                    background-color: rgba(50, 50, 50, .8);
                    font-size: 20px;
                }
                '''
            )
            self.grabbing_data_label.hide()


        # Chart Settings Frame
        if True:
            self.settings_frame = QFrame(self)
            self.settings_frame.setObjectName('settings_frame')
            self.settings_frame.setGeometry(int(self.width()/2) - 100, int(self.height()/2 - 150), 200, 300)
            self.settings_frame.setCursor(Qt.ArrowCursor)
            self.settings_frame.setStyleSheet(
                '''
                background-color: rgba(0, 0, 0, .8);
                '''
            )
            self.settings_shown = False
            self.settings_frame.hide()
            
            # Button to open settings
            self.settings_button = QPushButton(self)
            self.settings_button.setObjectName('settings_button')
            self.settings_button.setGeometry(0, 0, 60, 30)
            self.settings_button.setCursor(Qt.ArrowCursor)
            self.settings_button.setText('Settings')
            self.settings_button.setStyleSheet(
                '''
                QPushButton {
                    background-color: rgba(50, 50, 50, .5);
                    color: white;
                    border: 1px solid rgba(75, 75, 75, .9);
                }

                QPushButton:hover {
                    background-color: rgba(75, 75, 75, .9);
                    border: 1px solid rgba(75, 75, 75, .9);
                }

                QPushButton:pressed {
                    background-color: rgb(150, 150, 150);
                    border: 1px solid rgb(150, 150, 150);
                }
                '''
            )
            self.settings_button.clicked.connect(self.settings_button_clicked)

            self.set_indicators_button = QPushButton()
            self.set_indicators_button.setObjectName('set_indicators_button')
            self.set_indicators_button.setText('Update')
            self.set_indicators_button.setStyleSheet(
                '''
                background-color: transparent;
                border: 1px solid rgb(200, 200, 200);
                color: rgb(200, 200, 200);
                '''
            )
            self.set_indicators_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            self.set_indicators_button.setFixedSize(100, 30)
            self.set_indicators_button.clicked.connect(self.update_indicators)

            self.settings_layout = QVBoxLayout(self.settings_frame)

            self.ma7_button = QPushButton()
            self.ma7_button.setObjectName('ma7_button:off')
            self.ma7_button.setText('7 Period MA')
            self.ma7_button.setStyleSheet(
                '''
                background-color: transparent;
                border: 1px solid rgb(75, 75, 75);
                color: rgb(75, 75, 75);
                '''
            )
            self.ma7_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            self.ma7_button.setFixedSize(100, 30)
            self.ma7_button.clicked.connect(lambda: self.setIndicator(self.ma7_button))


            self.ma30_button = QPushButton()
            self.ma30_button.setObjectName('ma30_button:off')
            self.ma30_button.setText('30 Period MA')
            self.ma30_button.setStyleSheet(
                '''
                background-color: transparent;
                border: 1px solid rgb(75, 75, 75);
                color: rgb(75, 75, 75);
                '''
            )
            self.ma30_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            self.ma30_button.setFixedSize(100, 30)
            self.ma30_button.clicked.connect(lambda: self.setIndicator(self.ma30_button))


            self.ma60_button = QPushButton()
            self.ma60_button.setObjectName('ma60_button:off')
            self.ma60_button.setText('60 Period MA')
            self.ma60_button.setStyleSheet(
                '''
                background-color: transparent;
                border: 1px solid rgb(75, 75, 75);
                color: rgb(75, 75, 75);
                '''
            )
            self.ma60_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            self.ma60_button.setFixedSize(100, 30)
            self.ma60_button.clicked.connect(lambda: self.setIndicator(self.ma60_button))

            self.settings_layout.setAlignment(Qt.AlignHCenter)
            self.settings_layout.addWidget(self.ma7_button)
            self.settings_layout.addWidget(self.ma30_button)
            self.settings_layout.addWidget(self.ma60_button)
            
            self.settings_layout.addWidget(self.set_indicators_button)

        self.change_interval()

        self.timer = QTimer()
        self.timer.timeout.connect(self.up)
        self.timer.start(5)

    def set_data(self):
        self.data = get_data_date(self.ticker, self.date, self.interval)

        if len(self.data) > 0:
            if self.start:
                self.last_index = len(self.data)-390  # 390
                self.end = self.data[self.last_index][0]
                self.start = False
            else:
                self.last_index = len(self.data)-2
                
                if self.interval == '1m':
                    for i in range(0, len(self.data)):
                        if compare_dates(self.data[i][0], self.end) == -1:
                            self.last_index = i
                            break
                else:
                    for i in range(0, len(self.data)):
                        if compare_dates(self.data[i][0], self.end) == 0:
                            self.last_index = max(i-2, 0)
                            break
            
            # self.w = width
            # self.h = height

            print('-- Stop At --')
            print(self.last_index, len(self.data))
            print(self.data[self.last_index])

            if len(self.data) > 0:
                image_data, indicator_image, mi, ma = create_graph(self.data, candle_width=self.candle_width, ma7=self.ma7, ma30=self.ma30, ma60=self.ma60)
                self.mi = mi
                self.ma = ma
                self.dif = self.ma - self.mi
                # image_data.show()
                self.image_w = image_data.width
                self.image_h = image_data.height
                self.indicator_image_w = indicator_image.width
                self.indicator_image_h = indicator_image.height

                self.rawraw_image = ImageQt.ImageQt(image_data)
                self.rawraw_indicator_image = ImageQt.ImageQt(indicator_image)

                self.raw_image = self.rawraw_image.copy(QRect(0, 0, (self.last_index*self.candle_width)+self.candle_width, self.rawraw_image.height()))
                self.raw_indicator_image = self.rawraw_indicator_image.copy(QRect(0, 0, ((self.last_index*self.candle_width)+self.candle_width) * 5, self.rawraw_indicator_image.height()))
                
                self.cur_image = self.raw_image
                self.cur_indicator_image = self.raw_indicator_image

                self.image = self.cur_image
                self.indicator_image = self.cur_indicator_image
                
                self.mouse_pos = (0, 0)
                self.zoom_amt = 1
                self.zoom_int = .0005
                self.zoom_min = .05
                self.zoom_max = 1

                self.offset = [0, 0]
                self.zoom(0)
                self.grabbing_data_label.hide()
                return True
            else:
                self.grabbing_data_label.hide()
                return False

    def update_indicators(self):
        image_data, indicator_image, mi, ma = create_graph(self.data, candle_width=self.candle_width, ma7=self.ma7, ma30=self.ma30, ma60=self.ma60)
        # self.rawraw_image = ImageQt.ImageQt(image_data)
        # self.raw_image = self.rawraw_image.copy(QRect(0, 0, (self.last_index*self.candle_width)+self.candle_width, self.rawraw_image.height()))
        # self.cur_image = self.raw_image
        # self.image = self.cur_image

        self.image_w = image_data.width
        self.image_h = image_data.height
        self.indicator_image_w = indicator_image.width
        self.indicator_image_h = indicator_image.height

        self.rawraw_image = ImageQt.ImageQt(image_data)
        self.rawraw_indicator_image = ImageQt.ImageQt(indicator_image)

        self.raw_image = self.rawraw_image.copy(QRect(0, 0, (self.last_index*self.candle_width)+self.candle_width, self.rawraw_image.height()))
        self.raw_indicator_image = self.rawraw_indicator_image.copy(QRect(0, 0, ((self.last_index*self.candle_width)+self.candle_width) * 5, self.rawraw_indicator_image.height()))

        self.cur_image = self.raw_image
        self.cur_indicator_image = self.raw_indicator_image

        self.image = self.cur_image
        self.indicator_image = self.cur_indicator_image

        self.settings_frame.hide()
        self.settings_button.show()
        self.settings_shown = False

    def get_progress(self):
        return self.step_counter

    def step(self):
        if self.interval == '1m':
            self.last_index += 1
            if self.last_index == len(self.data):
                self.last_index -= 1
                return True
            else:
                self.step_counter += 1
            print('last_index', self.data[self.last_index][1])
            self.end = self.data[self.last_index][0]
            self.raw_image = self.rawraw_image.copy(QRect(0, 0, (self.last_index*self.candle_width)+self.candle_width, self.rawraw_image.height()))
            self.raw_indicator_image = self.rawraw_indicator_image.copy(QRect(0, 0, ((self.last_index*self.candle_width)+self.candle_width) * 5, self.rawraw_indicator_image.height()))

            self.zoom(0)
        else:
            pass
        return False

    def setIndicator(self, b: QPushButton):
        name, status = b.objectName().split(':')
        
        if status == 'off':
            c = '(200, 200, 200, 255)'
            if name == 'ma7_button':
                self.ma7 = self.ma7C
                c = self.ma7C
            elif name == 'ma30_button':
                self.ma30 = self.ma30C
                c = self.ma30C
            elif name == 'ma60_button':
                self.ma60 = self.ma60C
                c = self.ma60C
            c = c[:c.rfind(',')] + ')'
            b.setStyleSheet(
                f'''
                background-color: transparent;
                border: 1px solid rgb{c};
                color: rgb{c};
                '''
            )
            b.setObjectName(name + ':on')
        else:
            b.setStyleSheet(
                '''
                background-color: transparent;
                border: 1px solid rgb(75, 75, 75);
                color: rgb(75, 75, 75);
                '''
            )
            b.setObjectName(name + ':off')
            if name == 'ma7_button':
                self.ma7 = None
            elif name == 'ma30_button':
                self.ma30 = None
            elif name == 'ma60_button':
                self.ma60 = None

    def settings_button_clicked(self):
        if self.settings_shown:
            self.settings_frame.hide()
            self.settings_shown = False
            self.setCursor(create_blank_cursor())
        else:
            self.settings_button.hide()
            self.settings_frame.setGeometry(int(self.width()/2) - 100, int(self.height()/2 - 150), 200, 300)
            self.settings_frame.show()

            self.settings_shown = True
            self.setCursor(Qt.ArrowCursor)

    def change_interval(self):
        if not self.settings_shown:
            interval = self.change_interval_dd.itemText(self.change_interval_dd.currentIndex())
            if interval == '1 minute':
                self.interval = '1m'
            elif interval == '2 minute':
                self.interval = '2m'
            elif interval == '5 minute':
                self.interval = '5m'
            elif interval == '15 minute':
                self.interval = '15m'
            elif interval == '30 minute':
                self.interval = '30m'
            elif interval == '1 hour (lag)':
                self.interval = '1h'
            elif interval == '1 day (lag)':
                self.interval = '1d'
            elif interval == '1 week':
                self.interval = '1wk'
            self.grabbing_data_label.show()
            QTimer.singleShot(1, self.set_data)

    def get_ms(self):
        off_per = self.offset[1] + 1

        mi = (off_per - self.zoom_amt)/2 * self.dif
        ma = mi + self.zoom_amt * self.dif

        mi = self.mi + mi
        ma = self.mi + ma

        dif = ma - mi
        return mi, ma, dif

    def get_msX(self):
        off_per = -self.offset[0] + 1

        mi = (off_per - self.zoom_amt)/2 * len(self.data)
        ma = mi + self.zoom_amt * len(self.data)

        dif = ma - mi
        return mi, ma, dif

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.cur_image is not None and not self.cur_image.isNull():
            # Draw the QImage
            painter.drawImage(0, 0, self.image)
            painter.drawImage(0, 0, self.indicator_image)

            # Price Grid
            mi, ma, dif = self.get_ms()

            lines = 8

            for i in range(1, lines):
                line = i / lines * dif + mi
                painter.setPen(QColor(255, 255, 255, 10))
                painter.drawLine(0, self.height() - int(i / lines * self.height()), self.width(), self.height() - int(i / lines * self.height()))
                painter.setFont(QFont('Arial', 6 + int(self.height() / 200)))
                painter.setPen(QColor(255, 255, 255, 150))
                painter.drawText(self.width() - 75, self.height() - int(i / lines * self.height()) - 10, f'${line:.2f}')
        
            for pl in self.stored_price_lines:
                if mi < pl < ma:
                    painter.setPen(QColor(255, 0, 0, 200))
                    painter.drawLine(0, self.height() - int((pl - mi) / dif * self.height()), self.width(), self.height() - int((pl - mi) / dif * self.height()))
                    painter.setFont(QFont('Arial', 6 + int(self.height() / 200)))
                    painter.setPen(QColor(255, 0, 0, 255))
                    painter.drawText(self.width() - 75, self.height() - int((pl - mi) / dif * self.height()) - 10, f'${pl:.2f}')
            
            miX, maX, difX = self.get_msX()

            for i in self.stored_diagonal_lines:
                if miX <= i[0][0] <= maX or miX <= i[1][0] <= maX:
                    painter.setPen(QColor(75, 75, 150))
                    painter.drawLine(int((i[0][0] - miX) / difX * self.width()), self.height() - int((i[0][1] - mi) / dif * self.height()), int((i[1][0] - miX) / difX * self.width()), self.height() - int((i[1][1] - mi) / dif * self.height()))
            
            if not self.settings_shown:
                if self.current_diagonal is not None:
                    size = int(min(self.height(), self.width()) / 40)
                    painter.setPen(QColor(75, 75, 150))
                    painter.drawEllipse(int( (self.current_diagonal[0] - miX) / difX * self.width() ) - int(size/2), self.height() - int( (self.current_diagonal[1] - mi) / dif * self.height() ) - int(size/2), size, size)
                    painter.drawLine(int( (self.current_diagonal[0] - miX) / difX * self.width() ), self.height() - int( (self.current_diagonal[1] - mi) / dif * self.height() ), self.mouse_pos[0], self.mouse_pos[1])


                painter.setPen(QColor(100, 100, 100))
                painter.drawLine(self.mouse_pos[0], 0, self.mouse_pos[0], self.height())
                painter.drawLine(0, self.mouse_pos[1], self.width(), self.mouse_pos[1])

                painter.setFont(QFont('Arial', 6 + int(self.height() / 200)))
                painter.setPen(QColor(255, 255, 255, 150))
                painter.drawText(self.width() - 75, self.mouse_pos[1] - 10, f'${((self.height() - self.mouse_pos[1])/self.height()) * dif + mi:.2f}')

    def up(self):
        # pixels = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(400 * 300)]
        # self.image.putdata(pixels)
        if self.cur_image is not None and not self.cur_image.isNull():
            self.image = self.cur_image.scaled(self.width(), self.height())
            self.indicator_image = self.cur_indicator_image.scaled(self.width(), self.height())
            self.change_interval_dd.setGeometry(int(self.width()/2) - 85, self.height() - 40, 100, 30)
            self.change_interval_button.setGeometry(int(self.width()/2) + 35, self.height() - 40, 50, 30)
            self.grabbing_data_label.setGeometry(0, 0, self.width(), self.height())
            self.update()
    
    def zoom(self, amt):
        self.zoom_amt += self.zoom_int * -amt
        self.zoom_amt = min(self.zoom_max, self.zoom_amt)
        self.zoom_amt = max(self.zoom_min, self.zoom_amt)
        
        if self.offset[0] > 1 - self.zoom_amt:
            self.offset[0] = 1 - self.zoom_amt
        elif self.offset[0] * -1 > 1 - self.zoom_amt:
            self.offset[0] = (1 - self.zoom_amt) * -1
        
        if self.offset[1] > 1 - self.zoom_amt:
            self.offset[1] = 1 - self.zoom_amt
        elif self.offset[1] * -1 > 1 - self.zoom_amt:
            self.offset[1] = (1 - self.zoom_amt) * -1

        new_w = self.zoom_amt * self.image_w
        new_h = self.zoom_amt * self.image_h

        new_w_i = self.zoom_amt * self.indicator_image_w
        new_h_i = self.zoom_amt * self.indicator_image_h

        crop_rect = QRect(
            int((self.image_w - new_w)/2) + -int(self.offset[0] * self.image_w / 2),
            int((self.image_h - new_h)/2) + -int(self.offset[1] * self.image_h / 2),
            int(new_w),
            int(new_h)
        )

        crop_rect_i = QRect(
            int((self.indicator_image_w - new_w_i)/2) + -int(self.offset[0] * self.indicator_image_w / 2),
            int((self.indicator_image_h - new_h_i)/2) + -int(self.offset[1] * self.indicator_image_h / 2),
            int(new_w_i),
            int(new_h_i)
        )
        
        self.cur_image = self.raw_image.copy(crop_rect)
        self.cur_indicator_image = self.raw_indicator_image.copy(crop_rect_i)
    
    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        if not self.settings_shown:
            delta = event.angleDelta().y()

            self.zoom(delta)
    
    def mouseMoveEvent(self, event):
        # print('hello')
        self.mouse_pos = (event.x(), event.y())

        if event.buttons() == Qt.LeftButton and not self.settings_shown:
            if self.last_mouse_pos == None:
                self.last_mouse_pos = event.pos()
            delta = event.pos() - self.last_mouse_pos
            # print('delta', delta, 'zoom_amt', self.zoom_amt)
            self.offset[0] += delta.x() / self.width() * self.zoom_amt
            self.offset[1] += delta.y() / self.height() * self.zoom_amt

            if self.offset[0] > 1 - self.zoom_amt:
                self.offset[0] = 1 - self.zoom_amt
            elif self.offset[0] * -1 > 1 - self.zoom_amt:
                self.offset[0] = (1 - self.zoom_amt) * -1
            
            if self.offset[1] > 1 - self.zoom_amt:
                self.offset[1] = 1 - self.zoom_amt
            elif self.offset[1] * -1 > 1 - self.zoom_amt:
                self.offset[1] = (1 - self.zoom_amt) * -1
            
            self.zoom(0)
        
        self.last_mouse_pos = event.pos()
    
    def mousePressEvent(self, event):
        if not self.settings_shown and event.button() == Qt.RightButton:
            if event.modifiers() and Qt.ControlModifier:
                ind = event.pos().x() / self.width()
                # print(ind * len(self.data), len(self.data))

                mi, ma, dif = self.get_msX()
                ind = int(ind*dif + mi)
                # print(ind)
                # print(self.data[ind])

                perc = 1 - event.pos().y() / self.height()
                mi, ma, dif = self.get_ms()

                line = perc * dif + mi

                if self.current_diagonal is None:
                    self.current_diagonal = [ind, line]
                else:
                    self.stored_diagonal_lines.append([self.current_diagonal, [ind, line]])
                    self.current_diagonal = None
            else:
                perc = 1 - event.pos().y() / self.height()
                mi, ma, dif = self.get_ms()

                line = perc * dif + mi

                exists = False
                for pl in self.stored_price_lines:
                    if abs((pl-mi) - (line-mi)) / dif <= .01:
                        exists = True
                        self.stored_price_lines.remove(pl)
                        break

                if not exists:
                    self.stored_price_lines.append(line)

        else:
            super().mousePressEvent(event)




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    data = json.load(open('aapl.json', 'r+'))
    view = ChartPopup(data)
    view.setGeometry(190, 100, 800, 600)
    view.show()

    sys.exit(app.exec_())