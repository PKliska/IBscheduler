

all: executable

src/ui/mainwindow.py: ui/mainwindow.ui
	pyuic5 ui/mainwindow.ui -o src/ui/mainwindow.py

src/ui/about.py: ui/about.ui
	pyuic5 ui/about.ui -o src/ui/about.py

src/ui/edit_student.py: ui/edit_student.ui
	pyuic5 ui/edit_student.ui -o src/ui/edit_student.py

src/ui/edit_subject.py: ui/edit_subject.ui
	pyuic5 ui/edit_subject.ui -o src/ui/edit_subject.py


executable: ui-files
	pyinstaller src/main.py -w -n "IB scheduler"

ui-files: src/ui/mainwindow.py src/ui/edit_student.py src/ui/edit_subject.py src/ui/about.py
    
