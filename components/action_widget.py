from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
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
        
        # Add the frame to the main layout
        layout.addWidget(self.actions_frame)
        
        # Add stretch to push content to the top
        layout.addStretch(1)
    
    def clear_suggestions(self):
        """Clears all suggested actions"""
        pass 