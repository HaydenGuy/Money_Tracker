import re
from typing import Union

from PySide2.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, 
                               QPushButton, QDialog, QLineEdit, QLabel, QComboBox, QAbstractItemView, QSizePolicy, QHeaderView, QMessageBox, QAction)


# Item object whose information will be used to populate the list
class Item:
    # Define paramaters of a certain type. Union[] allows either option
    def __init__(self, name: str, price: Union[int, float], category: str, cashflow: str):
        # Set self.name to name if paramater is given and name not None/False else set to default of -
        self.name = name if name and name != "" else "-"
        self.price = self.check_if_positive(price)
        self.category = category
        self.cashflow = cashflow

    # Checks if the price is a float based on if a . is present
    def check_if_float(self, price):
        pattern = r'^[^.]*\.[^.]*$'  # Only one . can be present
        if re.search(pattern, price):
            price = float(price)
            return price
        else:
            price = int(price)
            return price
    
    # Checks if the price is positive by checking if it is lower than 0
    def check_if_positive(self, price):
        check_if_float_price = self.check_if_float(price)
        
        if check_if_float_price < 0:
            raise ValueError
        else:
            return check_if_float_price

# Popup box that appears when Add Item button is clicked
class Add_Popup(QDialog):
    def __init__(self, main_ui):  # Pass the main_ui as a parent so that it's data can be accessed
        super().__init__(main_ui)

        self.main_ui_info = main_ui

        self.setWindowTitle("Add Item")
        self.setGeometry(700, 300, 300, 100)

        self.item = None  # Item container to be used when item is object is added

        self.setup_ui()

    def setup_ui(self):
        labels_layout = QVBoxLayout()  # Creates label layout
        name_label = QLabel("Name:     ")  # Label item
        price_label = QLabel("Price:    ")
        category_label = QLabel("Category: ")
        cashflow_label = QLabel("Cashflow: ")
        labels_layout.addWidget(name_label)  # Adds the labels to the layout
        labels_layout.addWidget(price_label)
        labels_layout.addWidget(category_label)
        labels_layout.addWidget(cashflow_label)

        input_layout = QVBoxLayout()  # Creates a layout for the user input items
        # Creates an editable area for the item name
        self.name_box = QLineEdit(self)
        # Creates an editable area for the price
        self.price_box = QLineEdit(self)
        # Adds the line edits to the input layout
        input_layout.addWidget(self.name_box)
        input_layout.addWidget(self.price_box)

        category = ("Wages", "Rent", "Bills", "Subscriptions", "Restaurants",
                    "Groceries", "Household", "Entertainment", "Other")
        self.category_menu = QComboBox()  # Creates a dropdown menu
        # Adds the category list items to the dropdown menu
        self.category_menu.addItems(category)
        # Adds the dropdown to the input layout
        input_layout.addWidget(self.category_menu)

        self.cashflow_menu = QComboBox()  # Creates a dropdown menu
        self.cashflow_menu.addItem("Income")  # Adds item to the dropdown list
        self.cashflow_menu.addItem("Expenditure")
        # Adds the dropdown to the input layout
        input_layout.addWidget(self.cashflow_menu)

        # Creates a layout to hold the labels and input
        labels_input_layout = QHBoxLayout()
        # Adds the label layout to the parent
        labels_input_layout.addLayout(labels_layout)
        # Adds the input layout to the parent
        labels_input_layout.addLayout(input_layout)

        # Creates a button layout to hold the add/cancel buttons
        button_layout = QHBoxLayout()
        add_button = QPushButton("Add", self)
        # Run the on_add function when add is pressed
        add_button.clicked.connect(self.on_add)
        cancel_button = QPushButton("Cancel", self)
        # Run the on_cancel function when cancel is pressed
        cancel_button.clicked.connect(self.on_cancel)
        button_layout.addWidget(add_button)  # Add buttons to the layout
        button_layout.addWidget(cancel_button)

        main_layout = QVBoxLayout()  # Main layout to hold all of the popup specific layouts
        main_layout.addLayout(labels_input_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    # Creates a new item object from the user input and button selection information
    def on_add(self):
        name_input = self.name_box.text()  # The name input text
        price_input = self.price_box.text()  # The price input text
        # The selected category input name
        selected_category = self.category_menu.currentText()
        selected_cashflow = self.cashflow_menu.currentText()  # The selected cashflow input

        # ValueError raised when int/float is not entered into price box. Error popup raised
        try:
            self.item = Item(name_input, price_input, selected_category,
                            selected_cashflow)  # Creates the item object
            self.close()  # Close the window after add is pressed
            self.add_item_to_table(self.item) # Runs the add item to table method over self.item
        except ValueError:
            # Logic to create and display an error popup when letters are entered into the price box
            error_box = QMessageBox()
            error_box.setIcon(QMessageBox.Critical)
            error_box.setWindowTitle("Invalid Entry")
            error_box.setText("Invalid entry.\n\nPlease enter a number 0.0 or greater.\n")
            error_box.setStandardButtons(QMessageBox.Ok)
            error_box.exec_()

    def on_cancel(self):
        self.item = None  # Reset the self.item if cancel is pressed
        self.close()  # If cancel is pressed close the window

    # Adds an item to the table based on information from the item object passed
    def add_item_to_table(self, item: object):
        row_count = self.main_ui_info.table.rowCount()  # Gets the number of rows
        self.main_ui_info.table.insertRow(row_count)  # Adds a row to the table

        # Create a table widget item for name, price and category
        name = QTableWidgetItem(item.name)
        # Convert the price to a str so it can be displayed
        price = QTableWidgetItem(str(item.price))
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
    def __init__(self):  # Initialises the main window for the UI
        super().__init__()

        self.setWindowTitle("Money Tracker")
        self.setGeometry(700, 300, 600, 500)  # x, y, width, height

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.income_total = 0 # Used in the add_to_total method
        self.expenditure_total = 0 # Used in the add_to_total method

        self.setup_menuBar() # Calls the setup_menuBar to create menu header options
        self.setup_ui() # Calls setup_ui to create graphical elements of the UI
        
        # Signals that connect the menu header options to corresponding slot
        self.new_action.triggered.connect(self.new_file)
        self.open_action.triggered.connect(self.open_file)
        self.save_action.triggered.connect(self.save_file)
        self.save_as_action.triggered.connect(self.save_as_file)

        # When add button is clicked the popup method runs
        self.add_button.clicked.connect(self.add_item_popup)
        # Runs the remove item method to remove the selected item
        self.remove_button.clicked.connect(self.remove_item)

    # Creates the menubar with options File->New/Open/Save/SaveAs
    def setup_menuBar(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        self.new_action = QAction("New", self)
        file_menu.addAction(self.new_action)
        self.open_action = QAction("Open..", self)
        file_menu.addAction(self.open_action)
        self.save_action = QAction("Save", self)
        file_menu.addAction(self.save_action)
        self.save_as_action = QAction("Save As..", self)
        file_menu.addAction(self.save_as_action)


    # Creates the graphical elements of the UI
    def setup_ui(self):
        # Initial row boolean will be used to remove the row when first item is added
        self.initial_row = True
        self.table = QTableWidget(1, 4)  # Create a 1x4 table widget
        # Disable the edit triggers on the table so that cells cannot be edited
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setHorizontalHeaderLabels(
            ["Name", "Price", "Category", "Cashflow"])  # Sets column header lable

        # Table will expand to fit the available horizontal/veritcal space when window is resized
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Table headers/cells will stretch uniformly to fit the available space of the table widget which is the window size
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.income_label = QLabel("Income: 0.0") # PLACEHOLDER
        self.expenditure_label = QLabel("Expenditure: 0.0") # PLACEHOLDER

        # Creates add and remove buttons
        self.add_button = QPushButton("Add Item")
        self.remove_button = QPushButton("Remove Item")

        button_h_layout = QHBoxLayout()  # Horizontal layout to hold buttons
        # Add/Remove buttons added to button h layout
        button_h_layout.addWidget(self.add_button)
        button_h_layout.addWidget(self.remove_button)

        # Creates a vertical layout and adds the table widget to it
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.table)
        v_layout.addWidget(self.income_label) # PLACEHOLDER
        v_layout.addWidget(self.expenditure_label) # PLACEHOLDER
        v_layout.addLayout(button_h_layout)
        self.central_widget.setLayout(v_layout)


    def new_file(self):
        ...

    def open_file(self):
        ...

    def save_file(self):
        ...
    
    def save_as_file(self):
        ...

    # Creates a popup window object which allows the user to add items
    def add_item_popup(self):
        popup = Add_Popup(self)
        popup.exec_()
        try:
            self.add_to_total(popup.item.price, popup.item.cashflow) # Runs the add_to_total method with price and cashflow item paramaters
        except AttributeError:
            pass

    # Removes the currently selected row from the table widget
    def remove_item(self):
        try:
            cell = self.table.currentItem() # Gets the selected item from the table
            cell_text = cell.text() # If there is no cell text error is raised. This avoids NoneType errors for empty cells
            row = self.table.currentRow() # Gets the current row value
            self.subtract_from_total(row) # Runs the subtract from total method to update the total displays
            self.table.removeRow(row) # Removes the selected row
            self.table.setCurrentCell(row - 1, 0) # Sets the active cell to the row above the deleted row
        except AttributeError:
            pass
    
    # Adds the price value to the income/expenditure total and updates the displayed value
    def add_to_total(self, price, selected_cashflow):
        if selected_cashflow == "Income": # Adds to income value
            self.income_total += float(price)
            self.income_label.setText(f"Income: {str(self.income_total)}") # PLACEHOLDER
        else: # Adds to expenditure value
            self.expenditure_total += float(price)
            self.expenditure_label.setText(f"Expenditure: {str(self.expenditure_total)}") # PLACEHOLDER

    # Subtracts the price value from the income/expenditure total and updates the displayed value 
    def subtract_from_total(self, row):
        price_item = self.table.item(row, 1) # Gets the price QTableWidgetItem
        price = price_item.text() # Gets the price text
        cashflow_item = self.table.item(row, 3) # Gets the cashflow QTableWidgetItem
        selected_cashflow = cashflow_item.text() # Gets the cashflow text

        if selected_cashflow == "Income": # Subtracts from income value
            self.income_total -= float(price)
            self.income_label.setText(f"Income: {str(self.income_total)}") # PLACEHOLDER
        else: # Subtracts from expenditure value
            self.expenditure_total -= float(price)
            self.expenditure_label.setText(f"Expenditure: {str(self.expenditure_total)}") # PLACEHOLDER