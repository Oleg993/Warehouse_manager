import os
import shutil
import sqlite3
from functools import partial
import random

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QComboBox, QFileDialog
from PyQt5.QtGui import QPixmap

from Db_functions import DataBase as db


class Ui_add_good(object):
    def __init__(self, user):
        self.db = sqlite3.connect('Warehouses_db.db')
        self.cursor = self.db.cursor()
        self.image_path = None
        self.downloaded_image_path = None
        self.data_to_upload = []
        self.current_user = user
        self.flag = False

    def setupUi(self, add_good):
        add_good.setObjectName("add_good")
        add_good.resize(600, 380)
        self.table_add_good = QtWidgets.QTableWidget(add_good)
        self.table_add_good.setGeometry(QtCore.QRect(20, 30, 560, 180))
        self.table_add_good.setObjectName("table_add_good")
        self.tableWidget_new_data = QtWidgets.QTableWidget(add_good)
        self.tableWidget_new_data.setGeometry(QtCore.QRect(20, 230, 560, 80))
        self.tableWidget_new_data.setObjectName("tableWidget_new_data")
        self.tableWidget_new_data.setColumnCount(0)
        self.tableWidget_new_data.setRowCount(0)
        self.layoutWidget = QtWidgets.QWidget(add_good)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 330, 560, 25))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_add_good = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_add_good.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_add_good.setObjectName("btn_add_good")
        self.horizontalLayout.addWidget(self.btn_add_good)
        self.btn_clear_data = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_clear_data.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_clear_data.setObjectName("btn_clear_data")
        self.horizontalLayout.addWidget(self.btn_clear_data)

        # При запуске:
        # заполняем таблицу данными
        # создаем таблицу для добавления нового товара
        # запускаем сортировку при нажатии на столбец
        self.show_data_main()
        self.fill_table()
        self.table_add_good.horizontalHeader().sectionClicked.connect(self.sort_table)

        self.retranslateUi(add_good)
        QtCore.QMetaObject.connectSlotsByName(add_good)

    def retranslateUi(self, add_good):
        _translate = QtCore.QCoreApplication.translate
        add_good.setWindowTitle(_translate("add_good", "Добавление товара"))
        self.btn_add_good.setText(_translate("add_good", "Добавить товар"))
        self.btn_clear_data.setText(_translate("add_good", "Очистить данные"))
        self.btn_add_good.clicked.connect(partial(self.add_goods_to_db))
        self.btn_clear_data.clicked.connect(partial(self.clear_data))

    # сортировака при нажатии на столбик
    def sort_table(self, column):
        if not self.flag or self.table_add_good.horizontalHeader().sortIndicatorSection() != column:
            self.table_add_good.sortItems(column, QtCore.Qt.AscendingOrder)
            self.flag = True
        else:
            self.table_add_good.sortItems(column, QtCore.Qt.DescendingOrder)
            self.flag = False

    # получаем данные заполняем таблицу
    def show_data_main(self):
        self.cursor.execute("""SELECT good_name, amount, measure_unit, price, time_start, time_to_end, 
            description, article_number, image FROM Goods""")
        res = self.cursor.fetchall()
        if not res:
            QtWidgets.QMessageBox.information(self.tableWidget_new_data, 'Поиск товаров', 'Данные не найдены!')
        else:
            self.fill_table(res)

    # заполняем таблицу для воода данных по новому товару
    # заполняем таблицу с данными из БД
    def fill_table(self, info=None):
        if info is None:
            self.cursor.execute(f"SELECT * FROM Goods")
            res = self.cursor.fetchall()
            col_names = ['Склад', 'Категория', 'Название', 'Количество', 'Единица измер.', 'Цена', 'Годен с',
                         'Годен до', 'Описание', 'Изображение']
            self.tableWidget_new_data.setRowCount(1)
            self.tableWidget_new_data.setColumnCount(len(res[0])-1)
            self.tableWidget_new_data.setHorizontalHeaderLabels(col_names)
            for column in range(len(col_names)):
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget_new_data.setItem(0, column, item)
                if column == 0:
                    combo_box = QComboBox()
                    combo_box.clear()
                    warehouses = ["Выберите"]
                    warehouses += db().get_warehouses_names()
                    for warehouse in warehouses:
                        combo_box.addItem(warehouse)
                    self.tableWidget_new_data.setCellWidget(0, column, combo_box)
                if column == 1:
                    combo_box = QComboBox()
                    combo_box.clear()
                    categories = ["Выберите"]
                    self.cursor.execute(f"SELECT category_name FROM Categories")
                    res = self.cursor.fetchall()
                    categories += [i[0] for i in res]
                    for category in categories:
                        combo_box.addItem(category)
                    self.tableWidget_new_data.setCellWidget(0, column, combo_box)
                if column == len(col_names)-1:
                    button = QPushButton()
                    button.setText("Добавить")
                    button.clicked.connect(partial(self.get_data_and_img_for_download))
                    self.tableWidget_new_data.setCellWidget(0, column, button)
                if column == len(col_names) - 4 or column == len(col_names) - 3:
                    item.setText('гггг-мм-дд')

        else:
            col_names = ['Название', 'Количество', 'Единица измер.', 'Цена', 'Годен с', 'Годен до', 'Описание',
                         'Артикл', 'Изображение']
            self.table_add_good.setRowCount(0)
            self.table_add_good.setColumnCount(len(info[0]))
            self.table_add_good.setHorizontalHeaderLabels(col_names)
            for row_number, row_data in enumerate(info):
                self.table_add_good.insertRow(row_number)
                for column, data in enumerate(row_data):
                    if column == len(row_data) - 1:
                        button = QPushButton()
                        button.setText("Открыть")
                        button.clicked.connect(partial(self.open_image, data))
                        self.table_add_good.setCellWidget(row_number, column, button)
                    else:
                        item = QtWidgets.QTableWidgetItem(str(data))
                        item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                        self.table_add_good.setItem(row_number, column, item)

    # открываем картинку
    def open_image(self, image_path):
        if image_path:
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(350, 350, QtCore.Qt.KeepAspectRatio)
            self.image_label = QtWidgets.QLabel()
            self.image_label.setPixmap(pixmap)
            self.image_label.setWindowTitle("Изображение")
            self.image_label.show()

    # получаем данные для сохранения картинки в папку
    def get_data_and_img_for_download(self):
        row_count = self.tableWidget_new_data.rowCount()
        col_count = self.tableWidget_new_data.columnCount()

        for row in range(row_count):
            for col in range(col_count):
                widget = self.tableWidget_new_data.cellWidget(row, col)
                if isinstance(widget, QComboBox):
                    self.data_to_upload.append(widget.currentText())
                else:
                    item = self.tableWidget_new_data.item(row, col)
                    if item is not None:
                        self.data_to_upload.append(item.text())

        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg)")
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            self.image_path = selected_files[0]

        self.data_to_upload[-1] = self.get_article()
        return self.data_to_upload

    # получаем номер артикля (идентичен ID товара)
    def get_article(self):
        self.cursor.execute(f"SELECT MAX(article_number) + 1 FROM Goods")
        article = self.cursor.fetchone()[0]
        return article

    # сохранение картинки в папку
    def save_img(self, img_path):
        if self.image_path and self.data_to_upload:
            if not os.path.exists('Goods_img'):
                os.makedirs('Goods_img')

            image_name = os.path.basename(img_path)
            if os.path.exists(f'Goods_img/{image_name}'):
                random_number = random.randint(1, 100)
                image_name = f'{os.path.splitext(image_name)[0]}_{random_number}{os.path.splitext(image_name)[1]}'

            shutil.copy(img_path, f'Goods_img/{image_name}')
            self.downloaded_image_path = f'Goods_img/{image_name}'

            return self.downloaded_image_path

    # добавление данных по новому товару в БД
    def add_goods_to_db(self):
        if self.save_img(self.image_path):
            self.data_to_upload.append(self.downloaded_image_path)
            warehouse = self.data_to_upload[0]
            category = self.data_to_upload[1]
            self.cursor.execute("SELECT id FROM Warehouses WHERE warehouse_name =?", [warehouse])
            warehouse_id = self.cursor.fetchone()[0]
            self.cursor.execute("SELECT id FROM Categories WHERE category_name =?", [category])
            category_id = self.cursor.fetchone()[0]
            self.cursor.execute(f"""INSERT INTO Goods(warehouse_id, category_id, good_name, amount, measure_unit,
            price, time_start, time_to_end, description, article_number, image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", [warehouse_id, category_id, *self.data_to_upload[2:]])
            self.db.commit()
            self.show_data_main()
            self.fill_table()
            self.image_path = None
            self.downloaded_image_path = None
            self.data_to_upload = []
        return self.cursor.rowcount > 0

    # очистка данных после загрузки картинки
    def clear_data(self):
        self.fill_table()
        self.image_path = None
        self.downloaded_image_path = None
        self.data_to_upload = []



