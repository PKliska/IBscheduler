import os,sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from mainwindow import MainWindow


if __name__=='__main__':
    app = QApplication(sys.argv)
    main_window = QMainWindow()

    ui = MainWindow()
    ui.setupUi(main_window)

    main_window.show()

    sys.exit(app.exec_())
