import sys
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QListWidget
)
from PyQt5.QtCore import Qt
from dialogs import InfoMessageDialog, AddNewPasswordDialog, EnterMasterKeyDialog, ErrorMessageDialog
from config import Config
from cryptocode import encrypt, decrypt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setFixedWidth(500)
        self.setFixedHeight(550)
        self.setWindowTitle("Менеджер паролей")
        self.passwords = []
        self.setup_ui()

    def init_data(self, passwords):
        self.passwords = passwords
        view = self.findChild(QListWidget)
        view.addItems(list(map(lambda p: p['name'], self.passwords)))

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        button_layout = QHBoxLayout(self)

        add_button = QPushButton("Добавить", self)
        remove_button = QPushButton("Удалить", self)
        save_button = QPushButton("Сохранить", self)
        pass_view = QListWidget(self)

        add_button.clicked.connect(self.add_new_password)
        save_button.clicked.connect(self.save_all)
        remove_button.clicked.connect(self.remove_button_handler)
        pass_view.itemDoubleClicked.connect(self.pass_view_handler)

        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)
        button_layout.addWidget(save_button)
        main_layout.addWidget(pass_view)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def remove_button_handler(self):
        view = self.findChild(QListWidget)
        if self.passwords:
            self.passwords.pop(view.currentRow())
            view.takeItem(view.currentRow())
        else:
            InfoMessageDialog("Выберите пароль для удаления.")

    def pass_view_handler(self, item):
        pass_name = item.text()
        d = EnterMasterKeyDialog()
        if d.exec_():
            master_key = d.master_key
            for password in self.passwords:
                if password['name'] == pass_name:
                    result = decrypt(password['value'], master_key)
                    if result:
                        InfoMessageDialog("Пароль от {}: {}".format(pass_name, result))
                    else:
                        ErrorMessageDialog("Неправильный пароль мастера.")

    def add_new_password(self):
        d = AddNewPasswordDialog()
        if d.exec_():
            name = d.name
            password = d.password
            master_key = d.master_key
            password = encrypt(password, master_key)
            self.passwords.append(
                {'name': name, 'value': password}
            )
            view = self.findChild(QListWidget)
            view.addItem(name)

    def save_all(self):
        if self.passwords:
            Config.save(self.passwords)
            InfoMessageDialog("Пароли успешно сохранены.")
        else:
            InfoMessageDialog("Вам необходимо добавить хотя бы один пароль.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    if Config.is_created():
        window.init_data(Config.load())
    window.show()
    app.exec_()
