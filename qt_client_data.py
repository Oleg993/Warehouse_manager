from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from Db_functions import DataBase
from datetime import datetime
from Documents.create_documents import files_sell


class Ui_Client_data(object):
    def __init__(self, cart_class, user, goods_in_cart, all_price):
        self.db = sqlite3.connect('Warehouses_db.db')
        self.cursor = self.db.cursor()
        self.cart_class = cart_class
        self.current_user = user
        self.goods_in_order = goods_in_cart
        self.price = all_price
        self.client = None
        self.address = None

    def setupUi(self, Client_data):
        Client_data.setObjectName("Client_data_and_address")
        Client_data.resize(400, 250)
        self.lineEdit_client = QtWidgets.QLineEdit(Client_data)
        self.lineEdit_client.setGeometry(QtCore.QRect(20, 50, 360, 30))
        self.lineEdit_client.setFrame(False)
        self.lineEdit_client.setObjectName("lineEdit_client")
        self.lineEdit_address = QtWidgets.QLineEdit(Client_data)
        self.lineEdit_address.setGeometry(QtCore.QRect(20, 140, 360, 30))
        self.lineEdit_address.setFrame(False)
        self.lineEdit_address.setObjectName("lineEdit_address")
        self.layoutWidget = QtWidgets.QWidget(Client_data)
        self.layoutWidget.setGeometry(QtCore.QRect(60, 210, 280, 25))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_take_data = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_take_data.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_take_data.setObjectName("btn_take_data")
        self.horizontalLayout.addWidget(self.btn_take_data)
        self.btn_cancel = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_cancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout.addWidget(self.btn_cancel)
        self.comboBox_client = QtWidgets.QComboBox(Client_data)
        self.comboBox_client.setGeometry(QtCore.QRect(20, 20, 360, 20))
        self.comboBox_client.setObjectName("comboBox_client")
        self.comboBox_address = QtWidgets.QComboBox(Client_data)
        self.comboBox_address.setGeometry(QtCore.QRect(20, 110, 360, 20))
        self.comboBox_address.setObjectName("comboBox_address")
        self.widget = QtWidgets.QWidget(Client_data)
        self.widget.setGeometry(QtCore.QRect(20, 180, 266, 20))
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_documents = QtWidgets.QLabel(self.widget)
        self.label_documents.setObjectName("label_documents")
        self.horizontalLayout_2.addWidget(self.label_documents)
        self.radioButton_Yes = QtWidgets.QRadioButton(self.widget)
        self.radioButton_Yes.setChecked(True)
        self.radioButton_Yes.setObjectName("radioButton_Yes")
        self.horizontalLayout_2.addWidget(self.radioButton_Yes)
        self.radioButton_No = QtWidgets.QRadioButton(self.widget)
        self.radioButton_No.setObjectName("radioButton_No")
        self.horizontalLayout_2.addWidget(self.radioButton_No)

        # При запуске:
        # присваиваем значение выбранное в комбобоксе строке для воода значения (клиент и адрес)
        # получаем список ранее сохраненныъ компаний и адресов
        # отображаем корзину при закрытии текущего окна
        self.comboBox_client.currentIndexChanged.connect(self.combo_box_client)
        self.comboBox_address.currentIndexChanged.connect(self.combo_box_address)
        self.get_companies_list()
        Client_data.closeEvent = self.close_window

        self.retranslateUi(Client_data)
        QtCore.QMetaObject.connectSlotsByName(Client_data)

    def retranslateUi(self, Client_data):
        _translate = QtCore.QCoreApplication.translate
        Client_data.setWindowTitle(_translate("Client_data_and_address", "Данные клиента"))
        self.lineEdit_client.setPlaceholderText(_translate("Client_data_and_address", "Введите данные заказчика"))
        self.lineEdit_address.setPlaceholderText(_translate("Client_data_and_address", "Введите адрес доставки (Город, улица, дом, почтовый индекс)"))
        self.btn_take_data.setText(_translate("Client_data_and_address", "Принять"))
        self.btn_cancel.setText(_translate("Client_data_and_address", "Отмена"))
        self.label_documents.setText(_translate("Client_data_and_address", "Создавать документы Word/Excel"))
        self.radioButton_Yes.setText(_translate("Client_data_and_address", "Да"))
        self.radioButton_No.setText(_translate("Client_data_and_address", "Нет"))
        self.btn_take_data.clicked.connect(self.get_data)
        self.btn_cancel.clicked.connect(self.close_window)

    # получаем данные по клиенту, адресу
    # доавляем заказ в таблицу Orders, Goods_in_order, Companies(опциаонально, если ранее нет в таблице)
    def get_data(self):
        client_data = self.lineEdit_client.text().strip()
        address_data = self.lineEdit_address.text().strip()

        if not client_data:
            QtWidgets.QMessageBox.information(self.layoutWidget, 'Ошибка', 'Введите данные клиента!')
            return

        if not address_data:
            QtWidgets.QMessageBox.information(self.layoutWidget, 'Ошибка', 'Введите адрес!')
            return

        self.client = client_data
        self.address = address_data

        goods = [[int(i[0]), int(i[1])] for i in self.goods_in_order]

        info_for_list = []
        for good in goods:
            self.cursor.execute("""SELECT Warehouses.warehouse_name, good_name, measure_unit, description 
                                  FROM Goods 
                                  JOIN Warehouses ON Goods.warehouse_id = Warehouses.id
                                  WHERE article_number = ?""", [good[0]])
            info_for_list.append(list(self.cursor.fetchone()))

        current_date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        goods_list_sell = [elem + good for elem, good in zip(info_for_list, goods)]

        list_sell = {'article_number': ', '.join(str(i[-2]) for i in goods_list_sell),
                     'good_name': ', '.join(str(i[1]) for i in goods_list_sell),
                     'warehouse_address': ', '.join(str(i[0]) for i in goods_list_sell),
                     'delivery_address': address_data,
                     'date': current_date,
                     'measure_unit': ', '.join(str(i[2]) for i in goods_list_sell),
                     'description': ', '.join(str(i[3]) for i in goods_list_sell),
                     'amount': ', '.join(str(i[-1]) for i in goods_list_sell),
                     'price_sell': self.price}
        self.cart_class.clear_cart()
        if self.radioButton_Yes.isChecked():
            paths = files_sell(list_sell)
            DataBase().add_new_order_into_bd_orders_and_good_in_orders(self.current_user, self.client, self.address, goods, paths)
        else:
            DataBase().add_new_order_into_bd_orders_and_good_in_orders(self.current_user, self.client, self.address, goods)
        QtWidgets.QMessageBox.information(self.layoutWidget, 'Информация', 'Заказ принят!')
        self.close_window()

    def get_companies_list(self):
        self.comboBox_client.clear()
        companies = ["Вписать данные самостоятельно"]
        companies_db = DataBase().get_all_companies()
        companies += [i[1] for i in companies_db]
        for company in companies:
            self.comboBox_client.addItem(company)

        addresses = ["Вписать адрес самостоятельно"]
        addresses += [i[2] for i in companies_db]
        for address in addresses:
            self.comboBox_address.addItem(address)

    # получаем введенные или выбранные данные Клиента
    def combo_box_client(self, index_client):
        if index_client == 0:
            self.lineEdit_client.clear()
            self.lineEdit_client.setEnabled(True)
            self.client = self.lineEdit_client.text()
        else:
            self.client = self.comboBox_client.currentText()
            self.lineEdit_client.setText(self.client)
            self.lineEdit_client.setEnabled(False)

    # получаем введенные или выбранные данные Адреса
    def combo_box_address(self, index_address):
        if index_address == 0:
            self.lineEdit_address.clear()
            self.lineEdit_address.setEnabled(True)
            self.address = self.lineEdit_address.text()
        else:
            self.address = self.comboBox_address.currentText()
            self.lineEdit_address.setText(self.address)
            self.lineEdit_address.setEnabled(False)

    # отображаем корзину при закрытии текущего окна
    def close_window(self, event=None):
        self.client = None
        self.address = None
        if not event:
            QtWidgets.QApplication.activeWindow().close()
        else:
            self.cart_class.current_window.show()
            event.accept()
