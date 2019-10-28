from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QHeaderView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from ui.mainwindow import Ui_MainWindow
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Student, Subject, DayOfWeek, TimePlace
from edit_student import EditStudent
from edit_subject import EditSubject


class MainWindow(Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.filename = ":memory:"
        self.engine = create_engine('sqlite:///'+self.filename)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def setupUi(self, main_window):
        super().setupUi(main_window)

        #Toolbar
        self.actionAdd_student.triggered.connect(self.addStudent)
        self.actionAdd_subject.triggered.connect(self.addSubject)

        #File menu actions
        self.actionOpen.triggered.connect(self.openFile)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionSave_as.triggered.connect(self.saveFileAs)
        self.actionQuit.triggered.connect(QApplication.instance().quit)

        #Students dock
        self.studentLineEdit.textChanged['QString'].connect(self.searchStudents)

        self.student_model = QStandardItemModel()
        self.studentList.setModel(self.student_model)
        self.studentList.doubleClicked['QModelIndex'].connect(self.editStudent)
        self.updateStudentModel()

        #Subjects dock
        self.subjectLineEdit.textChanged['QString'].connect(self.searchSubjects)

        self.subject_model = QStandardItemModel()
        self.subjectList.setModel(self.subject_model)
        self.subjectList.doubleClicked['QModelIndex'].connect(self.editSubject)
        self.updateSubjectModel()

        #Main view
        self.schedule_model = QStandardItemModel(12, 7)
        self.scheduleView.setModel(self.schedule_model)
        self.scheduleView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.scheduleView.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.updateScheduleModel()

    def searchStudents(self, name):
        self.student_model.clear()
        for i in self.session.query(Student).filter(Student.name.ilike('%'+name+'%')):
            it = QStandardItem()
            it.setText(i.name)
            it.setData(i)
            it.setEditable(False)
            self.student_model.appendRow(it)

    def searchSubjects(self, name):
        self.subject_model.clear()
        for i in self.session.query(Subject).filter(Subject.name.ilike('%'+name+'%')):
            it = QStandardItem()
            it.setText(i.name)
            it.setData(i)
            it.setEditable(False)
            self.subject_model.appendRow(it)

    def updateStudentModel(self):
        self.searchStudents(self.studentLineEdit.text())

    def updateSubjectModel(self):
        self.searchSubjects(self.subjectLineEdit.text())

    def updateScheduleModel(self):
        self.schedule_model.clear()
        self.schedule_model.setHorizontalHeaderLabels(["Monday", "Tuesday",
                                                    "Wednesday", "Thursday",
                                                    "Friday", "Saturday",
                                                    "Sunday"])
        for i in DayOfWeek:
            for j in range(12):
                q = self.session.query(TimePlace).filter(TimePlace.day == i, TimePlace.slot == j)
                subjects = []
                for tp in q:
                    subjects.append(' '.join([tp.subject.abbreviation, tp.place.name]))
                it = QStandardItem()
                it.setText('\n'.join(subjects))
                it.setEditable(False)
                self.schedule_model.setItem(j, int(i), it)

    def addStudent(self):
        dialog = QDialog()
        content = EditStudent(self.session)
        content.setupUi(dialog)
        dialog.exec_()
        self.updateStudentModel()
        self.updateScheduleModel()

    def addSubject(self):
        dialog = QDialog()
        content = EditSubject(self.session)
        content.setupUi(dialog)
        dialog.exec_()
        self.updateSubjectModel()
        self.updateScheduleModel()

    def editStudent(self, idx):
        dialog = QDialog()
        content = EditStudent(self.session, self.student_model.itemFromIndex(idx).data())
        content.setupUi(dialog)
        dialog.exec_()
        self.updateStudentModel()
        self.updateScheduleModel()

    def editSubject(self, idx):
        dialog = QDialog()
        content = EditSubject(self.session, self.subject_model.itemFromIndex(idx).data())
        content.setupUi(dialog)
        dialog.exec_()
        self.updateSubjectModel()
        self.updateScheduleModel()

    def openFile(self):
        new_filename = QFileDialog.getOpenFileName(caption="Open file",
                                filter="SQLite3 file (*.sqlite3)")[0]
        if new_filename:
            self.filename = new_filename
            self.engine.dispose()
            self.engine = create_engine('sqlite:///'+self.filename)
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
            self.session = self.Session()
            self.updateStudentModel()
            self.updateSubjectModel()
            self.updateScheduleModel()

    def saveFile(self):
        if self.filename == ':memory:':
            self.saveFileAs()
        else:
            self.session.commit()

    def saveFileAs(self):
        new_filename = QFileDialog.getSaveFileName(caption="Save file as",
                                filter="SQLite3 file (*.sqlite3)")[0]
        if new_filename:
            new_engine = create_engine('sqlite:///'+new_filename)
            Base.metadata.drop_all(new_engine)
            Base.metadata.create_all(new_engine)
            tables = Base.metadata.tables
            for tbl in tables:
                data = self.engine.execute(tables[tbl].select()).fetchall()
                if data:
                    new_engine.execute(tables[tbl].insert(), data)
            self.engine.dispose()
            self.engine = new_engine
            self.Session = sessionmaker(bind=self.engine)
            self.session = self.Session()
            self.filename=new_filename
            self.updateSubjectModel()
            self.updateStudentModel()
            self.updateScheduleModel()
