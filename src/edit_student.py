from PyQt5.QtGui import QStandardItemModel, QStandardItem
from ui.edit_student import Ui_dialog
from models import Student, Subject

class EditStudent(Ui_dialog):
    def __init__(self, session, student=None):
        super().__init__()
        self.session = session

        if student is None:
            self.student = Student()
        else:
            self.student = student

        self.subjects_model = QStandardItemModel()
        for i in session.query(Subject).all():
            it = QStandardItem()
            it.setCheckable(True)
            if i in self.student.subjects:
                it.setCheckState(2)
            it.setText(i.name)
            it.setData(i)
            self.subjects_model.appendRow(it)


    def setupUi(self, dialog):
        super().setupUi(dialog)

        self.student_name.setText(self.student.name)
        self.subject_list.setModel(self.subjects_model)
        self.buttonBox.accepted.connect(self.add_student)

    def add_student(self):
        self.student.name = self.student_name.text()
        self.student.subjects = []
        for i in range(self.subjects_model.rowCount()):
            subject = self.subjects_model.item(i)
            if subject.checkState():
                self.student.subjects.append(subject.data())
        self.session.add(self.student)
