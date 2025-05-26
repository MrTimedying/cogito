import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import json
import os
# No PySide6 import needed here for the fixes requested

class Agent:
    # Correct the constructor name from init to __init__
    def __init__(self, action_widget):
        print("Agent initialized.")
        self.action_widget = action_widget
        self.current_output = None  # Store current LLM output for editing
        self.current_loop_active = False  # Track if we're in the execute loop
        self.debug_mode = False  # Initialize debug mode flag as added in the previous turn

        # Connect action widget buttons to our handlers
        if self.action_widget:
            # Only disconnect if the buttons have connections
            try:
                # These lines are already correctly wrapped in a try/except
                # to handle the RuntimeWarning when no connections exist.
                self.action_widget.publish_button.clicked.disconnect()  # Remove existing connections
                self.action_widget.review_button.clicked.disconnect()
                self.action_widget.discard_button.clicked.disconnect()
            except RuntimeError:
                # Ignore errors if there are no connections to disconnect
                pass

            self.action_widget.publish_button.clicked.connect(self.handle_publish)
            self.action_widget.review_button.clicked.connect(self.handle_edit)
            self.action_widget.discard_button.clicked.connect(self.handle_discard)

    def set_debug_mode(self, enabled):
        """Set the debug mode flag"""
        self.debug_mode = enabled
        print(f"Debug mode {'enabled' if enabled else 'disabled'}")

    def validate_preconditions(self, main_workspace):
        """Validate that all required preconditions are met before executing."""
        errors = []

        # Check if compliance document is uploaded
        if not hasattr(main_workspace, 'compliance_content') or not main_workspace.compliance_content:
            errors.append("Compliance Document not completed")

        # Check if prompt is defined with LLM and API key
        if not hasattr(main_workspace, 'prompt_content') or not main_workspace.prompt_content:
            errors.append("Prompt Definition not completed")
        elif not hasattr(main_workspace, 'selected_model') or not main_workspace.selected_model:
            errors.append("LLM model not selected in Prompt Definition")
        elif not hasattr(main_workspace, 'api_key') or not main_workspace.api_key:
            errors.append("API key not provided in Prompt Definition")

        # Check if context is uploaded
        if not hasattr(main_workspace, 'context_content') or not main_workspace.context_content:
            errors.append("Context not uploaded")

        # Check if document is proofread
        if not hasattr(main_workspace, 'proofread_content') or not main_workspace.proofread_content:
            errors.append("Document not proof-read")

        return errors

    def handle_execute_produce(self, main_workspace):
        """Handle the Execute Produce button - this is the main entry point for the Execute loop."""
        print("Execute Produce button clicked - validating preconditions...")

        # Step 1: Validate preconditions
        validation_errors = self.validate_preconditions(main_workspace)
        if validation_errors:
            error_message = "Cannot proceed. Please complete the following:\n" + "\n".join([f"• {error}" for error in validation_errors])
            print(error_message)
            if self.action_widget:
                self.action_widget.display_error(error_message)
            return

        print("All preconditions met. Starting Execute loop...")
        self.current_loop_active = True

        # Step 2: Assemble input
        combined_input = self.assemble_input(
            main_workspace.prompt_content,
            main_workspace.context_content,
            main_workspace.compliance_content,
            main_workspace.proofread_content
        )

        # Step 3: LLM Invocation
        payload = self.prepare_execute_payload(
            combined_input,
            main_workspace.selected_model,
            main_workspace.api_key
        )

        # This calls the modified _call_llm_api which respects debug_mode
        llm_response = self._call_llm_api(payload, main_workspace.api_key, main_workspace.selected_model)

        # Step 4: Present output with action options
        if llm_response:
            self.current_output = self.extract_blog_content(llm_response)
            if self.current_output:
                self.present_output_actions(self.current_output)
            else:
                print("Failed to extract blog content from LLM response.")
                if self.action_widget:
                    self.action_widget.display_error("Failed to generate blog content. Please try again.")
        else:
            print("LLM API call failed.")
            if self.action_widget:
                self.action_widget.display_error("LLM API call failed. Please check your API key and try again.")

    def assemble_input(self, prompt, context, compliance, proofread):
        """Assemble all inputs into a combined prompt for the LLM."""
        combined_input = f"""
User-defined Prompt:
{prompt}

Uploaded Context:
{context}

Compliance Document:
{compliance}

Proof-read Document:
{proofread}

Please generate a blog article based on the above information, following the compliance requirements and incorporating the provided context.
"""
        return combined_input

    def prepare_execute_payload(self, combined_input, model, api_key):
        """Prepare the payload for the Execute LLM API call."""
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a professional blog writer. Generate high-quality blog articles based on the provided prompt, context, compliance requirements, and proofread document."
                },
                {
                    "role": "user",
                    "content": combined_input
                }
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        return payload

    def extract_blog_content(self, llm_response):
        """Extract the blog content from the LLM response."""
        try:
            if 'choices' in llm_response and llm_response['choices']:
                return llm_response['choices'][0]['message']['content']
            return None
        except (KeyError, IndexError) as e:
            print(f"Error extracting blog content: {e}")
            return None

    def present_output_actions(self, output):
        """Present the output with Publish/Edit/Discard action options."""
        if self.action_widget:
            # Create a compact card showing the output and action buttons
            action_card = {
                "type": "blog_output",
                "content": output[:500] + "..." if len(output) > 500 else output,  # Show preview
                "full_content": output,
                "actions": ["Publish", "Edit", "Discard"]
            }
            self.action_widget.display_output_card(action_card)

    def handle_publish(self):
        """Handle the Publish action - placeholder for future Sanity API integration."""
        if not self.current_loop_active or not self.current_output:
            return

        print("Publishing blog article...")
        # TODO: Implement Sanity API call here
        print("Blog article published successfully! (Placeholder)")

        if self.action_widget:
            self.action_widget.display_success("Blog article published successfully!")

        # End the loop
        self.current_loop_active = False
        self.current_output = None

    def handle_edit(self):
        """Handle the Edit action - open text editor for the output."""
        if not self.current_loop_active or not self.current_output:
            return

        print("Opening text editor for blog article...")

        if self.action_widget:
            # Open a full-featured text editor with the current output
            edited_content = self.action_widget.open_text_editor(self.current_output)
            if edited_content is not None:  # User saved the edited content
                self.current_output = edited_content
                # Present the edited content for another round of actions
                self.present_output_actions(self.current_output)

    def handle_discard(self):
        """Handle the Discard action - terminate the process."""
        if not self.current_loop_active:
            return

        print("Discarding blog article and terminating process...")

        if self.action_widget:
            self.action_widget.display_info("Blog article discarded. Process terminated.")
            self.action_widget.clear_suggestions()

        # End the loop
        self.current_loop_active = False
        self.current_output = None

    def _call_llm_api(self, payload, api_key=None, model=None):
        """Calls the LLM API with the prepared payload."""
        # Determine API endpoint based on model for logging purposes
        if model and model.startswith('gpt'):
            LLM_API_ENDPOINT = "[https://api.openai.com/v1/chat/completions](https://api.openai.com/v1/chat/completions)"
        elif model and model.startswith('claude'):
            LLM_API_ENDPOINT = "[https://api.anthropic.com/v1/messages](https://api.anthropic.com/v1/messages)"
        else:
            LLM_API_ENDPOINT = "[https://api.openai.com/v1/chat/completions](https://api.openai.com/v1/chat/completions)"  # Default to OpenAI

        # Log the payload regardless of debug mode
        # Use the determined endpoint in the log message
        log_content = f"API Call Simulation/Payload:\nEndpoint: {LLM_API_ENDPOINT}\nPayload:\n{json.dumps(payload, indent=2)}"
        self._log_to_file(log_content, prefix="api_call")
        print(f"Logged API call details to file. Simulating call to endpoint: {LLM_API_ENDPOINT}")


        # If debug mode is enabled, return a mock response immediately
        if self.debug_mode:
            print("Debug mode enabled. Using mock response instead of actual API call.")
            return {
                "choices": [
                    {
                        "message": {
                            "content": "[DEBUG MODE] This is a sample blog article generated for testing purposes. The actual LLM API call was skipped. Payload received:\n\n" + json.dumps(payload, indent=2)
                        }
                    }
                ]
            }

        # If not in debug mode, proceed with the actual API call logic
        print("Debug mode disabled. Attempting actual LLM API call.")
        if not api_key:
            print("API key not provided. Cannot make actual API call. Using mock response.")
            # Return mock response if no API key, even outside debug mode (though this should be caught by validate_preconditions)
            return {
                "choices": [
                    {
                        "message": {
                            "content": "This is a sample blog article generated because API key was missing. In a real implementation, this would be the actual LLM-generated content based on your prompt, context, compliance document, and proofread document."
                        }
                    }
                ]
            }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        try:
            print(f"Making actual API call to {LLM_API_ENDPOINT}...")
            response = requests.post(LLM_API_ENDPOINT, json=payload, headers=headers, timeout=60)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            print("API call successful.")
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error calling LLM API: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred during LLM API call: {e}")
            return None

    # The pack_contexts method is unchanged as it's for logging, not the API call payload assembly
    def pack_contexts(self, main_workspace):
        """Pack all contexts (compliance document, prompt, context, proofread document) into a single digestible content for API call.
        Also logs the output to a file for inspection.

        Returns:
            dict: A dictionary containing the packed contexts and metadata
        """
        # Get all the contexts from the workspace
        contexts = {
            "compliance_document": getattr(main_workspace, 'compliance_content', ''),
            "prompt": getattr(main_workspace, 'prompt_content', ''),
            "context": getattr(main_workspace, 'context_content', ''),
            "proofread_document": getattr(main_workspace, 'proofread_content', ''),
            "model": getattr(main_workspace, 'selected_model', ''),
            "temperature": getattr(main_workspace, 'temperature', 0.7),
            "max_tokens": getattr(main_workspace, 'max_tokens', 4000),
            "timestamp": self._get_timestamp()
        }

        # Create a formatted string representation for logging
        log_content = f"""=== COGITO CONTEXT PACK ===
        Timestamp: {contexts['timestamp']}
        Model: {contexts['model']}
        Temperature: {contexts['temperature']}
        Max Tokens: {contexts['max_tokens']}

        === COMPLIANCE DOCUMENT ===
        {contexts['compliance_document']}

        === PROMPT ===
        {contexts['prompt']}

        === CONTEXT ===
        {contexts['context']}

        === PROOFREAD DOCUMENT ===
        {contexts['proofread_document']}

        === END OF CONTEXT PACK ===
        """

        # Log to file
        self._log_to_file(log_content)

        print("Context pack created and logged to file.")
        return contexts

    def _get_timestamp(self):
        """Get current timestamp in a readable format."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    def _log_to_file(self, content, prefix="context_pack"):
        """Log content to a file in the project directory.

        Args:
            content (str): The content to log
            prefix (str): A prefix for the log filename
        """
        try:
            # Create logs directory if it doesn't exist
            if not os.path.exists("logs"):
                os.makedirs("logs")

            # Create log file with timestamp
            filename = f"logs/cogito_{prefix}_{self._get_timestamp()}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"Log file created: {filename}")
            return filename
        except Exception as e:
            print(f"Error writing log file: {e}")
            return None

    # Log methods remain unchanged as they are for logging data inputs
    def log_compliance_document(self, content):
        """Log compliance document content"""
        log_content = f"=== COGITO COMPLIANCE DOCUMENT ===\nTimestamp: {self._get_timestamp()}\n\n{content}\n\n=== END OF COMPLIANCE DOCUMENT ==="
        filename = self._log_to_file(log_content, prefix="compliance")
        return filename

    def log_prompt_definition(self, content, model, temperature, max_tokens):
        """Log prompt definition content"""
        log_content = f"=== COGITO PROMPT DEFINITION ===\nTimestamp: {self._get_timestamp()}\nModel: {model}\nTemperature: {temperature}\nMax Tokens: {max_tokens}\n\n{content}\n\n=== END OF PROMPT DEFINITION ==="
        filename = self._log_to_file(log_content, prefix="prompt")
        return filename

    def log_context_upload(self, content):
        """Log context upload content"""
        log_content = f"=== COGITO CONTEXT UPLOAD ===\nTimestamp: {self._get_timestamp()}\n\n{content}\n\n=== END OF CONTEXT UPLOAD ==="
        filename = self._log_to_file(log_content, prefix="context")
        return filename

    def log_proofread_document(self, content):
        """Log proofread document content"""
        log_content = f"=== COGITO PROOFREAD DOCUMENT ===\nTimestamp: {self._get_timestamp()}\n\n{content}\n\n=== END OF PROOFREAD DOCUMENT ==="
        filename = self._log_to_file(log_content, prefix="proofread")
        return filename

    def log_research_compliance(self, content):
        """Log research compliance document content"""
        log_content = f"=== COGITO RESEARCH COMPLIANCE DOCUMENT ===\nTimestamp: {self._get_timestamp()}\n\n{content}\n\n=== END OF RESEARCH COMPLIANCE DOCUMENT ==="
        filename = self._log_to_file(log_content, prefix="research_compliance")
        return filename

    def log_research_prompt(self, content, model, temperature, max_tokens):
        """Log research prompt definition content"""
        log_content = f"=== COGITO RESEARCH PROMPT DEFINITION ===\nTimestamp: {self._get_timestamp()}\nModel: {model}\nTemperature: {temperature}\nMax Tokens: {max_tokens}\n\n{content}\n\n=== END OF RESEARCH PROMPT DEFINITION ==="
        filename = self._log_to_file(log_content, prefix="research_prompt")
        return filename

    def log_rss_feeds(self, feeds):
        """Log RSS feeds content"""
        log_content = f"=== COGITO RSS FEEDS ===\nTimestamp: {self._get_timestamp()}\n\n{feeds}\n\n=== END OF RSS FEEDS ==="
        filename = self._log_to_file(log_content, prefix="rss_feeds")
        return filename