from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from ui.mainwindow import Ui_MainWindow
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Student, Subject
from edit_student import EditStudent


class MainWindow(Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.engine = create_engine('sqlite:///:memory:', echo=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def setupUi(self, main_window):
        super().setupUi(main_window)

        #Toolbar
        self.actionAdd_student.triggered.connect(self.addStudent)

        #File menu actions
        self.actionOpen.triggered.connect(self.openFile)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionQuit.triggered.connect(QApplication.instance().quit)

        #Students dock
        self.studentLineEdit.textChanged['QString'].connect(self.searchStudents)

        self.student_model = QStandardItemModel()
        self.studentList.setModel(self.student_model)
        self.studentList.doubleClicked['QModelIndex'].connect(self.editStudent)
        self.updateStudentModel()

        self.searchStudents("")

    def searchStudents(self, name):
        self.student_model.clear()
        for i in self.session.query(Student).filter(Student.name.ilike('%'+name+'%')):
            it = QStandardItem()
            it.setText(i.name)
            it.setData(i)
            it.setEditable(False)
            self.student_model.appendRow(it)

    def updateStudentModel(self):
        self.searchStudents(self.studentLineEdit.text())


    def addStudent(self):
        self.dialog = QDialog()
        content = EditStudent(self.session)
        content.setupUi(self.dialog)
        self.dialog.exec_()
        self.updateStudentModel()

    def editStudent(self, idx):
        self.dialog = QDialog()
        content = EditStudent(self.session, self.student_model.itemFromIndex(idx).data())
        content.setupUi(self.dialog)
        self.dialog.exec_()
        self.updateStudentModel()

    def openFile(self):
        filename = QFileDialog.getOpenFileName(caption="Load file",
                                filter="SQLite3 file (*.sqlite3)")[0]
        if filename:
            self.engine.dispose()
            self.engine = create_engine('sqlite:///'+filename)
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
            self.session = self.Session()
            self.updateStudentModel()

    def saveFile(self):
        self.session.commit()
