# Agent Description

This document outlines the definition and behavior of the Agent class within the Cogito application.

## Premise

The Agent encapsulates the core logic for processing user requests related to 'Execute' and 'Ongoing Research' functionalities. It interacts with an LLM via specific APIs, including function calling for application actions.

## Agent Definition

1.  **Operating Logics:** The agent operates based on two primary user interactions:
    1.1.  User calls "Execute" in the "Execute" component.
    1.2.  User calls "Research" in the "Ongoing Research" component.

2.  **"Execute" Handling Logic:**
    *   Reads context from the compliancy document.
    *   Reads the prompt from the prompt definition.
    *   Based on the RSS Feed Setup:
        *   Parses content of XML feed files.
        *   If an abstract is present, it's attached to the API context for the LLM.
        *   If an abstract is not present, it visits each article link to find, parse, and include the abstract in the payload.
    *   The final payload includes the prompt, compliancy document, and abstracts/scraped abstracts from RSS feeds.
    *   Leverages the LLM's function calling API to populate the Suggested Action widget with the result and a potential action.

3.  **Potential Actions (for now):**
    *   `discard`: Discards and deletes the output.
    *   `review`: Opens a separate text editor component for review and editing.
        *   Requires a highly customizable text editor library.
        *   Should function as a full text editor within a text area.
    *   `publish`: Makes an API call to Sanity to publish the content as a post.
        *   If content is being reviewed/edited, publishing is delayed until the edited version is ready.