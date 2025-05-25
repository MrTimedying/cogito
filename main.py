import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QSplitter, QWidget, QVBoxLayout, QLabel, QStackedWidget
from components.menu_widget import MenuWidget
from components.main_workspace import MainWorkspace
from components.action_widget import ActionWidget
from components.agent import Agent # Import the Agent class

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cogito")
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)

        self.splitter = QSplitter(self)
        self.main_layout.addWidget(self.splitter)

        # Create widgets
        self.menu_widget = MenuWidget()
        self.main_workspace = MainWorkspace()
        self.action_widget = ActionWidget() # Action widget instance

        # Add widgets to splitter
        self.splitter.addWidget(self.menu_widget)
        self.splitter.addWidget(self.main_workspace)
        self.splitter.addWidget(self.action_widget)

        # Set initial sizes (optional)
        self.splitter.setSizes([150, 700, 350])

        # Initialize Agent with ActionWidget instance
        self.agent = Agent(self.action_widget)

        self.connect_signals()
        self.set_mode("execute") # Set initial mode

    def connect_signals(self):
        self.menu_widget.execute_clicked.connect(self.agent.handle_execute)
        self.menu_widget.ongoing_research_clicked.connect(self.agent.handle_research)
        # Removed the archive_research_clicked connection

    def set_mode(self, mode):
        if mode == "execute":
            self.main_workspace.stacked_widget.setCurrentWidget(self.main_workspace.execute_options_widget)
            self.action_widget.setVisible(True)
        elif mode == "ongoing_research":
            self.main_workspace.stacked_widget.setCurrentWidget(self.main_workspace.ongoing_research_widget)
            self.action_widget.setVisible(False) # Hide action widget for ongoing research?
        # Removed the archive_research mode

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())