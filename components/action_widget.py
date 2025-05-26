from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QTextEdit, QDialog, QDialogButtonBox, QMessageBox
from PySide6.QtCore import Qt

class ActionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Set styling for the ActionWidget
        self.setStyleSheet("""
            QWidget {
                background-color: #18181b; /* zinc-900 */
                color: #d4d4d8; /* zinc-300 */
            }
            QLabel {
                color: #d4d4d8; /* zinc-300 */
            }
            QPushButton {
                background-color: #3f3f46; /* zinc-700 */
                color: #d4d4d8; /* zinc-300 */
                border: 1px solid #52525b; /* zinc-600 */
                border-radius: 4px;
                padding: 4px 12px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #52525b; /* zinc-600 */
            }
            QPushButton:pressed {
                background-color: #71717a; /* zinc-500 */
            }
             QTextEdit {
                background-color: #27272a; /* zinc-800 */
                color: #d4d4d8; /* zinc-300 */
                border: 1px solid #09090b; /* zinc-950 */
                border-radius: 2px;
                padding: 4px;
            }
        """)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_content = QWidget()
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_content)
        self.scroll_area.setWidget(self.scroll_area_content)

        self.layout.addWidget(QLabel("Suggested Actions:"))
        self.layout.addWidget(self.scroll_area)

        # Action buttons for the Execute loop
        self.discard_button = QPushButton("Discard")
        self.review_button = QPushButton("Edit")
        self.publish_button = QPushButton("Publish")

        self.layout.addWidget(self.discard_button)
        self.layout.addWidget(self.review_button)
        self.layout.addWidget(self.publish_button)

        # Initially hide buttons until we have content to act on
        self.discard_button.setVisible(False)
        self.review_button.setVisible(False)
        self.publish_button.setVisible(False)

    def display_output_card(self, action_card):
        """Display a compact card with the LLM output and action options."""
        # Clear previous content
        self.clear_suggestions()
        
        # Create card content
        card_label = QLabel(
            f"<h3>Generated Blog Article</h3>"
            f"<p><b>Preview:</b></p>"
            f"<p>{action_card['content']}</p>"
            f"<p><i>Choose an action below:</i></p>"
        )
        card_label.setWordWrap(True)
        card_label.setTextFormat(Qt.RichText)
        self.scroll_area_layout.addWidget(card_label)
        
        # Show action buttons
        self.discard_button.setVisible(True)
        self.review_button.setVisible(True)
        self.publish_button.setVisible(True)

    def open_text_editor(self, content):
        """Open a full-featured text editor dialog for editing the content."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Blog Article")
        dialog.setModal(True)
        dialog.resize(800, 600)
        
        layout = QVBoxLayout(dialog)
        
        # Text editor
        text_edit = QTextEdit()
        text_edit.setPlainText(content)
        layout.addWidget(text_edit)
        
        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        # Show dialog and return result
        if dialog.exec() == QDialog.Accepted:
            return text_edit.toPlainText()
        return None

    def display_error(self, message):
        """Display an error message."""
        self.clear_suggestions()
        error_label = QLabel(f"<p style='color: #f87171;'><b>Error:</b> {message}</p>")
        error_label.setWordWrap(True)
        error_label.setTextFormat(Qt.RichText)
        self.scroll_area_layout.addWidget(error_label)
        
        # Hide action buttons
        self.discard_button.setVisible(False)
        self.review_button.setVisible(False)
        self.publish_button.setVisible(False)

    def display_success(self, message):
        """Display a success message."""
        self.clear_suggestions()
        success_label = QLabel(f"<p style='color: #4ade80;'><b>Success:</b> {message}</p>")
        success_label.setWordWrap(True)
        success_label.setTextFormat(Qt.RichText)
        self.scroll_area_layout.addWidget(success_label)
        
        # Hide action buttons
        self.discard_button.setVisible(False)
        self.review_button.setVisible(False)
        self.publish_button.setVisible(False)

    def display_info(self, message):
        """Display an info message."""
        self.clear_suggestions()
        info_label = QLabel(f"<p style='color: #38bdf8;'><b>Info:</b> {message}</p>")
        info_label.setWordWrap(True)
        info_label.setTextFormat(Qt.RichText)
        self.scroll_area_layout.addWidget(info_label)
        
        # Hide action buttons
        self.discard_button.setVisible(False)
        self.review_button.setVisible(False)
        self.publish_button.setVisible(False)

    def clear_suggestions(self):
        """Clear all suggestions from the scroll area."""
        for i in reversed(range(self.scroll_area_layout.count())):
            widget = self.scroll_area_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

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