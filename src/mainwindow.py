from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from ui.mainwindow import Ui_MainWindow
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Student
from add_student import AddStudent


class MainWindow(Ui_MainWindow):

    def __init__(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)

        self.Session = sessionmaker(bind=self.engine)
        self.student_model = QStandardItemModel()
        super().__init__()

    def setupUi(self, main_window):
        super().setupUi(main_window)

        #Toolbar
        self.actionAdd_student.triggered.connect(self.addStudent)

        #File menu actions
        self.actionQuit.triggered.connect(QApplication.instance().quit)

        #Students dock
        self.studentLineEdit.textChanged['QString'].connect(self.searchStudents)
        self.studentList.setModel(self.student_model)
        self.searchStudents("")

    def searchStudents(self, name):
        session = self.Session()

        self.student_model.clear()
        for i in session.query(Student).filter(Student.name.ilike('%'+name+'%')):
            it = QStandardItem()
            it.setText(i.name)
            self.student_model.appendRow(it)


    def addStudent(self):
        self.dialog = QDialog()
        content = AddStudent(self.Session())
        content.setupUi(self.dialog)
        self.dialog.exec_()

    def load_file(self, filename):
        pass
