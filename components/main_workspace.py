# This file has been refactored into:
# - components/execute_workspace.py - For execute workflow functionality
# - components/research_workspace.py - For ongoing research functionality
# - components/base_workspace.py - For shared functionality
# - components/pdf_processor.py - For PDF processing functionality

# Please use ExecuteWorkspace and ResearchWorkspace classes instead of MainWorkspace

print("Warning: main_workspace.py is deprecated. Use execute_workspace.py and research_workspace.py instead.")

from .execute_workspace import ExecuteWorkspace
from .research_workspace import ResearchWorkspace

# Legacy import support
MainWorkspace = ExecuteWorkspace 