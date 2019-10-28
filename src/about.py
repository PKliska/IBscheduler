from ui.about import Ui_About
import config

class About(Ui_About):

    def __init__(self):
        super().__init__()

    def setupUi(self, dialog):
        super().setupUi(dialog)

    def retranslateUi(self, dialog):
        super().retranslateUi(dialog)
        self.version.setText(self.version.text().format(config.VERSION))
