from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, 
    QFileDialog, QTextEdit, QScrollArea, QFrame, QComboBox,
    QLineEdit, QGridLayout, QFormLayout, QSlider, QSpinBox, 
    QDoubleSpinBox, QMessageBox, QCheckBox, QTableWidget, QHeaderView,
    QTableWidgetItem
)
from PySide6.QtCore import Qt
import os
from datetime import datetime
from .base_workspace import BaseWorkspace
from .pdf_processor import PDFProcessor

class ExecuteWorkspace(BaseWorkspace):
    """
    Execute workspace widget that handles the execute workflow components.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pdf_processor = PDFProcessor()
        self.uploaded_pdf_paths = []
        self.compliance_content = None
        self.prompt_content = None
        self.selected_model = None
        self.api_key = None
        self.context_content = None
        self.proofread_content = None
        self.token_counter = None
        self._setup_execute_ui()
        
    def _setup_execute_ui(self):
        """Set up the execute workflow UI components"""
        # Create different views for execute workflow
        self.execute_options_widget = self._create_execute_options_widget()
        self.compliance_widget = self._create_compliance_widget()
        self.prompt_definition_widget = self._create_prompt_definition_widget()
        self.context_upload_widget = self._create_context_upload_widget()
        self.proofread_widget = self._create_proofread_widget()
        
        # Add widgets to stacked widget
        self.stacked_widget.addWidget(self.execute_options_widget)
        self.stacked_widget.addWidget(self.compliance_widget)
        self.stacked_widget.addWidget(self.prompt_definition_widget)
        self.stacked_widget.addWidget(self.context_upload_widget)
        self.stacked_widget.addWidget(self.proofread_widget)
        
        # Set default widget
        self.stacked_widget.setCurrentWidget(self.execute_options_widget)

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
        
        # Add log button
        log_btn = QPushButton("Log")
        log_btn.setToolTip("Log compliance document content to a file")
        log_btn.clicked.connect(self._log_compliance_document)
        header_layout.addWidget(log_btn)
        
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
        
        # Add log button
        log_btn = QPushButton("Log")
        log_btn.setToolTip("Log prompt definition content to a file")
        log_btn.clicked.connect(self._log_prompt_definition)
        header_layout.addWidget(log_btn)
        
        layout.addLayout(header_layout)
        
        # Rest of the widget implementation...
        empty = QWidget()
        empty.setMinimumWidth(back_btn.sizeHint().width())
        header_layout.addWidget(empty)
        
        # Form layout for prompt options
        form_layout = QFormLayout()
        
        # Model selection with updated models
        self.model_combo = QComboBox()
        self.model_combo.addItems([
            "Claude 3 Opus",
            "Claude 3.5 Haiku",
            "Claude 3.5 Sonnet",
            "Claude 3.7 Sonnet",
            "Claude 4 Opus",
            "Claude 4 Sonnet",
            "Cursor Small",
            "Deepseek R1",
            "Deepseek V3",
            "Gemini 2.0 Pro (exp)",
            "Gemini 2.5 Flash",
            "Gemini 2.5 Pro",
            "GPT 4.1",
            "GPT 4.5 Preview",
            "GPT-4o",
            "GPT-4o mini",
            "Grok 2",
            "Grok 3 Beta",
            "Grok 3 Mini Beta",
            "o1",
            "o1 Mini",
            "o3",
            "o3-mini",
            "o4-mini"
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
        """Create widget for context upload with PDF processing capabilities"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Add header with back button
        header_layout = QHBoxLayout()
        back_btn = QPushButton("\u2190 Back")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.execute_options_widget))
        header_layout.addWidget(back_btn)
        
        title = QLabel("Upload Context")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        
        # Add log button
        log_btn = QPushButton("Log")
        log_btn.setToolTip("Log uploaded context content to a file")
        log_btn.clicked.connect(self._log_context_upload)
        header_layout.addWidget(log_btn)
        
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
        
        # List of uploaded files with token counts (using QTableWidget)
        self.file_list_label = QLabel("Uploaded Files:")
        layout.addWidget(self.file_list_label)
        
        self.file_table = QTableWidget(0, 3) # Name, Tokens, Actions
        self.file_table.setHorizontalHeaderLabels(["File Name", "Tokens", "Actions"])
        self.file_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch) # Stretch file name column
        self.file_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.file_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.file_table.setEditTriggers(QTableWidget.NoEditTriggers) # Make table read-only
        self.file_table.setSelectionBehavior(QTableWidget.SelectRows) # Select entire row
        self.file_table.setSelectionMode(QTableWidget.SingleSelection) # Allow single selection
        self.file_table.setMaximumHeight(150)
        layout.addWidget(self.file_table)
        
        # Processing options section
        options_layout = QFormLayout()
        
        # Add options for PDF processing if needed
        self.process_immediately_checkbox = QCheckBox("Process PDFs immediately on upload")
        self.process_immediately_checkbox.setChecked(True)
        options_layout.addRow("", self.process_immediately_checkbox)
        
        # Add process button
        process_btn = QPushButton("Process Selected PDFs")
        process_btn.clicked.connect(self._process_pdfs)
        layout.addLayout(options_layout)
        layout.addWidget(process_btn)
        
        # Add stretch
        layout.addStretch()
        
        return widget

    def _create_proofread_widget(self):
        """Create widget for proof-read document"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Add header with back button
        header_layout = QHBoxLayout()
        back_btn = QPushButton("\u2190 Back")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.execute_options_widget))
        header_layout.addWidget(back_btn)
        
        title = QLabel("Proof-read Document")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        
        # Add log button
        log_btn = QPushButton("Log")
        log_btn.setToolTip("Log proof-read document content to a file")
        log_btn.clicked.connect(self._log_proofread_document)
        header_layout.addWidget(log_btn)
        
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
                    # Store content for future use
                    self.compliance_content = content
            except Exception as e:
                self.compliance_preview.setText(f"Error reading file: {str(e)}")
    
    def _select_context_files(self):
        """Open file dialog to select PDF context files and process them"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Select Context Files", "", "PDF Files (*.pdf)"
        )
        if file_paths:
            # Store selected file paths
            self.uploaded_pdf_paths = file_paths

            # Clear previous entries in the table
            self.file_table.setRowCount(0)

            # Add files to the table initially (before processing)
            for path in file_paths:
                row = self.file_table.rowCount()
                self.file_table.insertRow(row)
                self.file_table.setItem(row, 0, QTableWidgetItem(os.path.basename(path)))
                self.file_table.setItem(row, 1, QTableWidgetItem("Processing...")) # Placeholder

                # Add remove button
                remove_btn = QPushButton("Remove")
                remove_btn.clicked.connect(lambda checked, row=row: self._remove_context_file(row))
                button_widget = QWidget()
                button_layout = QHBoxLayout(button_widget)
                button_layout.addWidget(remove_btn)
                button_layout.setContentsMargins(0, 0, 0, 0)
                button_layout.setAlignment(Qt.AlignCenter)
                self.file_table.setCellWidget(row, 2, button_widget)

            # Process PDFs if the checkbox is checked
            if hasattr(self, 'process_immediately_checkbox') and self.process_immediately_checkbox.isChecked():
                self._process_pdfs()
            else:
                # Update the token counter with 0 initially if not processed
                self._update_total_token_count() # This will show 0/Limit initially

    def _process_pdfs(self):
        """Process the uploaded PDF files using PDFProcessor and update the table and token count"""
        if not self.uploaded_pdf_paths:
            QMessageBox.warning(self, "No Files", "No PDF files have been uploaded.")
            return

        # Clear previous processed data to avoid mixing
        self.pdf_processor.processed_pdfs = {}
        
        total_tokens = 0
        updated_file_paths = [] # To store paths of files that were successfully processed

        # Process each PDF and update the table
        for row, path in enumerate(self.uploaded_pdf_paths):
            try:
                # Process PDF and get token count
                processed_data = self.pdf_processor.process_pdf(path)

                token_count = processed_data['token_count']

                # Update table item with actual token count
                self.file_table.setItem(row, 1, QTableWidgetItem(str(token_count)))

                total_tokens += token_count
                updated_file_paths.append(path)

            except Exception as e:
                # Update table item with error message
                self.file_table.setItem(row, 1, QTableWidgetItem(f"Error: {str(e)[:20]}...")) # Truncate error message
                print(f"Error processing {os.path.basename(path)}: {str(e)}")

        # Update the internal list to only include successfully processed files
        self.uploaded_pdf_paths = updated_file_paths

        # Update the total token count displayed
        self._update_total_token_count()

        # Store processed content for future use (only include successfully processed files)
        token_limit = self._get_token_limit(self.model_combo.currentText())
        combined_text, _, _ = self.pdf_processor.get_combined_text(
            self.uploaded_pdf_paths,
            max_tokens=token_limit
        )
        self.context_content = combined_text

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
                    # Store content for future use
                    self.proofread_content = content
            except Exception as e:
                self.proofread_preview.setText(f"Error reading file: {str(e)}")
    
    def _handle_produce(self):
        """Handle the produce button click - trigger the Execute loop in Agent"""
        if self.agent:
            self.agent.handle_execute_produce(self)
        else:
            print("Agent not available for Execute loop.")

    def _update_token_limit(self, model_name):
        """Update token limit based on selected model and refresh token counter"""
        token_limit = self._get_token_limit(model_name)

        self.token_limit_label.setText(f"Token Context Window: {token_limit//1000}K")

        # Recalculate and update the token counter based on the new limit
        self._update_total_token_count()

    def _update_token_counter(self, token_count, model_name=None):
        """Update token counter with the current count and limit"""
        token_limit = self._get_token_limit(model_name)

        if self.token_counter:
            self.token_counter.setText(f"Tokens: {token_count}/{token_limit}")

            # Update color based on token count
            if token_count > token_limit:
                self.token_counter.setStyleSheet("color: #e06c75;")  # Red color
            else:
                self.token_counter.setStyleSheet("color: #98c379;")  # Green color
    
    def _get_token_limit(self, model_name=None):
        """Get token limit for the specified model"""
        # Map model display names to their token limits
        token_limits = {
            "Claude 3 Opus": 200000,
            "Claude 3.5 Haiku": 150000,
            "Claude 3.5 Sonnet": 180000,
            "Claude 3.7 Sonnet": 180000,
            "Claude 4 Opus": 200000,
            "Claude 4 Sonnet": 180000,
            "Cursor Small": 32000,
            "Deepseek R1": 64000,
            "Deepseek V3": 128000,
            "Gemini 2.0 Pro (exp)": 32000,
            "Gemini 2.5 Flash": 1000000,
            "Gemini 2.5 Pro": 1000000,
            "GPT 4.1": 128000,
            "GPT 4.5 Preview": 256000,
            "GPT-4o": 128000,
            "GPT-4o mini": 128000,
            "Grok 2": 128000,
            "Grok 3 Beta": 128000,
            "Grok 3 Mini Beta": 64000,
            "o1": 128000,
            "o1 Mini": 64000,
            "o3": 128000,
            "o3-mini": 64000,
            "o4-mini": 64000
        }

        if not model_name:
            # If model_name is not provided, try to get it from the combo box
            model_name = self.model_combo.currentText() if hasattr(self, 'model_combo') else None

        return token_limits.get(model_name, 8192)  # Default if model not found

    def _log_compliance_document(self):
        """Log compliance document content"""
        if hasattr(self, 'compliance_content') and self.compliance_content:
            if self.agent:
                filename = self.agent.log_compliance_document(self.compliance_content)
                if filename:
                    QMessageBox.information(self, "Log Created", f"Compliance document logged to {filename}")
            else:
                self._save_log_file("compliance_document", self.compliance_content)
        else:
            QMessageBox.warning(self, "Error", "No compliance document content to log")

    def _log_prompt_definition(self):
        """Log prompt definition content"""
        if hasattr(self, 'prompt_text') and self.prompt_text.toPlainText():
            content = self.prompt_text.toPlainText()
            model = self.model_combo.currentText()
            temperature = self.temp_value.value()
            max_tokens = self.max_tokens.value()
            
            log_content = f"Model: {model}\n"
            log_content += f"Temperature: {temperature}\n"
            log_content += f"Max Tokens: {max_tokens}\n\n"
            log_content += f"Prompt Content:\n{content}"
            
            if self.agent:
                filename = self.agent.log_prompt_definition(
                    content, model, temperature, max_tokens
                )
                if filename:
                    QMessageBox.information(self, "Log Created", f"Prompt definition logged to {filename}")
            else:
                self._save_log_file("prompt_definition", log_content)
        else:
            QMessageBox.warning(self, "Error", "No prompt content to log")

    def _log_context_upload(self):
        """Log processed PDF content"""
        if not self.uploaded_pdf_paths:
            QMessageBox.warning(self, "Error", "No PDF files have been uploaded")
            return
            
        log_content = self.pdf_processor.log_processed_content(self.uploaded_pdf_paths)
        
        if self.agent:
            filename = self.agent.log_context_upload(log_content)
            if filename:
                QMessageBox.information(self, "Log Created", f"Context content logged to {filename}")
        else:
            self._save_log_file("context_upload", log_content)

    def _log_proofread_document(self):
        """Log proofread document content"""
        if hasattr(self, 'proofread_content') and self.proofread_content:
            if self.agent:
                filename = self.agent.log_proofread_document(self.proofread_content)
                if filename:
                    QMessageBox.information(self, "Log Created", f"Proof-read document logged to {filename}")
            else:
                self._save_log_file("proofread_document", self.proofread_content)
        else:
            QMessageBox.warning(self, "Error", "No proof-read document content to log")
            
    def _save_log_file(self, prefix, content):
        """Save content to a log file if agent is not available"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"logs/{prefix}_{timestamp}.txt"
        
        # Ensure logs directory exists
        os.makedirs("logs", exist_ok=True)
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            QMessageBox.information(self, "Log Created", f"Content logged to {filename}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to create log: {str(e)}")

    def _remove_context_file(self, row_index):
        """Remove a file from the context list and update token count"""
        # Get file path from stored list
        if 0 <= row_index < len(self.uploaded_pdf_paths):
            removed_file_path = self.uploaded_pdf_paths.pop(row_index)

            # Remove row from table
            self.file_table.removeRow(row_index)

            # Update token count
            self._update_total_token_count()

            print(f"Removed file: {removed_file_path}")

    def _update_total_token_count(self):
        """Calculate and update the total token count from processed files"""
        total_tokens = 0
        for path in self.uploaded_pdf_paths:
            if path in self.pdf_processor.processed_pdfs:
                total_tokens += self.pdf_processor.processed_pdfs[path]['token_count']

        model_name = self.model_combo.currentText() if hasattr(self, 'model_combo') else None
        if self.token_counter:
            self._update_token_counter(total_tokens, model_name) 