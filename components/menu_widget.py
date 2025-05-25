from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Signal, Qt

class MenuWidget(QWidget):
    """
    Left panel widget that contains menu options for the different functionality modes.
    """
    execute_clicked = Signal()
    ongoing_research_clicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set Cursor-like dark theme colors
        self.setStyleSheet("""
            QWidget {
                background-color: #21252b; 
                color: #abb2bf;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 10px;
                color: #d7dae0;
            }
        """)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 15, 10, 10)
        layout.setSpacing(8)
        
        # Add a title
        title = QLabel("Menu")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Create buttons for each functionality
        self.execute_button = self._create_button("Execute", self.execute_clicked)
        self.ongoing_research_button = self._create_button("Ongoing Research", self.ongoing_research_clicked)
        
        # Add buttons to layout
        layout.addWidget(self.execute_button)
        layout.addWidget(self.ongoing_research_button)
        
        # Add stretch to push buttons to the top
        layout.addStretch(1)

    def _create_button(self, text, signal):
        """Helper method to create styled buttons"""
        button = QPushButton(text)
        button.setMinimumHeight(32)  # Smaller height
        button.setStyleSheet("""
            QPushButton {
                background-color: #2c313a;
                color: #abb2bf;
                border: 1px solid #181a1f;
                border-radius: 4px;
                padding: 4px 12px;
                font-size: 12px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #3a404b;
            }
            QPushButton:pressed {
                background-color: #4d78cc;
            }
        """)
        button.clicked.connect(lambda: signal.emit())
        return button