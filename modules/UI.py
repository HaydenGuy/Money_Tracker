import re
from typing import Union

from PySide2.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                               QTableWidgetItem, QPushButton, QDialog, QLineEdit, QLabel, QRadioButton, QButtonGroup)

# Item object whose information will be used to populate the list
class Item:
    def __init__(self, name: str, price: Union[int, float], category: str): # Define paramaters of a certain type. Union[] allows either option
        self.name = name
        self.price = self.check_if_float(price)
        self.category = category

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

        # Sends a signal to the selected_button function when a radio button is clicked
        self.radio_button_group.buttonClicked.connect(self.selected_button)
        
    def setup_ui(self):
        labels_layout = QVBoxLayout() # Creates label layout and add labels to it
        name_label = QLabel("Name:  ")
        price_label = QLabel("Price: ")
        labels_layout.addWidget(name_label)
        labels_layout.addWidget(price_label)

        box_layout = QVBoxLayout() # Create layout for line edit boxes and add line edits to it
        self.name_box = QLineEdit(self)
        self.price_box = QLineEdit(self)
        box_layout.addWidget(self.name_box)
        box_layout.addWidget(self.price_box)

        input_layout = QHBoxLayout() # Create layout to hold the labels and line edits
        input_layout.addLayout(labels_layout)
        input_layout.addLayout(box_layout)

        button_layout = QHBoxLayout() # Creates a button layout to hold the add/cancel buttons
        add_button = QPushButton("Add", self)
        add_button.clicked.connect(self.on_add) # Run the on_add function when add is pressed
        cancel_button = QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.on_cancel) # Run the on_cancel function when cancel is pressed
        button_layout.addWidget(add_button) # Add buttons to the layout
        button_layout.addWidget(cancel_button)

        radio_layout_left = QVBoxLayout() # Create layouts to hold the radio buttons
        radio_layout_right = QVBoxLayout()
        radio_layout = QHBoxLayout()
        self.category = ("Rent", "Bills", "Subscriptions", "Restaurants", "Groceries", "Household", "Entertainment", "Other") # Radio button options
        self.radio_button_group = QButtonGroup() # Container to hold the radio buttons
        
        # Iterate through the category list and create a radio button based on the cat
        for i, cat in enumerate(self.category):
            button = QRadioButton(cat)
            self.radio_button_group.addButton(button, i) # Add the radio button to the radio button group
            if i < 4: # Add the button the radio layout left if i less than 3
                radio_layout_left.addWidget(button)
            else:
                radio_layout_right.addWidget(button)
        
        radio_layout.addLayout(radio_layout_left) # Add radio left/right layouts to the main radio layout
        radio_layout.addLayout(radio_layout_right) 
        
        main_layout = QVBoxLayout() # Main layout to hold all of the popup specific layouts
        main_layout.addLayout(input_layout) # Adds the popup specific layouts to main layout
        main_layout.addLayout(radio_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    # Returns the name of the selected button 
    def selected_button(self):
        selected_category = self.category[self.radio_button_group.checkedId()]
        
        return selected_category

    # Creates a new item object from the user input and button selection information
    def on_add(self):
        name_input = self.name_box.text() # The name input text
        price_input = self.price_box.text() # The price input text 
        selected_category = self.selected_button() # The category input name
        self.item = Item(name_input, price_input, selected_category) # Creates the item object
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

        # Add the table widget items to the table in columns 0, 1, 2 respectively
        self.main_ui_info.table.setItem(row_count, 0, name) 
        self.main_ui_info.table.setItem(row_count, 1, price) 
        self.main_ui_info.table.setItem(row_count, 2, category) 

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
        self.table = QTableWidget(1, 3) # Create a 1x3 table widget
        self.table.setHorizontalHeaderLabels(["Name", "Price", "Category"]) # Sets column header lable

        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 150)

        # Creates add and remove buttons
        add_button = QPushButton("Add Item")
        add_button.clicked.connect(self.add_item_popup) # When add button is clicked the popup function runs
        remove_button = QPushButton("Remove Item")

        button_h_layout = QHBoxLayout() # Horizontal layout to hold buttons
        button_h_layout.addWidget(add_button) # Add/Remove buttons added to button h layout
        button_h_layout.addWidget(remove_button)
        
        # Creates a vertical layout and adds the table widget to it
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.table)
        v_layout.addLayout(button_h_layout)
        self.central_widget.setLayout(v_layout)

    # Creates a popup window object which allows the user to add items
    def add_item_popup(self):
        popup = Add_Popup(self)
        popup.exec_()