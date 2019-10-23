from PyQt5.QtWidgets import QApplication
from ui.mainwindow import Ui_MainWindow


class MainWindow(Ui_MainWindow):

    def __init__(self):
        super().__init__()

    def setupUi(self, main_window):
        super().setupUi(main_window)

        #File menu actions
        self.actionQuit.triggered.connect(QApplication.instance().quit)

        #Students dock
        self.studentLineEdit.textChanged['QString'].connect(self.searchStudents)

    def searchStudents(self, s):
        self.studentList.addItem(s)
