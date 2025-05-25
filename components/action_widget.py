from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea
from PySide6.QtCore import Qt

class ActionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_content = QWidget()
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_content)
        self.scroll_area.setWidget(self.scroll_area_content)

        self.layout.addWidget(QLabel("Suggested Actions:"))
        self.layout.addWidget(self.scroll_area)

        # Placeholder buttons for actions
        self.discard_button = QPushButton("Discard")
        self.review_button = QPushButton("Review")
        self.publish_button = QPushButton("Publish")

        self.layout.addWidget(self.discard_button)
        self.layout.addWidget(self.review_button)
        self.layout.addWidget(self.publish_button)

        self.discard_button.clicked.connect(self.handle_discard)
        self.review_button.clicked.connect(self.handle_review)
        self.publish_button.clicked.connect(self.handle_publish)

    def display_suggestions(self, suggested_actions):
        # Clear previous suggestions
        for i in reversed(range(self.scroll_area_layout.count())):
            widget = self.scroll_area_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Display new suggestions
        if suggested_actions:
            for suggestion in suggested_actions:
                suggestion_label = QLabel(
                    f"<b>Title:</b> {suggestion.get('title', 'N/A')}<br>"
                    f"<b>Action:</b> {suggestion.get('action', 'N/A')}<br>"
                    f"<b>Justification:</b> {suggestion.get('justification', 'N/A')}"
                )
                suggestion_label.setWordWrap(True)
                suggestion_label.setTextFormat(Qt.RichText)
                self.scroll_area_layout.addWidget(suggestion_label)
        else:
            no_suggestions_label = QLabel("No suggestions available.")
            self.scroll_area_layout.addWidget(no_suggestions_label)

    def handle_discard(self):
        print("Discard button clicked.")
        # TODO: Implement discard logic

    def handle_review(self):
        print("Review button clicked.")
        # TODO: Implement review logic (open text editor)

    def handle_publish(self):
        print("Publish button clicked.")
        # TODO: Implement publish logic (API call to Sanity)