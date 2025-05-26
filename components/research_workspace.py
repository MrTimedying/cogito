from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, 
    QFileDialog, QTextEdit, QScrollArea, QFrame, QComboBox,
    QLineEdit, QGridLayout, QFormLayout, QSlider, QSpinBox, 
    QDoubleSpinBox, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QCheckBox
)
from PySide6.QtCore import Qt
import os
from datetime import datetime
from .base_workspace import BaseWorkspace

class ResearchWorkspace(BaseWorkspace):
    """
    Research workspace widget that handles the ongoing research workflow components.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_research_ui()
        
    def _setup_research_ui(self):
        """Set up the research workflow UI components"""
        # Create different views for research workflow
        self.ongoing_research_widget = self._create_ongoing_research_widget()
        self.rss_feed_widget = self._create_rss_feed_widget()
        self.research_compliance_widget = self._create_research_compliance_widget()
        self.research_prompt_widget = self._create_research_prompt_widget()
        
        # Add widgets to stacked widget
        self.stacked_widget.addWidget(self.ongoing_research_widget)
        self.stacked_widget.addWidget(self.rss_feed_widget)
        self.stacked_widget.addWidget(self.research_compliance_widget)
        self.stacked_widget.addWidget(self.research_prompt_widget)
        
        # Set default widget
        self.stacked_widget.setCurrentWidget(self.ongoing_research_widget)
        
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
        
        # Add log button (new)
        log_btn = QPushButton("Log")
        log_btn.setToolTip("Log RSS feed setup to a file")
        log_btn.clicked.connect(self._log_rss_feed_setup)
        header_layout.addWidget(log_btn)
        
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
        
        # Add log button (new)
        log_btn = QPushButton("Log")
        log_btn.setToolTip("Log research compliance document to a file")
        log_btn.clicked.connect(self._log_research_compliance_document)
        header_layout.addWidget(log_btn)
        
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
        
        # Add log button (new)
        log_btn = QPushButton("Log")
        log_btn.setToolTip("Log research prompt definition to a file")
        log_btn.clicked.connect(self._log_research_prompt_definition)
        header_layout.addWidget(log_btn)
        
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
                    # Store for later use
                    self.research_compliance_content = content
            except Exception as e:
                self.research_compliance_preview.setText(f"Error reading file: {str(e)}")
    
    def _handle_research(self):
        """Handle the research button click - implement RSS scraping logic"""
        print("Research button clicked - Starting RSS scraping process")
        
        # Here we would implement the actual RSS scraping and research logic
        # For now, just display a message
        QMessageBox.information(
            self, 
            "Research Process", 
            "Research process started:\n\n"
            "1. Reading RSS Feeds...\n"
            "2. Extracting article information...\n"
            "3. Handling missing abstracts...\n"
            "4. Preparing data for AI...\n"
            "5. Sending to AI API...\n"
            "6. Processing AI response...\n"
            "7. Research completed!"
        )

    def _log_rss_feed_setup(self):
        """Log RSS feed setup"""
        if not hasattr(self, 'rss_table') or self.rss_table.rowCount() == 0:
            QMessageBox.warning(self, "Error", "No RSS feeds to log")
            return
            
        # Collect all RSS feeds from the table
        feeds = []
        for row in range(self.rss_table.rowCount()):
            name = self.rss_table.item(row, 0).text()
            topic = self.rss_table.item(row, 1).text()
            url = self.rss_table.item(row, 2).text()
            feeds.append({"name": name, "topic": topic, "url": url})
            
        # Create log content
        log_content = f"RSS Feeds - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        log_content += "=" * 80 + "\n\n"
        
        for i, feed in enumerate(feeds, 1):
            log_content += f"Feed #{i}\n"
            log_content += f"Name: {feed['name']}\n"
            log_content += f"Topic: {feed['topic']}\n"
            log_content += f"URL: {feed['url']}\n"
            log_content += "-" * 40 + "\n"
            
        log_content += f"\nTotal Feeds: {len(feeds)}"
        
        # Log the feed content
        if self.agent:
            filename = self.agent.log_rss_feeds(log_content)
            if filename:
                QMessageBox.information(self, "Log Created", f"RSS feeds logged to {filename}")
        else:
            self._save_log_file("rss_feeds", log_content)

    def _log_research_compliance_document(self):
        """Log research compliance document"""
        if hasattr(self, 'research_compliance_content') and self.research_compliance_content:
            if self.agent:
                filename = self.agent.log_research_compliance(self.research_compliance_content)
                if filename:
                    QMessageBox.information(self, "Log Created", f"Research compliance document logged to {filename}")
            else:
                self._save_log_file("research_compliance", self.research_compliance_content)
        else:
            QMessageBox.warning(self, "Error", "No research compliance document content to log")

    def _log_research_prompt_definition(self):
        """Log research prompt definition"""
        if hasattr(self, 'research_prompt_text') and self.research_prompt_text.toPlainText():
            content = self.research_prompt_text.toPlainText()
            model = self.research_model_combo.currentText()
            temperature = self.research_temp_value.value()
            max_tokens = self.research_max_tokens.value()
            
            log_content = f"Model: {model}\n"
            log_content += f"Temperature: {temperature}\n"
            log_content += f"Max Tokens: {max_tokens}\n\n"
            log_content += f"Prompt Content:\n{content}"
            
            if self.agent:
                filename = self.agent.log_research_prompt(
                    content, model, temperature, max_tokens
                )
                if filename:
                    QMessageBox.information(self, "Log Created", f"Research prompt definition logged to {filename}")
            else:
                self._save_log_file("research_prompt", log_content)
        else:
            QMessageBox.warning(self, "Error", "No research prompt content to log")
            
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