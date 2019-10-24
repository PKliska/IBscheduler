from PyQt5.QtGui import QStandardItemModel, QStandardItem
from ui.add_student import Ui_dialog
from models import Student, Subject

class AddStudent(Ui_dialog):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.subjects_model = QStandardItemModel()
        for i in session.query(Subject).all():
            it = QStandardItem()
            it.setCheckable(True)
            it.setText(i.name)
            it.setData(i)
            self.subjects_model.appendRow(it)


    def setupUi(self, dialog):
        super().setupUi(dialog)

        self.subject_list.setModel(self.subjects_model)
        self.buttonBox.accepted.connect(self.add_student)

    def add_student(self):
        s = Student(name = self.student_name.text())
        for i in range(self.subjects_model.rowCount()):
            subject = self.subjects_model.item(i)
            if subject.checkState():
                s.subjects.append(subject.data())
        self.session.add(s)
        self.session.commit()
