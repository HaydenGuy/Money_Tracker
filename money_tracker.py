import sys

from typing import Union
from PySide2.QtWidgets import QApplication
from modules import UI # Imports the UI module

class Item:
    def __init__(self, name: str, price: Union[int, float]): # Define paramaters of a certain type. Union[] allows either option
        self.name = name
        self.price = price

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = UI.Money_Tracker() # Creates a Money_Tracker object from the main_ui module
    window.show()

    sys.exit(app.exec_())