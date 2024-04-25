import sys

from PySide2.QtWidgets import QApplication
from modules import UI # Imports the UI module

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = UI.Money_Tracker() # Creates a Money_Tracker object from the main_ui module
    window.show()

    sys.exit(app.exec_())