from PyQt5.QtWidgets import QMessageBox

import qt_authorization_form
from qt_warehouse_main import *


class Login(QtWidgets.QMainWindow, qt_authorization_form.Ui_Authorize_form):
    def __init__(self):
        super(Login, self).__init__()
        self.setupUi(self)
        self.db = sqlite3.connect('Warehouses_db.db')
        self.cursor = self.db.cursor()
        self.current_user = None

        self.btn_enter.clicked.connect(self.login)

    def login(self):
        #забираем логин и пароль введенные в соответствующие поля
        user_login = self.lineEdit_login.text()
        user_password = self.lineEdit_password.text()
        #проверяем чтобы поля не были пустыми
        if len(user_login) == 0 or len(user_password) == 0:
            return

        try:
            # проверяем зарегистрирован ли пользователь, если нет выводим соответствующее окно
            self.cursor.execute("SELECT id, password FROM users WHERE login=?", [user_login])
            check_pass = self.cursor.fetchone()

            if check_pass is not None and check_pass[1] == user_password:
                self.hide()
                self.open_main_window(check_pass[0])
            else:
                QMessageBox.critical(self, "Ошибка авторизации", "Неверный логин или пароль")
        except (sqlite3.Error, TypeError) as e:
            QMessageBox.critical(self, "Ошибка", f"Возникла ошибка: {str(e)}")

    def open_main_window(self, user):
        # открываем главное окно после успешной авторизации
        self.main_window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow(user)
        self.current_user = user
        self.ui.setupUi(self.main_window)
        self.main_window.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication([])
    window = Login()
    window.show()
    sys.exit(app.exec())
