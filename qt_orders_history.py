import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from Db_functions import DataBase
from PyQt5.QtWidgets import QPushButton, QWidget
from os import startfile
from functools import partial


class Ui_Orders_History(object):
    def __init__(self, user):
        self.current_user = user
        self.flag = False
        self.flag_search = False

    def setupUi(self, Orders_History):
        Orders_History.setObjectName("Orders_History")
        Orders_History.resize(600, 320)
        self.tableWidget_table_history = QtWidgets.QTableWidget(Orders_History)
        self.tableWidget_table_history.setGeometry(QtCore.QRect(20, 60, 560, 240))
        self.tableWidget_table_history.setObjectName("tableWidget_table_history")
        self.comboBox = QtWidgets.QComboBox(Orders_History)
        self.comboBox.setGeometry(QtCore.QRect(20, 30, 91, 21))
        self.comboBox.setObjectName("comboBox")
        self.comboBox_2 = QtWidgets.QComboBox(Orders_History)
        self.comboBox_2.setGeometry(QtCore.QRect(120, 30, 91, 21))
        self.comboBox_2.setObjectName("comboBox_2")
        self.lineEdit = QtWidgets.QLineEdit(Orders_History)
        self.lineEdit.setGeometry(QtCore.QRect(370, 20, 200, 30))
        self.lineEdit.setFrame(False)
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(Orders_History)
        self.label.setGeometry(QtCore.QRect(20, 10, 91, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Orders_History)
        self.label_2.setGeometry(QtCore.QRect(120, 10, 91, 16))
        self.lineEdit_2 = QtWidgets.QLineEdit(Orders_History)
        self.lineEdit_2.setGeometry(QtCore.QRect(220, 30, 41, 20))
        self.lineEdit_2.setObjectName("lineEdit")
        self.label_3 = QtWidgets.QLabel(Orders_History)
        self.label_3.setGeometry(QtCore.QRect(230, 10, 71, 16))
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(Orders_History)
        self.pushButton.setGeometry(QtCore.QRect(280, 20, 75, 31))
        self.pushButton.setObjectName("pushButton")

        self.tableWidget_table_history.horizontalHeader().sectionClicked.connect(self.sort_table)

        self.retranslateUi(Orders_History)
        QtCore.QMetaObject.connectSlotsByName(Orders_History)

        table_collums = ["№ Заказа", "Составитель ТТН", "Компания (заказчик)",
                         "Адрес доставки", "Дата оформления", "Word", "Excel", "Товары"]
        self.tableWidget_table_history.setColumnCount(len(table_collums))
        self.tableWidget_table_history.setHorizontalHeaderLabels(table_collums)
        self.fill_table()
        if self.flag_search is not False:
            self.flag_search = False

    def retranslateUi(self, Orders_History):
        _translate = QtCore.QCoreApplication.translate
        Orders_History.setWindowTitle(_translate("Orders_History", "История заказов"))
        self.lineEdit.setPlaceholderText(_translate("Orders_History", "Поиск..."))
        self.label.setText(_translate("old_orders", "Начальный месяц"))
        self.label_2.setText(_translate("old_orders", "Конечный месяц"))
        self.label_3.setText(_translate("old_orders", "Год"))
        self.pushButton.setText(_translate("old_orders", "Показать"))
        self.lineEdit_2.setText(str(datetime.datetime.now().year))
        self.pushButton.clicked.connect(partial(self.fill_table, old_orders=True))
        self.lineEdit.returnPressed.connect(self.search)

        global months
        months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
                  'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
        self.comboBox.addItems(months)
        self.comboBox_2.addItems(months)
        self.comboBox.currentTextChanged.connect(self.change_months)
    def change_months(self):
        self.comboBox_2.clear()
        self.comboBox_2.addItems(months[months.index(self.comboBox.currentText()):])

    def search(self):
        if self.flag_search:
            self.fill_table(old_orders=True)
        else:
            self.fill_table()

    # сортировака по столбикам
    def sort_table(self, column):
        if not self.flag or self.tableWidget_table_history.horizontalHeader().sortIndicatorSection() != column:
            self.tableWidget_table_history.sortItems(column, QtCore.Qt.AscendingOrder)
            self.flag = True
        else:
            self.tableWidget_table_history.sortItems(column, QtCore.Qt.DescendingOrder)
            self.flag = False

    def open_window_goods_info(self, order_id, old_orders=None):
        self.window_order_info = QWidget()
        self.window_order_info.setWindowTitle('Новое окно')
        self.window_order_info.setObjectName("Admin_panel")
        self.window_order_info.setWindowModality(QtCore.Qt.NonModal)
        self.tableWidget1 = QtWidgets.QTableWidget(self.window_order_info)
        self.tableWidget1.setGeometry(QtCore.QRect(20, 20, 335, 300))
        self.tableWidget1.setObjectName("tableView_data")
        self.window_order_info.resize(375, 335)
        self.window_order_info.show()
        self.window_order_info.setWindowTitle(QtCore.QCoreApplication.translate("window_order_info", "Товары заказа"))

        table_collums = ["Название", "Ед. изм.", "Количество"]
        self.tableWidget1.setColumnCount(len(table_collums))
        self.tableWidget1.setHorizontalHeaderLabels(table_collums)
        self.fill_table(order_id, old_orders)

    def input_file_button(self, row, coll, file_text, file_path):
        button = QPushButton()
        button.setText(file_text)
        button.clicked.connect(partial(startfile, file_path))
        self.tableWidget_table_history.setCellWidget(row, coll, button)

    def fill_table(self, order_id=None, old_orders=None):
        if order_id in (None, False):
            if old_orders:
                self.flag_search = True
            search_text = self.lineEdit.text().lower()

            if old_orders is None:
                info_for_search = DataBase().get_completed_orders()
            else:
                between = months[months.index(self.comboBox.currentText()):months.index(self.comboBox_2.currentText()) + 1]
                info_for_search = DataBase().get_old_orders(between, self.lineEdit_2.text())

            if search_text:
                info = []
                for i in info_for_search:
                    if i[2].lower() == search_text or search_text in i[2].lower() or search_text in i[1].lower():
                        info.append(i)
                if len(info) == 0:
                    QtWidgets.QMessageBox.information(self.tableWidget_table_history, 'Ошибка поиска', 'Данные не найдены!')
                    return
            else:
                info = info_for_search
            self.tableWidget_table_history.setRowCount(len(info))
            for row, str_info in enumerate(info):
                len_str = len(str_info)
                order_id = ""
                for coll, info_insert in enumerate(str_info):
                    if not order_id:
                        order_id = info_insert
                    if coll == len_str - 2:
                        if info_insert is not None and not info_insert == "-":
                            self.input_file_button(row, coll, "Word", info_insert)
                        else:
                            self.tableWidget_table_history.setItem(row, coll, QtWidgets.QTableWidgetItem("-"))
                    elif coll == len_str - 1:
                        if info_insert is not None and not info_insert == "-":
                            self.input_file_button(row, coll, "Excel", info_insert)
                        else:
                            self.tableWidget_table_history.setItem(row, coll, QtWidgets.QTableWidgetItem("-"))
                        button = QPushButton()
                        button.setText("Посмотреть")
                        button.clicked.connect(partial(self.open_window_goods_info, order_id, old_orders))
                        self.tableWidget_table_history.setCellWidget(row, coll + 1, button)
                    else:
                        self.tableWidget_table_history.setItem(row, coll, QtWidgets.QTableWidgetItem(str(info_insert)))
        else:
            if old_orders is None:
                info = DataBase().get_goods_info_from_order(order_id)
            else:
                between = months[months.index(self.comboBox.currentText()):months.index(self.comboBox_2.currentText()) + 1]
                info = DataBase().get_goods_info_from_old_orders(between, self.lineEdit_2.text(), order_id)

            if len(info) == 0:
                QtWidgets.QMessageBox.information(self.tableWidget1, 'Ошибка поиска', 'Данные не найдены!')
                return
            self.tableWidget1.setRowCount(len(info))
            for row, str_info in enumerate(info):
                for coll, info_insert in enumerate(str_info):
                    self.tableWidget1.setItem(row, coll, QtWidgets.QTableWidgetItem(str(info_insert)))

    def open_window(self, window):
        self.current_window = QtWidgets.QApplication.activeWindow()
        self.main_window = QtWidgets.QMainWindow()
        self.ui = window
        self.ui.setupUi(self.main_window)
        self.main_window.show()
        self.current_window.hide()
