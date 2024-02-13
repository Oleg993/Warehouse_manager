import sqlite3
from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets

import qt_client_data


class Ui_Cart(object):
    def __init__(self, make_order_class, user):
        self.db = sqlite3.connect('Warehouses_db.db')
        self.cursor = self.db.cursor()
        self.all_price = []
        self.make_order_class = make_order_class
        self.current_user = user
        self.current_window = None

    def setupUi(self, Cart):
        Cart.setObjectName("Cart")
        Cart.resize(460, 380)
        self.table_widget_cart = QtWidgets.QTableWidget(Cart)
        self.table_widget_cart.setGeometry(QtCore.QRect(20, 30, 417, 250))
        self.table_widget_cart.setObjectName("tableView")
        self.layoutWidget = QtWidgets.QWidget(Cart)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 330, 400, 25))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(17, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_cart_get_order = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_cart_get_order.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_cart_get_order.setObjectName("btn_cart_get_order")
        self.horizontalLayout.addWidget(self.btn_cart_get_order)
        self.btn_cart_delete = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_cart_delete.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_cart_delete.setObjectName("btn_cart_delete")
        self.horizontalLayout.addWidget(self.btn_cart_delete)
        self.btn_cart_clear = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_cart_clear.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_cart_clear.setObjectName("btn_cart_clear")
        self.horizontalLayout.addWidget(self.btn_cart_clear)
        self.label_all_rpice = QtWidgets.QLabel(Cart)
        self.label_all_rpice.setGeometry(QtCore.QRect(256, 290, 70, 20))
        self.label_all_rpice.setObjectName("label_all_rpice")
        self.lineEdit_sum = QtWidgets.QLineEdit(Cart)
        self.lineEdit_sum.setGeometry(QtCore.QRect(336, 290, 100, 20))
        self.lineEdit_sum.setFrame(False)
        self.lineEdit_sum.setObjectName("lineEdit")
        self.lineEdit_sum.setReadOnly(True)

        # При запуске:
        # отображаем содержимое корзины в таблице
        # отображаем окно Сделать заказ при закрытии Корзины
        # блокируем нажатие кнопок если корзина пустая
        self.show_cart(self.make_order_class.goods_in_cart)
        Cart.closeEvent = self.close_window
        self.block_btns()

        self.retranslateUi(Cart)
        QtCore.QMetaObject.connectSlotsByName(Cart)

    def retranslateUi(self, Cart):
        _translate = QtCore.QCoreApplication.translate
        Cart.setWindowTitle(_translate("Cart", "Корзина"))
        self.btn_cart_get_order.setText(_translate("Cart", "Подтвердить заказ"))
        self.btn_cart_delete.setText(_translate("Cart", "Удалить"))
        self.btn_cart_clear.setText(_translate("Cart", "Очистить корзину"))
        self.label_all_rpice.setText(_translate("Cart", "Общая сумма:"))
        self.btn_cart_clear.clicked.connect(partial(self.clear_cart))
        self.btn_cart_delete.clicked.connect(partial(self.delete_from_cart))
        self.btn_cart_get_order.clicked.connect(partial(self.open_window, qt_client_data.Ui_Client_data(
            self, self.make_order_class.current_user, self.make_order_class.goods_in_cart, self.all_price)))

    # отображаем данные в Корзине
    def show_cart(self, cart):
        data = []
        for good in cart:
            self.cursor.execute(f"""SELECT good_name, measure_unit, price*{good[1]}, 
            article_number FROM Goods WHERE article_number = ?""", [good[0]])
            res = self.cursor.fetchone()
            if res:
                data.append(res)
        res_data = []
        for good, i in zip(data, cart):
            res_data.append([good[0], str(i[1] + ' ' + good[1]), good[2], good[3]])
        self.all_price = sum([i[2] for i in res_data])
        self.lineEdit_sum.setText(f'{self.all_price}')
        return self.fill_table(res_data)

    def block_btns(self):
        if len(self.make_order_class.goods_in_cart) == 0:
            self.btn_cart_get_order.setEnabled(False)
            self.btn_cart_delete.setEnabled(False)
            self.btn_cart_clear.setEnabled(False)
        else:
            self.btn_cart_get_order.setEnabled(True)
            self.btn_cart_delete.setEnabled(True)
            self.btn_cart_clear.setEnabled(True)

    # заполняем таблицу данными по колонкам(которые нельзя редактировать)
    def fill_table(self, info):
        col_names = ['Название', 'Количество', 'Цена', 'Артикль']
        self.table_widget_cart.setRowCount(0)
        self.table_widget_cart.setColumnCount(len(info[0]))
        self.table_widget_cart.setHorizontalHeaderLabels(col_names)
        for row_number, row_data in enumerate(info):
            self.table_widget_cart.insertRow(row_number)
            for column, data in enumerate(row_data):
                self.table_widget_cart.setItem(row_number, column, QtWidgets.QTableWidgetItem(str(data)))

    # очистка корзины
    def clear_cart(self):
        for good in self.make_order_class.goods_in_cart:
            self.cursor.execute(f"SELECT amount FROM Goods WHERE article_number = ?", [int(good[0])])
            current_quantity = int(self.cursor.fetchone()[0])
            self.cursor.execute(f"UPDATE Goods SET amount = ? WHERE article_number = ?",
                                [current_quantity + int(good[1]), int(good[0])])
        self.db.commit()
        self.lineEdit_sum.clear()
        self.table_widget_cart.clear()
        self.make_order_class.flag = True
        self.make_order_class.btn_cart.setText('Корзина')
        self.make_order_class.goods_in_cart = []
        self.make_order_class.cart_count = 0
        self.make_order_class.get_info_from_db()
        self.make_order_class.show_data()
        self.block_btns()

    # отображаем окно Сделать заказ при закрытии Корзины
    def close_window(self, event):
        self.make_order_class.get_info_from_db()
        self.make_order_class.show_data()
        self.make_order_class.current_window.show()
        return event.accept()

    # возвращаем товары в БД в случае нажатия "очистить корзину"
    def delete_from_cart(self):
        selected_rows = self.table_widget_cart.selectedItems()
        if not selected_rows:
            return
        selected_ids = set()
        for row in selected_rows:
            article = self.table_widget_cart.item(row.row(), 3)
            quantity = self.table_widget_cart.item(row.row(), 1)
            selected_ids.add((article.text(), quantity.text().split(' ')[0]))
        selected_ids = list([list(i) for i in selected_ids])

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setWindowTitle('Удаление товара')
        msg.setText("Вы уверены, что хотите удалить товар(ы)?")
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        btn = msg.exec_()
        if btn == QtWidgets.QMessageBox.Yes:
            for selected_id in selected_ids:
                self.cursor.execute(f"UPDATE Goods SET amount = amount + ? WHERE article_number = ?",
                                    [selected_id[1], selected_id[0]])
        self.db.commit()

        goods_in_cart = [i for i in self.make_order_class.goods_in_cart if i not in selected_ids]
        self.make_order_class.goods_in_cart = goods_in_cart
        self.make_order_class.cart_count -= 1
        _translate = QtCore.QCoreApplication.translate
        self.make_order_class.btn_cart.setText(_translate("make_order", f"Корзина {self.make_order_class.cart_count}"))

        if len(goods_in_cart) == 0:
            self.table_widget_cart.clear()
            self.lineEdit_sum.clear()
            self.all_price = []
            self.make_order_class.btn_cart.setText('Корзина')
            self.make_order_class.goods_in_cart = []
            self.make_order_class.cart_count = 0
            self.make_order_class.show_data()
        else:
            self.show_cart(self.make_order_class.goods_in_cart)
        self.block_btns()

    # открываем окно подтверждения заказа
    def open_window(self, window):
        self.current_window = QtWidgets.QApplication.activeWindow()
        self.main_window = QtWidgets.QMainWindow()
        self.ui = window
        self.ui.setupUi(self.main_window)
        self.current_window.close()
        self.main_window.show()

