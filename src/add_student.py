from ui.add_student import Ui_dialog
from models import Student

class AddStudent(Ui_dialog):
    def __init__(self, session):
        self.session=session
        super().__init__()

    def setupUi(self, dialog):
        super().setupUi(dialog)
        self.buttonBox.accepted.connect(self.add_student)

    def add_student(self):
        s = Student(name = self.student_name.text())
        self.session.add(s)
        self.session.commit()
