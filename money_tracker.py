import sys

from typing import Union
from PySide2.QtWidgets import QApplication
from modules import main_ui # Imports the UI module

class Item:
    def __init__(self, name: str, price: Union[int, float], category: str): # Define paramaters of a certain type. Union[] allows either option
        self.name = name
        self.price = price
        self.valid_category(category) # Runs the valid category function on the category and sets self.category if valid
        self.category = category

    # Check that the category is in the list of valid options and return ValueError if not
    def valid_category(self, category: str):
        valid_options = ("RENT", "GROCERIES", "BILLS", "SUBSCRIPTIONS", "HOUSEHOLD", "RESTAURANTS", "ENTERTAINMENT", "OTHER")
        if category not in valid_options:
            raise ValueError(f"Invalid category: {category}\nValid categories: {valid_options}")


test_item = Item("Food", 50.0, "GROCERIES")
test_item2 = Item("Phone", 27, "BILLS")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = main_ui.Money_Tracker() # Creates a Money_Tracker object from the main_ui module
    window.show()

    sys.exit(app.exec_())