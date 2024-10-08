import re
import csv
import os

from typing import Union
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
                               QPushButton, QDialog, QLineEdit, QLabel, QComboBox, QAbstractItemView, QSizePolicy, 
                               QHeaderView, QMessageBox, QFileDialog)
from PySide6.QtGui import QAction

# Creates an error window popup
def create_error_window(title, text):
    error_box = QMessageBox()
    error_box.setIcon(QMessageBox.Critical)
    error_box.setWindowTitle(f"{title}") 
    error_box.setText(f"{text}")
    error_box.setStandardButtons(QMessageBox.Ok) # Gives an ok button for the user to press
    error_box.exec_()

# Item object whose information will be used to populate the list
class Item:

    categories = ("wages", "rent", "bills", "subscriptions", "restaurants",
                    "groceries", "household", "entertainment", "other")
    
    # Define paramaters of a certain type. Union[] allows either option
    def __init__(self, name: str, price: Union[int, float], category: str, cashflow: str):
        self.name = name.strip() if name and name != "" else "-" # Trailing whitespace removed from name and set to name or default of - 
        self.price = self.check_if_positive(price)
        self.category = self.check_category(category)
        self.cashflow = self.check_cashflow(cashflow)

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
            raise ValueError("Expected a positive number")
        else:
            return check_if_float_price
    
    # Checks if the category passed is in the list of categories
    def check_category(self, category):
        cat = category.strip() # Removes trailing and leading whitespace
        if cat.lower() in self.categories:
            return cat.lower().capitalize() # Return capitalized version of category
        else:
            raise ValueError("Expected categories: Wages, Rent, Bills, Subscriptions, Restaurants, Groceries, Household, Entertainment, Other")

    # Checks if the cashflow passed is income or expenditure
    def check_cashflow(self, cashflow):
        cash = cashflow.strip() # Removes trailing and leading whitespace
        if cash.lower() == "income" or cash.lower() == "expenditure":
            return cash.lower().capitalize() # Return capitalized version of cashflow
        else:
            raise ValueError("Expected: Income or Expenditure")

# Popup box that appears when Add Item button is clicked
class Add_Popup(QDialog):
    def __init__(self):
        super().__init__()

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
            return self.item
        except ValueError: # Display an error popup when numbers are not entered into the price box
            create_error_window("Invalid Entry", "Please enter a number 0.0 or greater")
            
    def on_cancel(self):
        self.item = None  # Reset the self.item if cancel is pressed
        self.close()  # If cancel is pressed close the window


class Money_Tracker(QMainWindow):
    def __init__(self):  # Initialises the main window for the UI
        super().__init__()

        self.active_window = [] # List to store the active window
        self.active_file_path = "" # String to store the active file path

        self.setWindowTitle("Money Tracker - untitled")
        self.setGeometry(700, 300, 600, 500)  # x, y, width, height

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.income_total = 0 # Used in the add_to_total method
        self.expenditure_total = 0 # Used in the add_to_total method

        self.rows_added = 0 # Used in save method

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

        # QAction creates the actions and addAction adds to the menubar
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

        self.income_label = QLabel("Income: 0.0") 
        self.expenditure_label = QLabel("Expenditure: 0.0") 

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
        v_layout.addWidget(self.income_label)
        v_layout.addWidget(self.expenditure_label) 
        v_layout.addLayout(button_h_layout)
        self.central_widget.setLayout(v_layout)

    # Closes the active UI and creates a new UI when the New button is selected 
    def new_file(self):
        self.close() # Closes active window
        new_ui = Money_Tracker() # Create new instance of Money_Tracker and show it
        new_ui.show()
        self.active_window.append(new_ui) # Add the new_ui to the active window list. Without this the app will close and destroy() will run behind the scenes
        self.active_file_path = "" # Resets the active file path variable

    # Creates a file explorer window to allow the user to choose a CSV
    def open_file_explorer(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("CSV files (*.csv)") # Allows only .csv
        file_dialog.setWindowTitle("Select a CSV file to open")
        file_dialog.setFileMode(QFileDialog.ExistingFile) # Ensures the file selected exists

        # If the user selects a file it is given a list of files and returns index 0 which is the selected file path
        if file_dialog.exec():
            self.selected_csv = file_dialog.selectedFiles()[0]
            self.active_file_path = self.selected_csv # Sets the active file path variable to the opened file path

    # Reads a csv file from the file_path and return a list of items
    def read_csv_file(self, file_path):
        item_list = []
        with open(file_path, mode='r') as file: # Opens in read mode as file
            csv_reader = csv.reader(file) # Reads the file
            for row in csv_reader: # Gets the rows in the csv_reader
                if any(row): # If a row exist (is not empty)
                    item = Item(*row) # Unpacks the rows to pass information to the Item class
                    item_list.append(item)
        return item_list
    
    # Reads the csv file and checks if the last line is a newline/empty row. If not it adds one
    def check_for_newline(self, csv_file):
        # Open the file in read-write binary mode
        with open(csv_file, "r+b") as file:
            file.seek(0, os.SEEK_END)  # Move the pointer to the end of the file
            if file.tell() == 0:  # Check if the file is empty
                needs_newline = False
            else:
                file.seek(-1, os.SEEK_END)  # Move the pointer to the last byte
                last_char = file.read(1)
                needs_newline = last_char != b'\n'  # Check if the last character is not a newline
            
            if needs_newline:
                file.write(b'\n')  # Write a newline character if it's not there

    # Writes all the lines in the table to a csv_file
    def write_rows_to_csv(self, csv_writer):
        for row in range(self.table.rowCount()):
            name = self.table.item(row, 0).text() # Gets the text value for each cell in the row
            price = self.table.item(row, 1).text()
            category = self.table.item(row, 2).text()
            cashflow = self.table.item(row, 3).text()
            csv_writer.writerow([name, price, category, cashflow]) # Write the items to the csv rows
            
    # Creates a question window to confirm if you want to save the file
    def save_file_question_window(self, title, text):
        question_box = QMessageBox()
        question_box.setIcon(QMessageBox.Question)
        question_box.setWindowTitle(f"{title}") 
        question_box.setText(f"{text}")
        question_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No) # Gives yes or no buttons
        user_selection = question_box.exec_() # Will retrieve the selected yes or no

        if user_selection == QMessageBox.Yes:
            return True
        else:
            return False
        
    # Opens a selected csv file
    def open_file(self):
        window_title = self.windowTitle()

        # Checks if the current file has unsaved information and runs the save file method before opening new file if user selects to save
        if window_title[-1] == "*":
            user_selection = self.save_file_question_window("Unsaved File", "Would you like to save the current file before opening?")
            
            if user_selection == True:
                self.save_file()
            else:
                pass
        
        self.open_file_explorer() # Opens the file explorer
            
        try: # Get the item_list from read_csv_file
            items = self.read_csv_file(self.selected_csv)
        except ValueError: # Error window if the information in the CSV does not align with expected
            create_error_window("Invalid CSV", "Information in the CSV does not match expected format:\n\nName,Price,Category,Cashflow")
        except AttributeError: # Do nothing if the user hits cancel
            pass
        except TypeError: # When an empty CSV is opened
            self.table.setRowCount(0) # Remove all rows from the table before opening the file
            self.income_total = 0 # Reset total values
            self.expenditure_total = 0
            self.income_label.setText("Income: 0.0") # Reset label text
            self.expenditure_label.setText("Expenditure: 0.0")
            file_name = os.path.basename(self.selected_csv) # Gets the file name.csv
            self.setWindowTitle(f"Money Tracker - {file_name}") # Sets the window title to the file name
        else:
            self.table.setRowCount(0) # Remove all rows from the table before opening the file
            self.income_total = 0 # Reset total values
            self.expenditure_total = 0
            self.initial_row = False # False means the first line wont be deleted, is used when adding to empty table
            file_name = os.path.basename(self.selected_csv) # Gets the file name.csv
            self.setWindowTitle(f"Money Tracker - {file_name}") # Sets the window title to the file name
            for item in items: # Iterates through the items list
                self.add_to_total(item.price, item.cashflow) # Updates the total information
                self.add_item_to_table(item) # Adds the items to the table

    # Saves an exisitng csv file or save_as if it's a new file
    def save_file(self):
        window_title = self.windowTitle() # Gets window title
        untitled = "Money Tracker - untitled" # Default window titles with/without changes
        untitled_changes = "Money Tracker - untitled*"

        # Runs save_as if the file has yet to be named and saved
        if window_title == untitled or window_title == untitled_changes:
            self.save_as_file()
        
        # Runs the save file question window and if No nothing happens
        overwrite = self.save_file_question_window("Save File", "Are you sure you want to overwrite the existing data?")

        if overwrite == False:
            pass
        else: # If user selects Yes from question window the file is overwritten
            self.check_for_newline(self.active_file_path) # Checks if for an empty line/row at the end of the csv file

            with open (self.active_file_path, mode='w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)

                try:
                    self.write_rows_to_csv(csv_writer) # Writes all rows from the table to the active csv_file
                except AttributeError:
                    pass
            
            # Resets the title by removing the *
            title = self.windowTitle()[:-1]
            self.setWindowTitle(title)

    # Saves a user named csv file
    def save_as_file(self):
        # Parent, window title, directory ("" is default), file filter, -  _ returns the filter
        file_name, _ = QFileDialog.getSaveFileName(self, 
                                                   "Save CSV File", 
                                                   "", 
                                                   "CSV Files (*.csv)")
        
        # Checks if a .csv appears at the end of the file_name and adds one if it is not present
        pattern = r'\.csv$'
        if not re.search(pattern, file_name):
            file_name += ".csv"
        
        if file_name:
            with open(file_name, 'w', newline='') as csv_file: # Open file for writing, ensure consistent line endings, automatically close file
                csv_writer = csv.writer(csv_file) # Create a CSV writer object linked to the opened file for writing

                try:
                    self.write_rows_to_csv(csv_writer) # Writes all rows from the table to the file_name csv file
                except AttributeError:
                    csv_writer.writerow([])
        
        self.active_file_path = file_name # Sets the active file path variable to the saved file path
        file = os.path.basename(file_name) # Gets just the file name not the whole path
        self.setWindowTitle(f"Money Tracker - {file}") # Sets the window title to the file name

    # Creates a popup window object which allows the user to add items
    def add_item_popup(self):
        popup = Add_Popup()
        popup.exec_()
        try:
            self.add_to_total(popup.item.price, popup.item.cashflow) # Runs the add_to_total method with price and cashflow item paramaters
            self.add_item_to_table(popup.item) # Runs the add_item_to_table method to add the new item to the table
            self.check_if_saved() # Checks if there is a * at the end of the window title and adds one if it is not present
            self.rows_added += 1 # Adds +1 to the rows added variable
        except AttributeError: # Does nothing when the user hits cancel
            pass

    # Adds an item to the table based on information from the item object passed
    def add_item_to_table(self, item: object):
        row_count = self.table.rowCount()  # Gets the number of rows
        self.table.insertRow(row_count)  # Adds a row to the table

        # Gets the data that will be populate a cell from the Item class and stores it in a list
        data = [item.name, str(item.price), item.category, item.cashflow]

        # Iterate through the data list and create QTableWidgetItem for each piece of data
        for column, cell_data in enumerate(data):
            item = QTableWidgetItem(cell_data)
            self.table.setItem(row_count, column, item) # Add the item to the row/column

        # Checks the initial_row boolean and if it is True it will remove the initial empty row and set the value to False
        if self.initial_row == True:
            self.table.removeRow(0)
            self.initial_row = False

    # Removes the currently selected row from the table widget
    def remove_item(self):
        try:
            cell = self.table.currentItem() # Gets the selected item from the table
            cell_text = cell.text() # If there is no cell text error is raised. This avoids NoneType errors for empty cells
            row = self.table.currentRow() # Gets the current row value
            self.subtract_from_total(row) # Runs the subtract from total method to update the total displays
            self.table.removeRow(row) # Removes the selected row
            self.table.setCurrentCell(row - 1, 0) # Sets the active cell to the row above the deleted row
            self.check_if_saved() # Checks if there is a * at the end of the window title and adds one if it is not present
            self.rows_added -= 1 if self.rows_added > 0 else 0 # -1 from the rows_added if button is pressed and rows added is over 0
        except: # Raise error window when removing empty cells or when no cells are available to remove
            create_error_window("Empty Cells", "No items to remove")
    
    # Adds the price value to the income/expenditure total and updates the displayed value
    def add_to_total(self, price, selected_cashflow):
        if selected_cashflow.lower() == "income": # Adds to income value
            self.income_total += float(price)
            self.income_label.setText(f"Income: {str(self.income_total)}")
        else: # Adds to expenditure value
            self.expenditure_total += float(price)
            self.expenditure_label.setText(f"Expenditure: {str(self.expenditure_total)}")

    # Subtracts the price value from the income/expenditure total and updates the displayed value 
    def subtract_from_total(self, row):
        price_item = self.table.item(row, 1) # Gets the price QTableWidgetItem
        price = price_item.text() # Gets the price text
        cashflow_item = self.table.item(row, 3) # Gets the cashflow QTableWidgetItem
        selected_cashflow = cashflow_item.text() # Gets the cashflow text

        if selected_cashflow == "Income": # Subtracts from income value
            self.income_total -= float(price)
            self.income_label.setText(f"Income: {str(self.income_total)}")
        else: # Subtracts from expenditure value
            self.expenditure_total -= float(price)
            self.expenditure_label.setText(f"Expenditure: {str(self.expenditure_total)}")

    # If there is not a * at the end of the window title, adds one to indicate file has unsaved changes
    def check_if_saved(self):
        title = self.windowTitle()
        pattern = r'\*$'
        if not re.search(pattern, title):
            self.setWindowTitle(f"{title}*")