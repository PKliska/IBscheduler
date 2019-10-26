from PyQt5.QtGui import QStandardItemModel, QStandardItem
from ui.edit_subject import Ui_Dialog
from models import Subject

class EditSubject(Ui_Dialog):

    def __init__(self, session, subject=None):
        super().__init__()
        self.session = session

        if subject is None:
            self.subject = Subject()
        else:
            self.subject = subject



    def setupUi(self, dialog):
        super().setupUi(dialog)

        self.name.setText(self.subject.name)
        self.abbreviation.setText(self.subject.abbreviation)
        self.buttonBox.accepted.connect(self.update_subject)

    def update_subject(self):
        self.subject.name = self.name.text()
        self.subject.abbreviation = self.abbreviation.text()

        self.session.add(self.subject)
