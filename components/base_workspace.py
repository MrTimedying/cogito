from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, 
    QFileDialog, QTextEdit, QScrollArea, QFrame, QComboBox,
    QLineEdit, QGridLayout, QGroupBox, QSlider, QSpinBox, 
    QSizePolicy, QStackedWidget, QFormLayout, QDoubleSpinBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QDrag, QDragEnterEvent, QDropEvent

class BaseWorkspace(QWidget):
    """
    Base workspace class that contains shared functionality between execute and research workspaces.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.agent = None
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the base UI elements and styling"""
        # Set Cursor-like dark theme colors (using Tailwind Zinc palette)
        self.setStyleSheet("""
            QWidget {
                background-color: #18181b; /* zinc-900 */
                color: #d4d4d8; /* zinc-300 */
            }
            QLabel {
                color: #d4d4d8; /* zinc-300 */
                font-size: 12px;
            }
            QLabel#Title {
                font-size: 16px;
                font-weight: bold;
                color: #fafafa; /* zinc-50 */
                margin-bottom: 15px;
            }
            QPushButton {
                background-color: #27272a; /* zinc-800 */
                color: #d4d4d8; /* zinc-300 */
                border: 1px solid #09090b; /* zinc-950 */
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #3f3f46; /* zinc-700 */
            }
            QPushButton:pressed {
                background-color: #52525b; /* zinc-600 */
            }
            QTextEdit, QLineEdit, QComboBox, QTableWidget {
                background-color: #27272a; /* zinc-800 */
                color: #d4d4d8; /* zinc-300 */
                border: 1px solid #09090b; /* zinc-950 */
                border-radius: 2px;
                padding: 4px;
            }
            QScrollArea {
                border: none;
            }
            QFrame#DropArea {
                border: 2px dashed #71717a; /* zinc-500 */
                border-radius: 8px;
                background-color: #27272a; /* zinc-800 */
                padding: 20px;
            }
            QPushButton#Card {
                min-height: 120px;
                padding: 20px;
                text-align: center;
                font-size: 14px;
                font-weight: bold;
                background-color: #27272a; /* zinc-800 */
            }
            QPushButton#Card:hover {
                background-color: #3f3f46; /* zinc-700 */
            }
        """)
        
        # Create main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        
        # Create a stacked widget to manage different views
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

    def set_agent(self, agent):
        """Set the agent reference"""
        self.agent = agent
        
    def _create_placeholder_widget(self, title):
        """Create a placeholder widget for modes not yet implemented"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        label = QLabel(title)
        label.setProperty("class", "Title")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        
        placeholder = QLabel(f"{title} functionality will be implemented here")
        placeholder.setAlignment(Qt.AlignCenter)
        layout.addWidget(placeholder)
        
        return widget
    
    def _create_nav_button(self, text, callback):
        """Create a styled navigation button"""
        button = QPushButton(text)
        button.setMinimumHeight(40)
        button.clicked.connect(callback)
        return button
        
    def _create_card_button(self, text, callback):
        """Create a styled card button"""
        button = QPushButton(text)
        button.setObjectName("Card")
        button.clicked.connect(callback)
        return button 