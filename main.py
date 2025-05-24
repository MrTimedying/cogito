import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QSplitter
from PySide6.QtCore import Qt, QSize

from components.menu_widget import MenuWidget
from components.main_workspace import MainWorkspace
from components.action_widget import ActionWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Cogito Application")
        self.setMinimumSize(QSize(1000, 600))
        
        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #282c34;
                color: #abb2bf;
            }
        """)
        
        # Create the main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Create horizontal layout for the three panels
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create a splitter to allow resizing of panels
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Menu
        self.menu_widget = MenuWidget()
        
        # Center panel - Main workspace
        self.main_workspace = MainWorkspace()
        
        # Right panel - Action widget
        self.action_widget = ActionWidget()
        
        # Add widgets to the splitter
        splitter.addWidget(self.menu_widget)
        splitter.addWidget(self.main_workspace)
        splitter.addWidget(self.action_widget)
        
        # Set initial sizes for the splitter
        splitter.setSizes([200, 600, 200])
        
        # Add the splitter to the main layout
        main_layout.addWidget(splitter)
        
        # Connect signals
        self.connect_signals()
        
        # Default to execute mode
        self.set_mode("execute")
    
    def connect_signals(self):
        """Connect signals between components"""
        # Connect menu button signals to mode changes
        self.menu_widget.execute_clicked.connect(lambda: self.set_mode("execute"))
        self.menu_widget.ongoing_research_clicked.connect(lambda: self.set_mode("ongoing_research"))
        self.menu_widget.archive_research_clicked.connect(lambda: self.set_mode("archive_research"))
    
    def set_mode(self, mode):
        """
        Set the application mode based on the selected menu option
        
        Args:
            mode (str): One of 'execute', 'ongoing_research', 'archive_research'
        """
        print(f"Switching to mode: {mode}")
        
        # Update the main workspace
        self.main_workspace.set_mode(mode)
    
    def handle_action(self, action_text):
        """
        Handle actions triggered from the action panel
        
        Args:
            action_text (str): The text of the action that was triggered
        """
        print(f"Action triggered: {action_text}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # More consistent cross-platform look
    window = MainWindow()
    window.show()
    sys.exit(app.exec()) 