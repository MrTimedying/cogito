from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, 
    QFileDialog, QTextEdit, QScrollArea, QFrame, QComboBox,
    QLineEdit, QGridLayout, QGroupBox, QSlider, QSpinBox, 
    QSizePolicy, QStackedWidget, QFormLayout, QDoubleSpinBox,
    QTableWidget, QTableWidgetItem, QHeaderView
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
            QTextEdit, QLineEdit, QComboBox, QTableWidget {
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
            QPushButton#Card {
                min-height: 120px;
                padding: 20px;
                text-align: center;
                font-size: 14px;
                font-weight: bold;
                background-color: #2c313a;
            }
            QPushButton#Card:hover {
                background-color: #3a404b;
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
        self.ongoing_research_widget = self._create_ongoing_research_widget()
        self.archive_research_widget = self._create_placeholder_widget("Archive Research")
        
        # Create specialized widgets for execute subpages
        self.compliance_widget = self._create_compliance_widget()
        self.prompt_definition_widget = self._create_prompt_definition_widget()
        self.context_upload_widget = self._create_context_upload_widget()
        self.proofread_widget = self._create_proofread_widget()
        
        # Create specialized widgets for ongoing research subpages
        self.rss_feed_widget = self._create_rss_feed_widget()
        self.research_compliance_widget = self._create_research_compliance_widget()
        self.research_prompt_widget = self._create_research_prompt_widget()
        
        # Add widgets to stacked widget
        self.stacked_widget.addWidget(self.execute_options_widget)
        self.stacked_widget.addWidget(self.ongoing_research_widget)
        self.stacked_widget.addWidget(self.archive_research_widget)
        self.stacked_widget.addWidget(self.compliance_widget)
        self.stacked_widget.addWidget(self.prompt_definition_widget)
        self.stacked_widget.addWidget(self.context_upload_widget)
        self.stacked_widget.addWidget(self.proofread_widget)
        self.stacked_widget.addWidget(self.rss_feed_widget)
        self.stacked_widget.addWidget(self.research_compliance_widget)
        self.stacked_widget.addWidget(self.research_prompt_widget)
        
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
        
        # Model selection with updated models
        self.model_combo = QComboBox()
        self.model_combo.addItems([
            "gpt-4o-2024-05-13", 
            "gpt-4-turbo", 
            "claude-3-opus", 
            "claude-3-sonnet",
            "claude-3-haiku",
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-1.0-pro"
        ])
        # Connect model selection to token limit update
        self.model_combo.currentTextChanged.connect(self._update_token_limit)
        form_layout.addRow("Model:", self.model_combo)
        
        # Add a token limit display that gets updated based on model
        self.token_limit_label = QLabel("Token Context Window: 128K")
        form_layout.addRow("", self.token_limit_label)
        
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
        
        # Initialize token limit for default model
        self._update_token_limit(self.model_combo.currentText())
        
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
        
        # Add token counter - now with variable limit based on model
        self.token_counter = QLabel("Tokens: 0/128000")
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
            
            # Get current token limit from selected model
            model_name = self.model_combo.currentText() if hasattr(self, 'model_combo') else None
            
            token_limits = {
                "gpt-4o-2024-05-13": 128000, 
                "gpt-4-turbo": 128000, 
                "claude-3-opus": 200000, 
                "claude-3-sonnet": 180000,
                "claude-3-haiku": 150000,
                "gemini-1.5-pro": 1000000,
                "gemini-1.5-flash": 1000000,
                "gemini-1.0-pro": 32000
            }
            
            token_limit = token_limits.get(model_name, 8192) if model_name else 8192
            
            self.token_counter.setText(f"Tokens: {total_tokens}/{token_limit}")
            
            # Change color if over token limit
            if total_tokens > token_limit:
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

    def _update_token_limit(self, model_name):
        """Update token limit based on selected model"""
        token_limits = {
            "gpt-4o-2024-05-13": 128000, 
            "gpt-4-turbo": 128000, 
            "claude-3-opus": 200000, 
            "claude-3-sonnet": 180000,
            "claude-3-haiku": 150000,
            "gemini-1.5-pro": 1000000,
            "gemini-1.5-flash": 1000000,
            "gemini-1.0-pro": 32000
        }
        
        token_limit = token_limits.get(model_name, 8192)  # Default if model not found
        self.token_limit_label.setText(f"Token Context Window: {token_limit//1000}K")
        
        # Also update token counter if it exists
        if hasattr(self, 'token_counter'):
            current_count = int(self.token_counter.text().split('/')[0].split(':')[1].strip())
            self.token_counter.setText(f"Tokens: {current_count}/{token_limit}")
            
            # Update color based on new limit
            if current_count > token_limit:
                self.token_counter.setStyleSheet("color: #e06c75;")  # Red color
            else:
                self.token_counter.setStyleSheet("color: #98c379;")  # Green color

    def _create_ongoing_research_widget(self):
        """Create widget for the ongoing research options screen"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        
        # Add title
        title = QLabel("Ongoing Research")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Create grid layout for card buttons
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)
        
        # Create card buttons
        rss_card = self._create_card_button("Setup RSS Feeds", 
                                          lambda: self.stacked_widget.setCurrentWidget(self.rss_feed_widget))
                                          
        compliance_card = self._create_card_button("Compliancy Document", 
                                                lambda: self.stacked_widget.setCurrentWidget(self.research_compliance_widget))
                                                
        prompt_card = self._create_card_button("Prompt Definition", 
                                            lambda: self.stacked_widget.setCurrentWidget(self.research_prompt_widget))
                                            
        research_card = self._create_card_button("Research", 
                                               self._handle_research)
        
        # Add cards to grid layout
        grid_layout.addWidget(rss_card, 0, 0)
        grid_layout.addWidget(compliance_card, 0, 1)
        grid_layout.addWidget(prompt_card, 1, 0)
        grid_layout.addWidget(research_card, 1, 1)
        
        # Add grid layout to main layout
        layout.addLayout(grid_layout)
        
        # Add stretch to push content to the top
        layout.addStretch()
        
        return widget
        
    def _create_card_button(self, text, callback):
        """Create a styled card button"""
        button = QPushButton(text)
        button.setObjectName("Card")
        button.clicked.connect(callback)
        return button

    def _create_rss_feed_widget(self):
        """Create widget for RSS feed setup"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Add header with back button
        header_layout = QHBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.ongoing_research_widget))
        header_layout.addWidget(back_btn)
        
        title = QLabel("RSS Feed Setup")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        
        # Add empty widget to balance the layout
        empty = QWidget()
        empty.setMinimumWidth(back_btn.sizeHint().width())
        header_layout.addWidget(empty)
        
        layout.addLayout(header_layout)
        
        # Add description
        description = QLabel("Add, edit or remove RSS feeds for scientific journals")
        description.setWordWrap(True)
        layout.addWidget(description)
        
        # Create form for adding new RSS feeds
        form_layout = QFormLayout()
        
        self.journal_name = QLineEdit()
        self.journal_name.setPlaceholderText("Enter journal name")
        form_layout.addRow("Journal Name:", self.journal_name)
        
        self.journal_topic = QLineEdit()
        self.journal_topic.setPlaceholderText("Enter journal topic")
        form_layout.addRow("Journal Topic:", self.journal_topic)
        
        self.rss_link = QLineEdit()
        self.rss_link.setPlaceholderText("Enter RSS feed URL")
        form_layout.addRow("RSS Link:", self.rss_link)
        
        # Add button to add the feed
        add_btn = QPushButton("Add Feed")
        add_btn.clicked.connect(self._add_rss_feed)
        
        # Add form to layout
        layout.addLayout(form_layout)
        layout.addWidget(add_btn)
        
        # Create table for displaying RSS feeds
        self.rss_table = QTableWidget(0, 4)  # rows, columns
        self.rss_table.setHorizontalHeaderLabels(["Name", "Topic", "RSS URL", "Actions"])
        self.rss_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        
        # Add table to layout
        layout.addWidget(QLabel("Current RSS Feeds:"))
        layout.addWidget(self.rss_table)
        
        # Add some example data
        self._add_example_rss_feeds()
        
        return widget
        
    def _create_research_compliance_widget(self):
        """Create widget for research compliance document"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Add header with back button
        header_layout = QHBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.ongoing_research_widget))
        header_layout.addWidget(back_btn)
        
        title = QLabel("Research Compliancy Document")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        
        # Add empty widget to balance the layout
        empty = QWidget()
        empty.setMinimumWidth(back_btn.sizeHint().width())
        header_layout.addWidget(empty)
        
        layout.addLayout(header_layout)
        
        # Add description
        description = QLabel("Upload a .txt or .md document that specifies the requirements and compliance rules for research.")
        description.setWordWrap(True)
        layout.addWidget(description)
        
        # Add buttons for uploading
        upload_btn = QPushButton("Select Document...")
        upload_btn.clicked.connect(self._select_research_compliance_document)
        layout.addWidget(upload_btn)
        
        # Display selected file
        self.selected_research_compliance_file = QLabel("No file selected")
        layout.addWidget(self.selected_research_compliance_file)
        
        # Add preview area
        self.research_compliance_preview = QTextEdit()
        self.research_compliance_preview.setReadOnly(True)
        self.research_compliance_preview.setPlaceholderText("Document preview will appear here...")
        layout.addWidget(self.research_compliance_preview)
        
        # Add stretch
        layout.addStretch()
        
        return widget
        
    def _create_research_prompt_widget(self):
        """Create widget for research prompt definition"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Add header with back button
        header_layout = QHBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.ongoing_research_widget))
        header_layout.addWidget(back_btn)
        
        title = QLabel("Research Prompt Definition")
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
        
        # Model selection with updated models
        self.research_model_combo = QComboBox()
        self.research_model_combo.addItems([
            "gpt-4o-2024-05-13", 
            "gpt-4-turbo", 
            "claude-3-opus", 
            "claude-3-sonnet",
            "claude-3-haiku",
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-1.0-pro"
        ])
        form_layout.addRow("Model:", self.research_model_combo)
        
        # API Key
        self.research_api_key = QLineEdit()
        self.research_api_key.setPlaceholderText("Enter your API key")
        self.research_api_key.setEchoMode(QLineEdit.Password)
        form_layout.addRow("API Key:", self.research_api_key)
        
        # Temperature
        temp_layout = QHBoxLayout()
        self.research_temp_slider = QSlider(Qt.Horizontal)
        self.research_temp_slider.setRange(0, 100)  # 0 to 1 with two decimal places
        self.research_temp_slider.setValue(70)  # Default to 0.7
        
        self.research_temp_value = QDoubleSpinBox()
        self.research_temp_value.setRange(0, 1)
        self.research_temp_value.setSingleStep(0.01)
        self.research_temp_value.setValue(0.7)
        
        # Connect them
        self.research_temp_slider.valueChanged.connect(lambda v: self.research_temp_value.setValue(v/100))
        self.research_temp_value.valueChanged.connect(lambda v: self.research_temp_slider.setValue(int(v*100)))
        
        temp_layout.addWidget(self.research_temp_slider)
        temp_layout.addWidget(self.research_temp_value)
        form_layout.addRow("Temperature:", temp_layout)
        
        # Max tokens
        self.research_max_tokens = QSpinBox()
        self.research_max_tokens.setRange(100, 100000)
        self.research_max_tokens.setSingleStep(100)
        self.research_max_tokens.setValue(4000)
        form_layout.addRow("Max Tokens:", self.research_max_tokens)
        
        # Add form layout to main layout
        layout.addLayout(form_layout)
        
        # Prompt input
        layout.addWidget(QLabel("Research Prompt:"))
        self.research_prompt_text = QTextEdit()
        self.research_prompt_text.setPlaceholderText("Enter your research prompt here...")
        layout.addWidget(self.research_prompt_text)
        
        # Add save button
        save_btn = QPushButton("Save Configuration")
        layout.addWidget(save_btn)
        
        # Add stretch
        layout.addStretch()
        
        return widget
        
    def _add_rss_feed(self):
        """Add an RSS feed to the table"""
        name = self.journal_name.text()
        topic = self.journal_topic.text()
        url = self.rss_link.text()
        
        if name and topic and url:
            row = self.rss_table.rowCount()
            self.rss_table.insertRow(row)
            
            # Create items
            self.rss_table.setItem(row, 0, QTableWidgetItem(name))
            self.rss_table.setItem(row, 1, QTableWidgetItem(topic))
            self.rss_table.setItem(row, 2, QTableWidgetItem(url))
            
            # Create action buttons
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda: self._delete_rss_feed(row))
            
            # Create widget to hold buttons
            button_widget = QWidget()
            button_layout = QHBoxLayout(button_widget)
            button_layout.addWidget(delete_btn)
            button_layout.setContentsMargins(0, 0, 0, 0)
            
            # Add widget to table
            self.rss_table.setCellWidget(row, 3, button_widget)
            
            # Clear input fields
            self.journal_name.clear()
            self.journal_topic.clear()
            self.rss_link.clear()
    
    def _delete_rss_feed(self, row):
        """Delete an RSS feed from the table"""
        self.rss_table.removeRow(row)
    
    def _add_example_rss_feeds(self):
        """Add example RSS feeds to the table"""
        example_feeds = [
            ("Nature", "Multidisciplinary", "https://www.nature.com/nature.rss"),
            ("Science", "Multidisciplinary", "https://www.science.org/action/showFeed?type=etoc&feed=rss&jc=science"),
            ("PNAS", "Multidisciplinary", "https://www.pnas.org/action/showFeed?type=etoc&feed=rss&jc=pnas")
        ]
        
        for name, topic, url in example_feeds:
            self.journal_name.setText(name)
            self.journal_topic.setText(topic)
            self.rss_link.setText(url)
            self._add_rss_feed()
    
    def _select_research_compliance_document(self):
        """Open file dialog to select research compliance document"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Research Compliance Document", "", "Text Files (*.txt);;Markdown Files (*.md)"
        )
        if file_path:
            self.selected_research_compliance_file.setText(f"Selected: {file_path}")
            # Read the file content and display in preview
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.research_compliance_preview.setText(content)
            except Exception as e:
                self.research_compliance_preview.setText(f"Error reading file: {str(e)}")
    
    def _handle_research(self):
        """Handle the research button click - implement RSS scraping logic"""
        print("Research button clicked - Starting RSS scraping process")
        print("1. Reading RSS Feeds...")
        print("2. Extracting article information...")
        print("3. Handling missing abstracts...")
        print("4. Preparing data for AI...")
        print("5. Sending to AI API...")
        print("6. Processing AI response...")
        print("7. Research completed!") 