from PySide2.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton

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

        # Horizontal layout to hold buttons
        button_h_layout = QHBoxLayout() 
        add_button = QPushButton("Add Item")
        remove_button = QPushButton("Remove Item")
        button_h_layout.addWidget(add_button) # Add/Remove buttons added to button h layout
        button_h_layout.addWidget(remove_button)
        
        # Creates a vertical layout and adds the table widget to it
        v_layout = QVBoxLayout()
        v_layout.addWidget(table)
        v_layout.addLayout(button_h_layout)
        self.central_widget.setLayout(v_layout)