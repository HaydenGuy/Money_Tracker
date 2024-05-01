import re
from typing import Union

from PySide2.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, 
                               QPushButton, QDialog, QLineEdit, QLabel, QRadioButton, QComboBox, QButtonGroup, QAbstractItemView)

# Item object whose information will be used to populate the list
class Item:
    def __init__(self, name: str, price: Union[int, float], category: str, cashflow: str): # Define paramaters of a certain type. Union[] allows either option
        self.name = name
        self.price = self.check_if_float(price)
        self.category = category
        self.cashflow = cashflow

    def check_if_float(self, price): # Checks if the price is a float based on if a . is present
        pattern = r'^[^.]*\.[^.]*$' # Only one . can be present
        if re.search(pattern, price):
            price = float(price)
            return price
        else:
            price = int(price)
            return price

# Popup box that appears when Add Item button is clicked
class Add_Popup(QDialog):
    def __init__(self, main_ui): # Pass the main_ui as a parent so that it's data can be accessed
        super().__init__(main_ui)

        self.main_ui_info = main_ui

        self.setWindowTitle("Add Item")
        self.setGeometry(700, 300, 300, 100)

        self.item = None # Item container to be used when item is object is added

        self.setup_ui()
        
    def setup_ui(self):
        labels_layout = QVBoxLayout() # Creates label layout
        name_label = QLabel("Name:     ") # Label item
        price_label = QLabel("Price:    ")
        category_label = QLabel("Category: ")
        cashflow_label = QLabel("Cashflow: ")
        labels_layout.addWidget(name_label) # Adds the labels to the layout
        labels_layout.addWidget(price_label)
        labels_layout.addWidget(category_label)
        labels_layout.addWidget(cashflow_label)
        
        input_layout = QVBoxLayout() # Creates a layout for the user input items
        self.name_box = QLineEdit(self) # Creates an editable area for the item name
        self.price_box = QLineEdit(self) # Creates an editable area for the price
        input_layout.addWidget(self.name_box) # Adds the line edits to the input layout
        input_layout.addWidget(self.price_box)

        category = ("Rent", "Bills", "Subscriptions", "Restaurants", "Groceries", "Household", "Entertainment", "Other")
        self.category_menu = QComboBox() # Creates a dropdown menu
        self.category_menu.addItems(category) # Adds the category list items to the dropdown menu
        input_layout.addWidget(self.category_menu) # Adds the dropdown to the input layout

        self.cashflow_menu = QComboBox() # Creates a dropdown menu
        self.cashflow_menu.addItem("Income") # Adds item to the dropdown list
        self.cashflow_menu.addItem("Expenditure")
        input_layout.addWidget(self.cashflow_menu) # Adds the dropdown to the input layout

        labels_input_layout = QHBoxLayout() # Creates a layout to hold the labels and input
        labels_input_layout.addLayout(labels_layout) # Adds the label layout to the parent
        labels_input_layout.addLayout(input_layout) # Adds the input layout to the parent

        button_layout = QHBoxLayout() # Creates a button layout to hold the add/cancel buttons
        add_button = QPushButton("Add", self)
        add_button.clicked.connect(self.on_add) # Run the on_add function when add is pressed
        cancel_button = QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.on_cancel) # Run the on_cancel function when cancel is pressed
        button_layout.addWidget(add_button) # Add buttons to the layout
        button_layout.addWidget(cancel_button)
        
        main_layout = QVBoxLayout() # Main layout to hold all of the popup specific layouts
        main_layout.addLayout(labels_input_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    # Creates a new item object from the user input and button selection information
    def on_add(self):
        name_input = self.name_box.text() # The name input text
        price_input = self.price_box.text() # The price input text 
        selected_category = self.category_menu.currentText() # The selected category input name
        selected_cashflow = self.cashflow_menu.currentText() # The selected cashflow input  
        self.item = Item(name_input, price_input, selected_category, selected_cashflow) # Creates the item object
        self.close() # Close the window after add is pressed
        self.add_item_to_table(self.item) # Runs the money tracker add item to table method over self.item
    
    def on_cancel(self):
        self.item = None # Reset the self.item if cancel is pressed
        self.close() # If cancel is pressed close the window

    # Adds an item to the table based on information from the item object passed
    def add_item_to_table(self, item: object):
        row_count = self.main_ui_info.table.rowCount() # Gets the number of rows
        self.main_ui_info.table.insertRow(row_count) # Adds a row to the table

        # Create a table widget item for name, price and category
        name = QTableWidgetItem(item.name) 
        price = QTableWidgetItem(str(item.price)) # Convert the price to a str so it can be displayed
        category = QTableWidgetItem(item.category)
        cashflow = QTableWidgetItem(item.cashflow)

        # Add the table widget items to the table in columns 1-4 
        self.main_ui_info.table.setItem(row_count, 0, name) 
        self.main_ui_info.table.setItem(row_count, 1, price) 
        self.main_ui_info.table.setItem(row_count, 2, category)
        self.main_ui_info.table.setItem(row_count, 3, cashflow)

        # Checks the initial_row boolean and if it is True it will remove the initial empty row and set the value to False
        if self.main_ui_info.initial_row == True:
            self.main_ui_info.table.removeRow(0)
            self.main_ui_info.initial_row = False
        
class Money_Tracker(QMainWindow):
    def __init__(self): # Initialises the main window for the UI
        super().__init__()
        
        self.setWindowTitle("Money Tracker")
        self.setGeometry(700, 300, 600, 500) # x, y, width, height

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.setup_ui()
        
        self.add_button.clicked.connect(self.add_item_popup) # When add button is clicked the popup method runs
        # self.remove_button.clicked.connect(self.remove_item) # Runs the remove item method to remove the selected item

    # Creates the graphical elements of the UI
    def setup_ui(self):
        self.initial_row = True # Initial row boolean will be used to remove the row when first item is added
        self.table = QTableWidget(1, 4) # Create a 1x4 table widget
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers) # Disable the edit triggers on the table so that cells cannot be edited
        self.table.setHorizontalHeaderLabels(["Name", "Price", "Category", "Cashflow"]) # Sets column header lable

        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 150)

        # Creates add and remove buttons
        self.add_button = QPushButton("Add Item")
        self.remove_button = QPushButton("Remove Item")

        button_h_layout = QHBoxLayout() # Horizontal layout to hold buttons
        button_h_layout.addWidget(self.add_button) # Add/Remove buttons added to button h layout
        button_h_layout.addWidget(self.remove_button)
        
        # Creates a vertical layout and adds the table widget to it
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.table)
        v_layout.addLayout(button_h_layout)
        self.central_widget.setLayout(v_layout)

    # Creates a popup window object which allows the user to add items
    def add_item_popup(self):
        popup = Add_Popup(self)
        popup.exec_()

    # def remove_item(self, item):
