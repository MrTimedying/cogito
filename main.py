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
        
        # Connect action widget signals
        self.action_widget.action_triggered.connect(self.handle_action)
    
    def set_mode(self, mode):
        """
        Set the application mode based on the selected menu option
        
        Args:
            mode (str): One of 'execute', 'ongoing_research', 'archive_research'
        """
        print(f"Switching to mode: {mode}")
        
        # Update the main workspace
        self.main_workspace.set_mode(mode)
        
        # Clear and update action suggestions based on the mode
        self.action_widget.clear_suggestions()
        
        # Add example actions based on the selected mode
        if mode == "execute":
            self.action_widget.add_suggestion("Start new execution")
            self.action_widget.add_suggestion("Load previous execution")
        elif mode == "ongoing_research":
            self.action_widget.add_suggestion("Create new research")
            self.action_widget.add_suggestion("Continue existing research")
        elif mode == "archive_research":
            self.action_widget.add_suggestion("Browse archives")
            self.action_widget.add_suggestion("Search archives")
    
    def handle_action(self, action_text):
        """
        Handle actions triggered from the action panel
        
        Args:
            action_text (str): The text of the action that was triggered
        """
        print(f"Action triggered: {action_text}")
        # This will be expanded to handle different actions

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # More consistent cross-platform look
    window = MainWindow()
    window.show()
    sys.exit(app.exec()) 