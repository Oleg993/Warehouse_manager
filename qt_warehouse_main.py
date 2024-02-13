import sqlite3
import traceback
from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QPushButton
from PyQt5.QtGui import QPixmap

import qt_make_order
import qt_add_good
import qt_orders_history
import qt_admin_panel
from Db_functions import DataBase as db


class Ui_MainWindow(object):
    def __init__(self, user):
        self.db = sqlite3.connect('Warehouses_db.db')
        self.cursor = self.db.cursor()
        self.selected_warehouse = None
        self.current_user = user
        self.info_for_search = None
        self.flag = False

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(730, 435)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox_warehouses = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_warehouses.setGeometry(QtCore.QRect(30, 10, 300, 20))
        self.comboBox_warehouses.setCurrentText("")
        self.comboBox_warehouses.setObjectName("comboBox_warehouses")
        self.table_warehouse = QtWidgets.QTableWidget(self.centralwidget)
        self.table_warehouse.setGeometry(QtCore.QRect(30, 60, 670, 250))
        self.table_warehouse.setObjectName("table_warehouse")
        self.lineEdit_search = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_search.setGeometry(QtCore.QRect(530, 10, 171, 25))
        self.lineEdit_search.setText("")
        self.lineEdit_search.setFrame(False)
        self.lineEdit_search.setObjectName("lineEdit_search")
        self.btn_search = QtWidgets.QPushButton(self.centralwidget)
        self.btn_search.setGeometry(QtCore.QRect(340, 10, 75, 20))
        self.btn_search.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_search.setObjectName("btn_search")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 330, 671, 61))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_take_changes = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_take_changes.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_take_changes.setObjectName("btn_take_changes")
        self.horizontalLayout.addWidget(self.btn_take_changes)
        self.btn_delete = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_delete.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_delete.setObjectName("btn_delete")
        self.horizontalLayout.addWidget(self.btn_delete)
        self.btn_cancel_changes = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_cancel_changes.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_cancel_changes.setObjectName("btn_cancel_changes")
        self.horizontalLayout.addWidget(self.btn_cancel_changes)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar_warehouse = QtWidgets.QMenuBar(MainWindow)
        self.menubar_warehouse.setGeometry(QtCore.QRect(0, 0, 730, 21))
        self.menubar_warehouse.setObjectName("menubar_warehouse")
        self.menu = QtWidgets.QMenu(self.menubar_warehouse)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar_warehouse)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action_2 = QtWidgets.QAction(MainWindow)
        self.action_2.setObjectName("action_2")
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.setObjectName("action_3")
        self.action_4 = QtWidgets.QAction(MainWindow)
        self.action_4.setObjectName("action_4")
        self.action_5 = QtWidgets.QAction(MainWindow)
        self.action_5.setObjectName("action_5")
        self.menu.addAction(self.action)
        self.menu.addAction(self.action_2)
        self.menu.addAction(self.action_4)
        self.menu.addAction(self.action_5)
        self.menubar_warehouse.addAction(self.menu.menuAction())

        # При запуске:
        # получаем список имеющихся складов
        # получаем данны по товарам из БД чтобы поиск работал корректно во всех регистрах
        # отображаем таблицу с товарами
        # запускаем сортировку при нажатии на столбец
        self.get_warehouses_list()
        self.get_info_from_db()
        self.show_data_main()
        self.table_warehouse.horizontalHeader().sectionClicked.connect(self.sort_table)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Выбор склада"))
        self.lineEdit_search.setPlaceholderText(_translate("MainWindow", "Поиск..."))
        self.btn_search.setText(_translate("MainWindow", "Выбрать"))
        self.btn_take_changes.setText(_translate("MainWindow", "Подтвердить изменения"))
        self.btn_delete.setText(_translate("MainWindow", "Удалить"))
        self.btn_cancel_changes.setText(_translate("MainWindow", "Отменить изменения"))
        self.menu.setTitle(_translate("MainWindow", "Меню"))
        self.action.setText(_translate("MainWindow", "Оформить заказ"))
        self.action_2.setText(_translate("MainWindow", "Добавить товар"))
        self.action_3.setText(_translate("MainWindow", "Редактировать товары"))
        self.action_4.setText(_translate("MainWindow", "История заказов"))
        self.action_5.setText(_translate("MainWindow", "Панель администратора"))
        self.action.triggered.connect(partial(self.open_window, qt_make_order.Ui_make_order(self.current_user)))
        self.action_2.triggered.connect(partial(self.open_window, qt_add_good.Ui_add_good(self.current_user)))
        self.action_4.triggered.connect(partial(self.open_window, qt_orders_history.Ui_Orders_History(self.current_user)))
        self.action_5.triggered.connect(partial(self.open_window, qt_admin_panel.Ui_Admin_panel(self.current_user)))
        self.lineEdit_search.returnPressed.connect(partial(self.show_selected_warehouse_goods))
        self.btn_search.clicked.connect(partial(self.show_selected_warehouse_goods))
        self.btn_cancel_changes.clicked.connect(partial(self.show_selected_warehouse_goods))
        self.btn_delete.clicked.connect(partial(self.delete_good))
        self.btn_take_changes.clicked.connect(partial(self.change_data))

    # сортировака по столбикам
    def sort_table(self, column):
        if not self.flag or self.table_warehouse.horizontalHeader().sortIndicatorSection() != column:
            self.table_warehouse.sortItems(column, QtCore.Qt.AscendingOrder)
            self.flag = True
        else:
            self.table_warehouse.sortItems(column, QtCore.Qt.DescendingOrder)
            self.flag = False

    # полeчаем данные по товарам для поиска
    def get_info_from_db(self):
        self.cursor.execute(f"""SELECT good_name, amount, measure_unit, price, time_start, time_to_end, description,
        article_number, image FROM Goods""")
        self.info_for_search = self.cursor.fetchall()

    def open_window(self, window):
        self.main_window = QtWidgets.QMainWindow()
        self.ui = window
        self.ui.setupUi(self.main_window)
        self.main_window.show()

    # заполняем таблицу данными по колонкам(которые можно редактировать)
    def fill_table(self, info):
        col_names = ['Название', 'Количество', 'Единица измер.', 'Цена', 'Годен с', 'Годен до', 'Описание',
                     'Артикль', 'Изображение']
        self.table_warehouse.setRowCount(0)
        self.table_warehouse.setColumnCount(len(info[0]))
        self.table_warehouse.setHorizontalHeaderLabels(col_names)
        for row_number, row_data in enumerate(info):
            self.table_warehouse.insertRow(row_number)
            for column, data in enumerate(row_data):
                if column == len(row_data)-1:
                    button = QPushButton()
                    button.setText("Открыть")
                    button.clicked.connect(partial(self.open_image, data))
                    self.table_warehouse.setCellWidget(row_number, column, button)
                if column == len(row_data)-2:
                    item = QtWidgets.QTableWidgetItem(str(data))
                    if column == len(row_data) - 2:
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.table_warehouse.setItem(row_number, column, item)
                else:
                    self.table_warehouse.setItem(row_number, column, QtWidgets.QTableWidgetItem(str(data)))

    # отображаем данные по выбранному складу или по всем складам
    # отображаем данные введенные в окно поиск по выбранному складу(всем складам)
    def show_data_main(self, selected_warehouse_data=None):
        if selected_warehouse_data is None:
            info_for_search = self.info_for_search
        else:
            info_for_search = selected_warehouse_data

        search_text = self.lineEdit_search.text().lower()
        if search_text:
            res = []
            for info in info_for_search:
                if info[0].lower() == search_text or search_text in info[0].lower():
                    res.append(info)
            return self.fill_table(res) if res != [] else (
                QtWidgets.QMessageBox.information(self.table_warehouse, 'Ошибка поиска', 'Данные не найдены!'))
        else:
            return self.fill_table(info_for_search) if info_for_search != [] else (
                QtWidgets.QMessageBox.information(self.table_warehouse, 'Ошибка поиска', 'Данные не найдены!'))

    # список складов
    def get_warehouses_list(self):
        self.comboBox_warehouses.clear()
        warehouses = ["Все склады"]
        warehouses += db().get_warehouses_names()
        for warehouse in warehouses:
            self.comboBox_warehouses.addItem(warehouse)

    # отображение товаров в выбранном складе
    def show_selected_warehouse_goods(self):
        if self.comboBox_warehouses.currentText() != 'Все склады':
            selected_warehouse = self.comboBox_warehouses.currentText()
            self.cursor.execute(f"""SELECT good_name, amount, measure_unit, price, time_start, time_to_end,
                                description, article_number, image FROM Goods
                                JOIN Warehouses ON Goods.warehouse_id = Warehouses.id
                                WHERE Warehouses.Warehouse_name = ?""", [selected_warehouse])
            res = self.cursor.fetchall()
            self.get_info_from_db()
            return self.show_data_main(res)
        else:
            self.get_info_from_db()
            return self.show_data_main()

    # открываем картинку в новом окне
    def open_image(self, image_path):
        if image_path:
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
            self.image_label = QtWidgets.QLabel()
            self.image_label.setPixmap(pixmap)
            self.image_label.setWindowTitle("Изображение")
            self.image_label.show()

    # удаление выбранного товара
    def delete_good(self):
        try:
            selected_rows = self.table_warehouse.selectedItems()
            if not selected_rows:
                return
            selected_ids = []
            for row in selected_rows:
                item = self.table_warehouse.item(row.row(), 7)
                selected_ids.append(item.text())
            selected_ids = set(selected_ids)
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle('Удаление товара')
            msg.setText("Вы уверены, что хотите удалить товар(ы)?")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            btn = msg.exec_()
            if btn == QtWidgets.QMessageBox.Ok:
                for selected_id in selected_ids:
                    self.cursor.execute(f"DELETE FROM Goods WHERE article_number = ?", [selected_id])
            self.db.commit()
            self.show_selected_warehouse_goods()

        except Exception as e:
            traceback.print_exc()

    # изменение данных в введенных в колонку
    def change_data(self):
        col_names = {'Название': 'good_name', 'Количество': 'amount', 'Единица измер.': 'measure_unit', 'Цена': 'price',
                     'Годен с': 'time_start', 'Годен до': 'time_to_end', 'Описание': 'description'}
        selected_fields = self.table_warehouse.selectedItems()
        if not selected_fields:
            return

        for field in selected_fields:
            row = field.row() + 1
            column = field.column()
            new_value = field.text()
            article = self.table_warehouse.item(row-1, 7).text()
            column_name = col_names[self.table_warehouse.horizontalHeaderItem(column).text()]
            self.cursor.execute(f"UPDATE Goods SET {column_name} = ? WHERE article_number = ?", [new_value, article])

        self.db.commit()
        self.show_selected_warehouse_goods()

