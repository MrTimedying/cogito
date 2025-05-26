from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QCheckBox
from PySide6.QtCore import Signal, Qt

class MenuWidget(QWidget):
    """
    Left panel widget that contains menu options for the different functionality modes.
    """
    execute_clicked = Signal()
    ongoing_research_clicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set Cursor-like dark theme colors (using Tailwind Zinc palette)
        self.setStyleSheet("""
            QWidget {
                background-color: #27272a; /* zinc-800 */
                color: #d4d4d8; /* zinc-300 */
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 10px;
                color: #fafafa; /* zinc-50 */
            }
            QCheckBox {
                color: #d4d4d8; /* zinc-300 */
            }
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
            }
            QCheckBox::indicator:unchecked {
                image: url(checkbox_unchecked.png);
            }
            QCheckBox::indicator:checked {
                image: url(checkbox_checked.png);
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
        
        # Add debug mode checkbox (fixed size)
        self.debug_checkbox = QCheckBox("Debug Mode")
        self.debug_checkbox.setFixedHeight(22)
        self.debug_checkbox.setFixedWidth(120)
        layout.addWidget(self.debug_checkbox)
        
        # Add stretch to push buttons to the top
        layout.addStretch(1)

    def _create_button(self, text, signal):
        """Helper method to create styled buttons"""
        button = QPushButton(text)
        button.setMinimumHeight(32)  # Smaller height
        button.setStyleSheet("""
            QPushButton {
                background-color: #3f3f46; /* zinc-700 */
                color: #d4d4d8; /* zinc-300 */
                border: 1px solid #52525b; /* zinc-600 */
                border-radius: 4px;
                padding: 4px 12px;
                font-size: 12px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #52525b; /* zinc-600 */
            }
            QPushButton:pressed {
                background-color: #71717a; /* zinc-500 */
            }
        """)
        button.clicked.connect(lambda: signal.emit())
        return button