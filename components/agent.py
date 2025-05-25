import os
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import json # Import the json library

class Agent:
    def __init__(self, action_widget):
        print("Agent initialized.")
        self.action_widget = action_widget # Store the ActionWidget instance

    def handle_execute(self):
        print("Handling Execute...")
        # 1. Read context from compliance document and prompt definition
        # Placeholder: Implement reading from files or configuration
        compliance_doc_content = "Content of compliance document..."
        prompt_definition_content = "Content of prompt definition..."

        # 2. Parse RSS feed content
        # Placeholder: Get RSS feed URLs from configuration or UI
        rss_feed_urls = ["http://example.com/feed.xml", "http://anothersite.com/rss"]
        abstracts = self._process_rss_feeds(rss_feed_urls)

        if not abstracts:
            print("No abstracts found or processed.")
            return

        # 3. Send payload to LLM
        payload = self._prepare_llm_payload(prompt_definition_content, compliance_doc_content, abstracts)
        llm_response = self._call_llm_api(payload)

        # 4. Use LLM's function calling API to populate Suggested Action widget
        if llm_response:
            suggested_actions = self._suggest_action(llm_response)
            if suggested_actions:
                print("Suggested Actions:", suggested_actions)
                # Update the Suggested Action widget with suggested_actions
                if self.action_widget:
                    self.action_widget.display_suggestions(suggested_actions) # Call a method on ActionWidget
                else:
                    print("ActionWidget not available.")
            else:
                print("Could not extract suggested actions from LLM response.")
        else:
            print("LLM API call failed or returned no response.")

    def _process_rss_feeds(self, feed_urls):
        """Fetches and processes RSS feeds to extract relevant information."""
        feed_items = []
        for url in feed_urls:
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()  # Raise an exception for HTTP errors
                root = ET.fromstring(response.content)

                # Assuming standard RSS structure (channel -> item)
                for item in root.findall('.//item'):
                    title = item.find('title').text if item.find('title') is not None else 'No Title'
                    link = item.find('link').text if item.find('link') is not None else 'No Link'
                    description = item.find('description').text if item.find('description') is not None else ''

                    # Use description as abstract if available, otherwise try scraping
                    abstract_or_desc = description.strip()

                    # Placeholder: if no abstract/summary, try to scrape from link
                    if not abstract_or_desc and link and link != 'No Link':
                        print(f"No description for {title}, attempting to scrape from link: {link}")
                        abstract_or_desc = self._scrape_abstract_from_link(link)

                    if title and link and abstract_or_desc:
                        feed_items.append({
                            'title': title,
                            'link': link,
                            'content': abstract_or_desc # Using 'content' key for consistency
                        })
                    else:
                        print(f"Skipping item due to missing info: Title={title}, Link={link}, Abstract={bool(abstract_or_desc)}")

            except requests.exceptions.RequestException as e:
                print(f"Error fetching RSS feed {url}: {e}")
            except ET.ParseError as e:
                print(f"Error parsing RSS feed {url}: {e}")
            except Exception as e:
                print(f"An unexpected error occurred processing feed {url}: {e}")

        return feed_items

    def _scrape_abstract_from_link(self, link):
        """Fetches and scrapes the abstract from a given URL."""
        try:
            response = requests.get(link, timeout=10)
            response.raise_for_status()  # Raise an exception for HTTP errors
            soup = BeautifulSoup(response.content, 'html.parser')

            # Placeholder for actual abstract extraction logic
            # This is highly dependent on the structure of the target websites.
            # Common strategies include looking for <meta name="description">,
            # <meta property="og:description">, or specific article body tags.
            abstract_tag = soup.find('meta', attrs={'name': 'description'})
            if abstract_tag and abstract_tag.get('content'):
                return abstract_tag.get('content').strip()

            abstract_tag_og = soup.find('meta', attrs={'property': 'og:description'})
            if abstract_tag_og and abstract_tag_og.get('content'):
                return abstract_tag_og.get('content').strip()

            # Add more sophisticated scraping logic here if needed
            # For example, looking for specific divs or paragraphs
            # For now, returning a placeholder if not found via meta tags
            print(f"Abstract not found via meta tags for {link}. Further scraping logic needed.")
            return "Abstract not found."

        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL {link}: {e}")
            return None
        except Exception as e:
            print(f"Error scraping abstract from {link}: {e}")
            return None

    def _prepare_llm_payload(self, prompt_definition, compliance_content, abstracts):
        """Prepares the payload for the LLM API call."""
        # Constructing a detailed prompt for the LLM
        # This can be further customized based on the LLM's requirements

        formatted_abstracts = "\n".join([f"- {abstract['title']}: {abstract['content']}" for abstract in abstracts])

        payload = {
            "model": "gpt-3.5-turbo", # Or any other model you intend to use
            "messages": [
                {
                    "role": "system",
                    "content": "You are an AI assistant. Your task is to analyze research abstracts based on a given prompt and a compliance document. Suggest an action: discard, review, or publish."
                },
                {
                    "role": "user",
                    "content": f"""
                        Prompt Definition:
                        {prompt_definition}

                        Compliance Document:
                        {compliance_content}

                        Research Abstracts:
                        {formatted_abstracts}

                        Based on the above, please analyze each abstract and suggest an action (discard, review, publish) and provide a brief justification.
                        """
                }
            ],
            "functions": [
                {
                    "name": "suggest_actions_for_abstracts",
                    "description": "Suggests actions (discard, review, publish) for a list of research abstracts.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "suggestions": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "title": {"type": "string", "description": "Title of the research abstract"},
                                        "action": {"type": "string", "enum": ["discard", "review", "publish"], "description": "Suggested action for the abstract"},
                                        "justification": {"type": "string", "description": "Brief justification for the suggested action"}
                                    },
                                    "required": ["title", "action", "justification"]
                                }
                            }
                        },
                        "required": ["suggestions"]
                    }
                }
            ],
            "function_call": {"name": "suggest_actions_for_abstracts"}
        }
        return payload

    def _call_llm_api(self, payload):
        """Calls the LLM API with the prepared payload."""
        LLM_API_ENDPOINT = "YOUR_LLM_API_ENDPOINT" # Replace with your LLM API endpoint
        YOUR_LLM_API_KEY = "YOUR_LLM_API_KEY"     # Replace with your LLM API key

        if LLM_API_ENDPOINT == "YOUR_LLM_API_ENDPOINT" or YOUR_LLM_API_KEY == "YOUR_LLM_API_KEY":
            print("LLM API endpoint or key not configured. Using mock response.")
            # Return mock response if not configured
            return {
                "choices": [
                    {
                        "message": {
                            "function_call": {
                                "name": "suggest_actions_for_abstracts",
                                "arguments": "{\"suggestions\": [{\"title\": \"Test Abstract 1\", \"action\": \"review\", \"justification\": \"Needs further review for compliance.\"}, {\"title\": \"Test Abstract 2\", \"action\": \"publish\", \"justification\": \"Looks good and compliant.\"}]}"
                            }
                        }
                    }
                ]
            }

        headers = {
            "Authorization": f"Bearer {YOUR_LLM_API_KEY}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(LLM_API_ENDPOINT, json=payload, headers=headers, timeout=60)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error calling LLM API: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred during LLM API call: {e}")
            return None

    def _suggest_action(self, llm_response):
        """Parses the LLM response and extracts suggested actions."""
        if not llm_response or 'choices' not in llm_response or not llm_response['choices']:
            print("Invalid or empty LLM response.")
            return None

        try:
            # Assuming the LLM uses the defined function 'suggest_actions_for_abstracts'
            message = llm_response['choices'][0]['message']
            if 'function_call' in message and message['function_call']['name'] == 'suggest_actions_for_abstracts':
                # The arguments are a JSON string within the 'arguments' field
                function_args_str = message['function_call']['arguments']
                function_args = json.loads(function_args_str)
                
                if 'suggestions' in function_args:
                    return function_args['suggestions']
                else:
                    print("LLM response function call missing 'suggestions' key.")
                    return None
            else:
                print("LLM response did not contain expected function call.")
                return None

        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"Error parsing LLM response: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred while processing LLM response: {e}")
            return None

    def handle_research(self):
        print("Handling Ongoing Research...")
        # Placeholder for ongoing research logic
        pass