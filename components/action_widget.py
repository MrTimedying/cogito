from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QPushButton
from PySide6.QtCore import Qt, Signal

class ActionWidget(QWidget):
    """
    Right panel widget that serves as a contextual action layer.
    It will provide action suggestions based on the app's internal logic.
    """
    action_triggered = Signal(str)
    
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
                color: #d7dae0;
            }
            QFrame {
                background-color: #282c34;
                border: 1px solid #181a1f;
                border-radius: 4px;
            }
        """)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 15, 10, 10)
        layout.setSpacing(8)
        
        # Add a title
        title = QLabel("Suggested Actions")
        title.setAlignment(Qt.AlignCenter)
        title.setContentsMargins(0, 0, 0, 10)
        layout.addWidget(title)
        
        # Create a frame for suggested actions
        self.actions_frame = QFrame()
        self.actions_frame.setFrameShape(QFrame.StyledPanel)
        
        # Create layout for the actions frame
        self.actions_layout = QVBoxLayout(self.actions_frame)
        self.actions_layout.setContentsMargins(8, 8, 8, 8)
        self.actions_layout.setSpacing(6)
        
        # Add some placeholder text
        placeholder = QLabel("Actions will appear here based on context")
        placeholder.setWordWrap(True)
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setStyleSheet("color: #5c6370; font-size: 12px; font-weight: normal;")
        self.actions_layout.addWidget(placeholder)
        
        # Add the frame to the main layout
        layout.addWidget(self.actions_frame)
        
        # Add stretch to push content to the top
        layout.addStretch(1)
    
    def add_suggestion(self, action_text, callback=None):
        """
        Adds a suggested action to the panel
        
        Args:
            action_text (str): Text describing the suggested action
            callback (callable, optional): Function to call when action is selected
        """
        button = QPushButton(action_text)
        button.setStyleSheet("""
            QPushButton {
                background-color: #2c313a;
                color: #abb2bf;
                border: 1px solid #181a1f;
                border-radius: 4px;
                padding: 6px 10px;
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
        
        if callback:
            button.clicked.connect(callback)
        else:
            button.clicked.connect(lambda: self.action_triggered.emit(action_text))
        
        self.actions_layout.addWidget(button)
    
    def clear_suggestions(self):
        """Clears all suggested actions"""
        # Remove all widgets from the actions layout except the placeholder
        for i in reversed(range(self.actions_layout.count())):
            item = self.actions_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater() 