import os
import re
import PyPDF2  # Use PyPDF2 instead of PyMuPDF
import nltk
from nltk.tokenize import sent_tokenize
from datetime import datetime

# Download NLTK data if not already present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class PDFProcessor:
    """
    Class to handle PDF processing operations including:
    - Text extraction
    - Cleaning and preprocessing
    - Chunking text for token limits
    - Token counting
    - Metadata extraction
    """
    
    def __init__(self):
        """Initialize the PDF processor"""
        self.processed_pdfs = {}  # Store processed PDF content
        
    def process_pdf(self, file_path):
        """
        Process a PDF file - extract text, clean, and chunk
        
        Args:
            file_path (str): Path to the PDF file
            
        Returns:
            dict: Dictionary with processed content and metadata
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        # Extract basic metadata
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path) / 1024  # KB
        
        # Extract text
        raw_text = self._extract_text(file_path)
        
        # Clean text
        cleaned_text = self._clean_text(raw_text)
        
        # Chunk text
        chunks = self._chunk_text(cleaned_text)
        
        # Count tokens (approximation)
        token_count = self._estimate_token_count(cleaned_text)
        
        result = {
            'file_path': file_path,
            'file_name': file_name,
            'file_size': file_size,  # in KB
            'raw_text': raw_text,
            'cleaned_text': cleaned_text,
            'chunks': chunks,
            'token_count': token_count,
            'processed_at': datetime.now().isoformat()
        }
        
        # Store in our processed PDFs dict
        self.processed_pdfs[file_path] = result
        
        return result
    
    def _extract_text(self, file_path):
        """
        Extract text from PDF using PyPDF2
        
        Args:
            file_path (str): Path to the PDF file
            
        Returns:
            str: Extracted text
        """
        text = ""
        try:
            # Open the PDF file
            with open(file_path, 'rb') as pdf_file:
                # Create a PDF reader object
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                
                # Extract text from each page
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() or ""  # Some pages might return None
                    # Add page markers to help with structure
                    text += f"\n\n--- Page {page_num + 1} ---\n\n"
        except Exception as e:
            print(f"Error extracting text from PDF: {str(e)}")
            text = f"[Error extracting PDF: {str(e)}]"
            
        return text
    
    def _clean_text(self, text):
        """
        Clean and normalize the extracted text
        
        Args:
            text (str): Raw text from PDF
            
        Returns:
            str: Cleaned text
        """
        if not text:
            return ""
            
        # Replace multiple newlines with single ones
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Remove strange Unicode artifacts
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        
        # Fix common OCR/PDF extraction issues
        text = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', text)  # Fix merged words
        
        # Replace tabs with spaces
        text = re.sub(r'\t+', ' ', text)
        
        # Replace multiple spaces with single ones
        text = re.sub(r' {2,}', ' ', text)
        
        return text.strip()
    
    def _chunk_text(self, text, chunk_size=1000):
        """
        Split text into manageable chunks
        
        Args:
            text (str): Text to chunk
            chunk_size (int): Approximate target size for each chunk in words
            
        Returns:
            list: List of text chunks
        """
        if not text:
            return []
            
        # Try to split at logical points like paragraphs or sentences
        paragraphs = re.split(r'\n{2,}', text)
        
        chunks = []
        current_chunk = ""
        current_size = 0
        
        for para in paragraphs:
            # If paragraph is very long, break it into sentences
            if len(para.split()) > chunk_size:
                sentences = sent_tokenize(para)
                for sentence in sentences:
                    sentence_size = len(sentence.split())
                    
                    # If adding this sentence exceeds chunk size, start a new chunk
                    if current_size + sentence_size > chunk_size and current_chunk:
                        chunks.append(current_chunk.strip())
                        current_chunk = sentence
                        current_size = sentence_size
                    else:
                        current_chunk += " " + sentence
                        current_size += sentence_size
            else:
                para_size = len(para.split())
                
                # If adding this paragraph exceeds chunk size, start a new chunk
                if current_size + para_size > chunk_size and current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = para
                    current_size = para_size
                else:
                    if current_chunk:
                        current_chunk += "\n\n" + para
                    else:
                        current_chunk = para
                    current_size += para_size
        
        # Add the last chunk if it's not empty
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks
    
    def _estimate_token_count(self, text):
        """
        Estimate token count in text
        A rough approximation is 4 characters per token for English text
        
        Args:
            text (str): Text to count tokens for
            
        Returns:
            int: Estimated token count
        """
        if not text:
            return 0
        
        # Count words (space-separated tokens)
        word_count = len(text.split())
        
        # Adjust for typical tokenization rules (rough approximation)
        # For English text, number of tokens is typically around 0.75 * word_count
        # We return a slight overestimate to be safe
        estimated_tokens = int(word_count * 1.25)
        
        return estimated_tokens
        
    def get_combined_text(self, file_paths, max_tokens=None):
        """
        Get combined processed text from multiple PDFs with optional token limit
        
        Args:
            file_paths (list): List of PDF file paths
            max_tokens (int, optional): Maximum token limit
            
        Returns:
            tuple: (combined_text, total_token_count)
        """
        if not file_paths:
            return "", 0, []
        
        # Process any unprocessed PDFs
        for file_path in file_paths:
            if file_path not in self.processed_pdfs:
                self.process_pdf(file_path)
        
        combined_text = ""
        total_tokens = 0
        processed_files = []
        
        for file_path in file_paths:
            if file_path in self.processed_pdfs:
                pdf_data = self.processed_pdfs[file_path]
                file_tokens = pdf_data['token_count']
                
                # Check if adding this file would exceed token limit
                if max_tokens and (total_tokens + file_tokens > max_tokens):
                    # If we're over limit, don't add this file
                    continue
                
                # Add file content with metadata header
                file_content = f"--- Document: {pdf_data['file_name']} ---\n\n"
                file_content += pdf_data['cleaned_text']
                file_content += f"\n\n--- End of {pdf_data['file_name']} ---\n\n"
                
                combined_text += file_content
                total_tokens += file_tokens
                processed_files.append(pdf_data['file_name'])
                
                # Stop if we've hit the token limit
                if max_tokens and total_tokens >= max_tokens:
                    break
        
        return combined_text, total_tokens, processed_files
        
    def log_processed_content(self, file_paths):
        """
        Generate a log of all processed content
        
        Args:
            file_paths (list): List of PDF file paths
            
        Returns:
            str: Log content
        """
        if not file_paths:
            return "No PDFs to log."
        
        # Process any unprocessed PDFs
        for file_path in file_paths:
            if file_path not in self.processed_pdfs:
                self.process_pdf(file_path)
                
        log_content = f"PDF Processing Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        log_content += "=" * 80 + "\n\n"
        
        total_tokens = 0
        
        for file_path in file_paths:
            if file_path in self.processed_pdfs:
                pdf_data = self.processed_pdfs[file_path]
                
                log_content += f"File: {pdf_data['file_name']}\n"
                log_content += f"Size: {pdf_data['file_size']:.2f} KB\n"
                log_content += f"Token Count: {pdf_data['token_count']}\n"
                log_content += f"Processed At: {pdf_data['processed_at']}\n"
                log_content += "-" * 40 + "\n"
                log_content += "Cleaned Content:\n" # Changed the label
                log_content += pdf_data['cleaned_text'] + "\n\n" # Removed the slicing
                
                total_tokens += pdf_data['token_count']
                
        log_content += "=" * 80 + "\n"
        log_content += f"Total Files: {len(file_paths)}\n"
        log_content += f"Total Tokens: {total_tokens}\n"
        
        return log_content