

all: ui-files

src/ui/mainwindow.py: ui/mainwindow.ui
	pyuic5 ui/mainwindow.ui -o src/ui/mainwindow.py

src/ui/edit_student.py: ui/edit_student.ui
		pyuic5 ui/edit_student.ui -o src/ui/edit_student.py

ui-files: src/ui/mainwindow.py src/ui/edit_student.py



