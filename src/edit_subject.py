from PyQt5.QtGui import QStandardItemModel, QStandardItem
from ui.edit_subject import Ui_Dialog
from sqlalchemy.sql import exists
from models import Subject, Place, TimePlace

class EditSubject(Ui_Dialog):

    def __init__(self, session, subject=None):
        super().__init__()
        self.session = session
        if subject is None:
            self.subject = Subject()
        else:
            self.subject = subject

        self.timeslot_model = QStandardItemModel(10, 7)
        self.timeslot_model.setHorizontalHeaderLabels(["Monday", "Tuesday",
                                                    "Wednesday", "Thursday",
                                                    "Friday", "Saturday",
                                                    "Sunday"])



    def setupUi(self, dialog):
        super().setupUi(dialog)

        self.name.setText(self.subject.name)
        self.abbreviation.setText(self.subject.abbreviation)
        self.timeslotView.setModel(self.timeslot_model)

        self.buttonBox.accepted.connect(self.update_subject)

    def update_subject(self):
        self.subject.name = self.name.text()
        self.subject.abbreviation = self.abbreviation.text()
        for i in range(self.timeslot_model.rowCount()):
            for j in range(self.timeslot_model.columnCount()):
                it = self.timeslot_model.item(i, j)
                if it is not None:
                    place = self.session.query(Place).filter(Place.name == it.text()).one_or_none()
                    if place is not None:
                        tp = TimePlace()
                        tp.day = i
                        tp.slot = j
                        tp.place = place
                        self.subject.time_places.append(tp)

        self.session.add(self.subject)
