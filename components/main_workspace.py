from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, 
    QFileDialog, QTextEdit, QScrollArea, QFrame, QComboBox,
    QLineEdit, QGridLayout, QGroupBox, QSlider, QSpinBox, 
    QSizePolicy, QStackedWidget, QFormLayout, QDoubleSpinBox
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QDrag, QDragEnterEvent, QDropEvent

class MainWorkspace(QWidget):
    """
    Central panel widget that serves as the main workspace of the application.
    This will be the primary area where content is displayed.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set Cursor-like dark theme colors
        self.setStyleSheet("""
            QWidget {
                background-color: #282c34;
                color: #abb2bf;
            }
            QLabel {
                color: #abb2bf;
                font-size: 12px;
            }
            QLabel#Title {
                font-size: 16px;
                font-weight: bold;
                color: #d7dae0;
                margin-bottom: 15px;
            }
            QPushButton {
                background-color: #2c313a;
                color: #abb2bf;
                border: 1px solid #181a1f;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #3a404b;
            }
            QPushButton:pressed {
                background-color: #4d78cc;
            }
            QTextEdit, QLineEdit, QComboBox {
                background-color: #2c313a;
                color: #abb2bf;
                border: 1px solid #181a1f;
                border-radius: 2px;
                padding: 4px;
            }
            QScrollArea {
                border: none;
            }
            QFrame#DropArea {
                border: 2px dashed #4d78cc;
                border-radius: 8px;
                background-color: #2c313a;
                padding: 20px;
            }
        """)
        
        # Create main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Create a stacked widget to manage different views
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)
        
        # Create different views for each mode
        self.execute_options_widget = self._create_execute_options_widget()
        self.ongoing_research_widget = self._create_placeholder_widget("Ongoing Research")
        self.archive_research_widget = self._create_placeholder_widget("Archive Research")
        
        # Create specialized widgets for execute subpages
        self.compliance_widget = self._create_compliance_widget()
        self.prompt_definition_widget = self._create_prompt_definition_widget()
        self.context_upload_widget = self._create_context_upload_widget()
        self.proofread_widget = self._create_proofread_widget()
        
        # Add widgets to stacked widget
        self.stacked_widget.addWidget(self.execute_options_widget)
        self.stacked_widget.addWidget(self.ongoing_research_widget)
        self.stacked_widget.addWidget(self.archive_research_widget)
        self.stacked_widget.addWidget(self.compliance_widget)
        self.stacked_widget.addWidget(self.prompt_definition_widget)
        self.stacked_widget.addWidget(self.context_upload_widget)
        self.stacked_widget.addWidget(self.proofread_widget)
        
        # Track current mode
        self.current_mode = "execute"

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
        
    def _create_execute_options_widget(self):
        """Create widget for the main execute options screen"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Add title
        title = QLabel("Execute")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Create buttons for each option
        compliance_btn = self._create_nav_button("Compliancy Document", lambda: self.stacked_widget.setCurrentWidget(self.compliance_widget))
        prompt_btn = self._create_nav_button("Prompt Definition", lambda: self.stacked_widget.setCurrentWidget(self.prompt_definition_widget))
        context_btn = self._create_nav_button("Upload Context", lambda: self.stacked_widget.setCurrentWidget(self.context_upload_widget))
        proofread_btn = self._create_nav_button("Proof-read Document", lambda: self.stacked_widget.setCurrentWidget(self.proofread_widget))
        produce_btn = self._create_nav_button("Produce", self._handle_produce)
        
        # Add buttons to layout
        layout.addWidget(compliance_btn)
        layout.addWidget(prompt_btn)
        layout.addWidget(context_btn)
        layout.addWidget(proofread_btn)
        layout.addWidget(produce_btn)
        
        # Add stretch to push buttons toward the top
        layout.addStretch()
        
        return widget
    
    def _create_compliance_widget(self):
        """Create widget for the compliance document upload"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Add header with back button
        header_layout = QHBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.execute_options_widget))
        header_layout.addWidget(back_btn)
        
        title = QLabel("Compliancy Document")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        
        # Add empty widget to balance the layout
        empty = QWidget()
        empty.setMinimumWidth(back_btn.sizeHint().width())
        header_layout.addWidget(empty)
        
        layout.addLayout(header_layout)
        
        # Add description
        description = QLabel("Upload a .txt or .md document that specifies the requirements and compliance rules.")
        description.setWordWrap(True)
        layout.addWidget(description)
        
        # Add buttons for uploading
        upload_btn = QPushButton("Select Document...")
        upload_btn.clicked.connect(self._select_compliance_document)
        layout.addWidget(upload_btn)
        
        # Display selected file
        self.selected_compliance_file = QLabel("No file selected")
        layout.addWidget(self.selected_compliance_file)
        
        # Add preview area
        self.compliance_preview = QTextEdit()
        self.compliance_preview.setReadOnly(True)
        self.compliance_preview.setPlaceholderText("Document preview will appear here...")
        layout.addWidget(self.compliance_preview)
        
        # Add stretch
        layout.addStretch()
        
        return widget

    def _create_prompt_definition_widget(self):
        """Create widget for prompt definition"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Add header with back button
        header_layout = QHBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.execute_options_widget))
        header_layout.addWidget(back_btn)
        
        title = QLabel("Prompt Definition")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        
        # Add empty widget to balance the layout
        empty = QWidget()
        empty.setMinimumWidth(back_btn.sizeHint().width())
        header_layout.addWidget(empty)
        
        layout.addLayout(header_layout)
        
        # Form layout for prompt options
        form_layout = QFormLayout()
        
        # Model selection
        self.model_combo = QComboBox()
        self.model_combo.addItems(["gpt-4-0125-preview", "gpt-4-turbo", "claude-3-opus", "claude-3-sonnet"])
        form_layout.addRow("Model:", self.model_combo)
        
        # API Key
        self.api_key = QLineEdit()
        self.api_key.setPlaceholderText("Enter your API key")
        self.api_key.setEchoMode(QLineEdit.Password)
        form_layout.addRow("API Key:", self.api_key)
        
        # Temperature
        temp_layout = QHBoxLayout()
        self.temp_slider = QSlider(Qt.Horizontal)
        self.temp_slider.setRange(0, 100)  # 0 to 1 with two decimal places
        self.temp_slider.setValue(70)  # Default to 0.7
        
        self.temp_value = QDoubleSpinBox()
        self.temp_value.setRange(0, 1)
        self.temp_value.setSingleStep(0.01)
        self.temp_value.setValue(0.7)
        
        # Connect them
        self.temp_slider.valueChanged.connect(lambda v: self.temp_value.setValue(v/100))
        self.temp_value.valueChanged.connect(lambda v: self.temp_slider.setValue(int(v*100)))
        
        temp_layout.addWidget(self.temp_slider)
        temp_layout.addWidget(self.temp_value)
        form_layout.addRow("Temperature:", temp_layout)
        
        # Max tokens
        self.max_tokens = QSpinBox()
        self.max_tokens.setRange(100, 100000)
        self.max_tokens.setSingleStep(100)
        self.max_tokens.setValue(4000)
        form_layout.addRow("Max Tokens:", self.max_tokens)
        
        # Add form layout to main layout
        layout.addLayout(form_layout)
        
        # Prompt input
        layout.addWidget(QLabel("Prompt:"))
        self.prompt_text = QTextEdit()
        self.prompt_text.setPlaceholderText("Enter your prompt here...")
        layout.addWidget(self.prompt_text)
        
        # Add save button
        save_btn = QPushButton("Save Configuration")
        layout.addWidget(save_btn)
        
        # Add stretch
        layout.addStretch()
        
        return widget
        
    def _create_context_upload_widget(self):
        """Create widget for context upload"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Add header with back button
        header_layout = QHBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.execute_options_widget))
        header_layout.addWidget(back_btn)
        
        title = QLabel("Upload Context")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        
        # Add token counter
        self.token_counter = QLabel("Tokens: 0/8192")
        self.token_counter.setAlignment(Qt.AlignRight)
        header_layout.addWidget(self.token_counter)
        
        layout.addLayout(header_layout)
        
        # Create drag & drop area
        drop_area = QFrame()
        drop_area.setObjectName("DropArea")
        drop_area.setMinimumHeight(200)
        drop_area_layout = QVBoxLayout(drop_area)
        
        drop_label = QLabel("Drop PDF files here or click to select")
        drop_label.setAlignment(Qt.AlignCenter)
        drop_area_layout.addWidget(drop_label)
        
        select_btn = QPushButton("Select Files...")
        select_btn.clicked.connect(self._select_context_files)
        drop_area_layout.addWidget(select_btn, alignment=Qt.AlignCenter)
        
        layout.addWidget(drop_area)
        
        # List of uploaded files with token counts
        self.file_list_label = QLabel("Uploaded Files:")
        layout.addWidget(self.file_list_label)
        
        self.file_list = QTextEdit()
        self.file_list.setReadOnly(True)
        self.file_list.setMaximumHeight(150)
        layout.addWidget(self.file_list)
        
        # Add stretch
        layout.addStretch()
        
        return widget
        
    def _create_proofread_widget(self):
        """Create widget for proof-read document"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Add header with back button
        header_layout = QHBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.execute_options_widget))
        header_layout.addWidget(back_btn)
        
        title = QLabel("Proof-read Document")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        
        # Add empty widget to balance the layout
        empty = QWidget()
        empty.setMinimumWidth(back_btn.sizeHint().width())
        header_layout.addWidget(empty)
        
        layout.addLayout(header_layout)
        
        # Add description
        description = QLabel("Upload a document to be used for proof-reading the output.")
        description.setWordWrap(True)
        layout.addWidget(description)
        
        # Add buttons for uploading
        upload_btn = QPushButton("Select Document...")
        upload_btn.clicked.connect(self._select_proofread_document)
        layout.addWidget(upload_btn)
        
        # Display selected file
        self.selected_proofread_file = QLabel("No file selected")
        layout.addWidget(self.selected_proofread_file)
        
        # Add preview area
        self.proofread_preview = QTextEdit()
        self.proofread_preview.setReadOnly(True)
        self.proofread_preview.setPlaceholderText("Document preview will appear here...")
        layout.addWidget(self.proofread_preview)
        
        # Add stretch
        layout.addStretch()
        
        return widget
    
    def _create_nav_button(self, text, callback):
        """Create a styled navigation button"""
        button = QPushButton(text)
        button.setMinimumHeight(40)
        button.clicked.connect(callback)
        return button
    
    def _select_compliance_document(self):
        """Open file dialog to select compliance document"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Compliance Document", "", "Text Files (*.txt);;Markdown Files (*.md)"
        )
        if file_path:
            self.selected_compliance_file.setText(f"Selected: {file_path}")
            # Read the file content and display in preview
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.compliance_preview.setText(content)
            except Exception as e:
                self.compliance_preview.setText(f"Error reading file: {str(e)}")
    
    def _select_context_files(self):
        """Open file dialog to select context files"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Select Context Files", "", "PDF Files (*.pdf)"
        )
        if file_paths:
            # Simple mock of token counting - in a real app this would need proper PDF parsing
            total_tokens = 0
            file_info = ""
            
            for path in file_paths:
                # Mock token count - would use a PDF parser in a real app
                estimated_tokens = 1000  # Example token count
                total_tokens += estimated_tokens
                file_info += f"{path} - Estimated tokens: {estimated_tokens}\n"
            
            self.file_list.setText(file_info)
            self.token_counter.setText(f"Tokens: {total_tokens}/8192")
            
            # Change color if over token limit
            if total_tokens > 8192:
                self.token_counter.setStyleSheet("color: #e06c75;")  # Red color
            else:
                self.token_counter.setStyleSheet("color: #98c379;")  # Green color
    
    def _select_proofread_document(self):
        """Open file dialog to select proof-read document"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Proof-read Document", "", "Text Files (*.txt);;Markdown Files (*.md)"
        )
        if file_path:
            self.selected_proofread_file.setText(f"Selected: {file_path}")
            # Read the file content and display in preview
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.proofread_preview.setText(content)
            except Exception as e:
                self.proofread_preview.setText(f"Error reading file: {str(e)}")
    
    def _handle_produce(self):
        """Handle the produce button click"""
        print("Produce button clicked - This feature is not yet implemented")
    
    def set_mode(self, mode):
        """
        Changes the workspace content based on the selected mode
        
        Args:
            mode (str): One of 'execute', 'ongoing_research', 'archive_research'
        """
        self.current_mode = mode
        
        if mode == "execute":
            self.stacked_widget.setCurrentWidget(self.execute_options_widget)
        elif mode == "ongoing_research":
            self.stacked_widget.setCurrentWidget(self.ongoing_research_widget)
        elif mode == "archive_research":
            self.stacked_widget.setCurrentWidget(self.archive_research_widget) 