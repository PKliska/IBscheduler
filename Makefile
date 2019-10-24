
src/ui/mainwindow.py: ui/mainwindow.ui
	pyuic5 ui/mainwindow.ui -o src/ui/mainwindow.py

src/ui/add_student.py: ui/add_student.ui
		pyuic5 ui/add_student.ui -o src/ui/add_student.py

ui-files: src/ui/mainwindow.py src/ui/add_student.py


all: ui-files
