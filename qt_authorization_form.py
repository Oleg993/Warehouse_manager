from PyQt5 import QtCore, QtGui, QtWidgets
from Db_functions import DataBase

class Ui_Authorize_form(object):
    def setupUi(self, Authorize_form):
        Authorize_form.setObjectName("Authorize_form")
        Authorize_form.resize(275, 175)
        self.layoutWidget = QtWidgets.QWidget(Authorize_form)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 10, 231, 161))
        self.layoutWidget.setObjectName("layoutWidget")
        self.vboxlayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.vboxlayout.setContentsMargins(0, 0, 0, 0)
        self.vboxlayout.setObjectName("vboxlayout")
        self.lineEdit_login = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_login.setMaximumSize(QtCore.QSize(229, 16777215))
        self.lineEdit_login.setFrame(False)
        self.lineEdit_login.setObjectName("lineEdit_login")
        self.vboxlayout.addWidget(self.lineEdit_login)
        self.lineEdit_password = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_password.setFrame(False)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.vboxlayout.addWidget(self.lineEdit_password)
        self.btn_enter = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_enter.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_enter.setObjectName("btn_enter")
        self.vboxlayout.addWidget(self.btn_enter)

        self.retranslateUi(Authorize_form)
        QtCore.QMetaObject.connectSlotsByName(Authorize_form)

    def retranslateUi(self, Authorize_form):
        _translate = QtCore.QCoreApplication.translate
        Authorize_form.setWindowTitle(_translate("Authorize_form", "Авторизация"))
        self.lineEdit_login.setPlaceholderText(_translate("Authorize_form", "Введите логин"))
        self.lineEdit_password.setPlaceholderText(_translate("Authorize_form", "Введите пароль"))
        self.btn_enter.setText(_translate("Authorize_form", "Войти"))

        '''Перенос заказов в архив и создание новых таблиц для них'''
        schedule = DataBase().create_db_for_old_orders()
        if schedule[0]:
            DataBase().tranfer_old_orders_into_archive_db_and_delete(schedule[1:])

        '''Вышел срок годности товаров, составление накладных на списание'''
        DataBase().delete_after_time_good_ends()
