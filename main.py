import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QSplitter, QWidget, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout, QCheckBox
from PySide6.QtCore import Qt
from components.menu_widget import MenuWidget
from components.execute_workspace import ExecuteWorkspace
from components.research_workspace import ResearchWorkspace 
from components.action_widget import ActionWidget
from components.agent import Agent

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cogito")
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Add debug mode checkbox at the top


        self.splitter = QSplitter(self)
        self.main_layout.addWidget(self.splitter)

        # Create widgets
        self.menu_widget = MenuWidget()
        self.execute_workspace = ExecuteWorkspace()
        self.research_workspace = ResearchWorkspace()
        self.action_widget = ActionWidget() # Action widget instance

        # Add sidebar menu to splitter
        self.splitter.addWidget(self.menu_widget)
        
        # Create a stacked widget for the workspaces
        self.workspace_stack = QStackedWidget()
        self.workspace_stack.addWidget(self.execute_workspace)
        self.workspace_stack.addWidget(self.research_workspace)
        
        # Add stacked workspace and action widget to splitter
        self.splitter.addWidget(self.workspace_stack)
        self.splitter.addWidget(self.action_widget)

        # Set initial sizes (optional)
        self.splitter.setSizes([150, 700, 350])

        # Initialize Agent with ActionWidget instance
        self.agent = Agent(self.action_widget)
        
        # Set agent reference in workspaces
        self.execute_workspace.set_agent(self.agent)
        self.research_workspace.set_agent(self.agent)
        
        self.connect_signals()
        self.set_mode("execute")

    def connect_signals(self):
        # Connect menu buttons to set_mode
        self.menu_widget.execute_clicked.connect(lambda: self.set_mode("execute"))
        self.menu_widget.ongoing_research_clicked.connect(lambda: self.set_mode("ongoing_research"))

    def set_mode(self, mode):
        if mode == "execute":
            self.workspace_stack.setCurrentWidget(self.execute_workspace)
            self.action_widget.setVisible(True)
        elif mode == "ongoing_research":
            self.workspace_stack.setCurrentWidget(self.research_workspace)
            self.action_widget.setVisible(True)  # Make action widget visible for ongoing research

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())