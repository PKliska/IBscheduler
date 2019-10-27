from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMessageBox
from ui.edit_subject import Ui_Dialog
from sqlalchemy.sql import exists
from models import Subject, Place, TimePlace, DayOfWeek

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
        for tp in self.subject.time_places:
            it = QStandardItem()
            it.setText(tp.place.name)
            self.timeslot_model.setItem(tp.slot, int(tp.day), it)



    def setupUi(self, dialog):
        super().setupUi(dialog)

        self.dialog = dialog

        self.name.setText(self.subject.name)
        self.abbreviation.setText(self.subject.abbreviation)
        self.timeslotView.setModel(self.timeslot_model)

        self.buttonBox.accepted.connect(self.update_subject)

    def update_subject(self):
        self.subject.name = self.name.text()
        self.subject.abbreviation = self.abbreviation.text()
        self.subject.time_places = []

        for i in range(self.timeslot_model.rowCount()):
            for j in range(self.timeslot_model.columnCount()):
                it = self.timeslot_model.item(i, j)
                if it is not None:
                    place = self.session.query(Place).filter(Place.name == it.text()).one_or_none()
                    if place is None:
                        messagebox = QMessageBox()
                        messagebox.setWindowTitle("Create new location?")
                        messagebox.setIcon(QMessageBox.Question)
                        messagebox.setText("Create location {0}".format(it.text()))
                        messagebox.setInformativeText("Location {0} does not exist. Do you want to create it?".format(it.text()))
                        messagebox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        messagebox.setDefaultButton(QMessageBox.Yes)

                        reply = messagebox.exec()
                        if reply == QMessageBox.Yes:
                            place = Place()
                            place.name = it.text()
                            self.session.add(place)
                    if place is not None:
                        tp = TimePlace()
                        tp.day = DayOfWeek(j)
                        tp.slot = i
                        tp.place = place
                        self.subject.time_places.append(tp)

        self.session.add(self.subject)
