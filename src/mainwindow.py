from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QHeaderView, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtCore import Qt
from ui.mainwindow import Ui_MainWindow
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Student, Subject, DayOfWeek, TimePlace
from edit_student import EditStudent
from edit_subject import EditSubject
from about import About


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

        #Help menu actions
        self.actionAbout.triggered.connect(self.showAbout)

        #Students dock
        self.studentLineEdit.textChanged['QString'].connect(self.searchStudents)

        self.student_model = QStandardItemModel()
        self.studentList.setModel(self.student_model)
        self.studentList.doubleClicked['QModelIndex'].connect(self.editStudent)
        self.studentList.selectionModel().selectionChanged['QItemSelection', 'QItemSelection'].connect(self.changeSelectedStudent)
        self.studentList.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
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

    def changeSelectedStudent(self, selected, unselected):
        tps = []
        for s in selected:
            for i in s.indexes():
                student = self.student_model.itemFromIndex(i).data()
                for subject in student.subjects:
                    for tp in subject.time_places:
                        tps.append((tp.slot, int(tp.day)))

        crossed = QBrush(Qt.black, Qt.BDiagPattern)
        normal = QBrush(Qt.white)

        for i in range(12):
            for j in map(int, DayOfWeek):
                if (i, j) in tps:
                    self.schedule_model.item(i, j).setBackground(normal)
                else:
                    self.schedule_model.item(i, j).setBackground(crossed)


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

    def showAbout(self):
        dialog = QDialog()
        ui = About()
        ui.setupUi(dialog)
        dialog.exec_()
