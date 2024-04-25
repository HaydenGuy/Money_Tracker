import sys

from typing import Union
from PySide2.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit

class Money_Tracker(QMainWindow):
    def __init__(self): # Initialises the main window for the UI
        super().__init__()
        
        self.setWindowTitle("Money Tracker")
        self.setGeometry(700, 300, 500, 500) # x, y, width, height

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.setup_ui()

    # Creates the graphical elements of the UI
    def setup_ui(self):
        button_layout = QHBoxLayout() # Horizontal layout to hold buttons
        add_button = QPushButton("Add Item") # Add button
        remove_button = QPushButton("Remove Item") # Remove button
        button_layout.addWidget(add_button) # Add/Remove buttons added to button layout
        button_layout.addWidget(remove_button)

        table = QTableWidget(2, 2) # Create a 2x2 table
        table.setHorizontalHeaderLabels(["Price", "Category"]) # Sets column header lable
        table.setVerticalHeaderLabels(["ITEM_NAME", "ITEM_NAME"]) # Sets row lable

        item1 = QTableWidgetItem("1000")  # Placeholder item
        item2 = QTableWidgetItem("50")  # Placeholder item
        item3 = QTableWidgetItem("RENT")  # Placeholder item
        item4 = QTableWidgetItem("PHONE")  # Placeholder item

        table.setItem(0, 0, item1) # Placeholder item
        table.setItem(1, 0, item2) # Placeholder item
        table.setItem(0, 1, item3) # Placeholder item
        table.setItem(1, 1, item4) # Placeholder item

        table.setColumnWidth(0, 100)
        table.setColumnWidth(1, 150)
        
        # Creates a vertical layout and adds the table widget to it
        v_layout = QVBoxLayout()
        v_layout.addWidget(table)
        v_layout.addLayout(button_layout)
        self.central_widget.setLayout(v_layout)


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

    window = Money_Tracker()
    window.show()

    sys.exit(app.exec_())