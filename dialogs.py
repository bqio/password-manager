from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QMessageBox
)
from PyQt5.QtCore import Qt


class BaseDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.setFixedWidth(350)


class ErrorMessageDialog(QMessageBox):
    def __init__(self, text):
        super().__init__()
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.setWindowTitle("Ошибка")
        self.setText(text)
        self.setIcon(QMessageBox.Critical)
        self.exec_()


class InfoMessageDialog(QMessageBox):
    def __init__(self, text):
        super().__init__()
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.setWindowTitle("Информация")
        self.setText(text)
        self.setIcon(QMessageBox.Information)
        self.exec_()


class EnterMasterKeyDialog(BaseDialog):
    def __init__(self):
        super(EnterMasterKeyDialog, self).__init__()
        self.setWindowTitle("Конфигурация")
        self.master_key = None
        self.setup_ui()

    def setup_ui(self):
        main_box = QVBoxLayout()
        master_key_input = QLineEdit()
        ok_btn = QPushButton("ОК")

        master_key_input.setPlaceholderText("Введите пароль мастера")
        master_key_input.setEchoMode(QLineEdit.Password)
        ok_btn.setDefault(True)

        master_key_input.textChanged.connect(self.master_key_input_handler)
        ok_btn.clicked.connect(self.ok_btn_handler)

        main_box.addWidget(master_key_input)
        main_box.addWidget(ok_btn)
        self.setLayout(main_box)

    def master_key_input_handler(self, master_key):
        self.master_key = master_key

    def ok_btn_handler(self):
        if self.master_key is not None:
            self.accept()
        else:
            ErrorMessageDialog("Введите пароль мастера!")


class AddNewPasswordDialog(BaseDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Конфигурация")
        self.name = None
        self.password = None
        self.master_key = None
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        name_input = QLineEdit(self)
        pass_input = QLineEdit(self)
        master_key_input = QLineEdit(self)
        add_button = QPushButton("Добавить", self)

        name_input.setPlaceholderText("Введите имя для пароля")
        pass_input.setPlaceholderText("Введите пароль")
        master_key_input.setPlaceholderText("Введите пароль мастера")
        name_input.setFocus()
        pass_input.setEchoMode(QLineEdit.Password)
        master_key_input.setEchoMode(QLineEdit.Password)
        add_button.setDefault(True)

        name_input.textChanged.connect(self.name_input_handler)
        pass_input.textChanged.connect(self.pass_input_handler)
        master_key_input.textChanged.connect(self.master_key_input_handler)
        add_button.clicked.connect(self.add_button_handler)

        main_layout.addWidget(name_input)
        main_layout.addWidget(pass_input)
        main_layout.addWidget(master_key_input)
        main_layout.addWidget(add_button)
        self.setLayout(main_layout)

    def name_input_handler(self, name):
        self.name = name

    def pass_input_handler(self, password):
        self.password = password

    def master_key_input_handler(self, master_key):
        self.master_key = master_key

    def add_button_handler(self):
        if self.name is None or self.password is None or self.master_key is None:
            ErrorMessageDialog("Введите корректные данные.")
        else:
            self.accept()
