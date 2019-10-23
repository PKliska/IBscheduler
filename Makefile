
src/ui/mainwindow.py: ui/mainwindow.ui
	pyuic5 ui/mainwindow.ui -o src/ui/mainwindow.py


ui-files: src/ui/mainwindow.py


all: ui-files
