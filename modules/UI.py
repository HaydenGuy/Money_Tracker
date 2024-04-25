from PySide2.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                               QTableWidgetItem, QPushButton, QDialog, QLineEdit, QLabel, QRadioButton)

# Popup box that appears when Add Item button is clicked
class Add_Popup(QDialog):
    def __init__(self, parent=None): # Defining that there is no parent for clarity
        super().__init__(parent)

        self.setWindowTitle("Add Item")
        self.setGeometry(700, 300, 300, 100)

        self.setup_ui()
        
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
        category_left = ("Rent", "Bills", "Subscriptions", "Restaurants") # Radio button options
        category_right = ("Groceries", "Household", "Entertainment", "Other")
        radio_buttons_left = [radio_layout_left.addWidget(QRadioButton(i)) for i in category_left] # Add radio buttons to the left layout based on category list
        radio_buttons_right = [radio_layout_right.addWidget(QRadioButton(i)) for i in category_right] # Add radio buttons to the right layout based on category list
        radio_layout.addLayout(radio_layout_left) # Add radio left/right layouts to the main radio layout
        radio_layout.addLayout(radio_layout_right)

        main_layout = QVBoxLayout() # Main layout to hold all of the popup specific layouts
        main_layout.addLayout(input_layout) # Adds the popup specific layouts to main layout
        main_layout.addLayout(radio_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def on_add(self):
        name_input = self.name_box.text()
        price_input = self.price_box.text()
        self.close() # Close the window after add is pressed

    def on_cancel(self):
        self.close() # If cancel is pressed close the window

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
        table = QTableWidget(2, 2) # Create a 2x2 placeholder table
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

        # Creates add and remove buttons
        add_button = QPushButton("Add Item")
        add_button.clicked.connect(self.add_item_popup) # When add button is clicked the popup function runs
        remove_button = QPushButton("Remove Item")

        button_h_layout = QHBoxLayout() # Horizontal layout to hold buttons
        button_h_layout.addWidget(add_button) # Add/Remove buttons added to button h layout
        button_h_layout.addWidget(remove_button)
        
        # Creates a vertical layout and adds the table widget to it
        v_layout = QVBoxLayout()
        v_layout.addWidget(table)
        v_layout.addLayout(button_h_layout)
        self.central_widget.setLayout(v_layout)

    # Creates an Add Popup object which allows the user to add items
    def add_item_popup(self):
        popup = Add_Popup(self)
        popup.exec_()