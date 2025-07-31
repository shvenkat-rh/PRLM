"""
GitHub PR Analyzer - A tool to analyze GitHub Pull Requests and generate comprehensive summaries.

A sophisticated, AI-powered platform for comprehensive GitHub Pull Request analysis 
featuring an advanced Streamlit-based graphical interface, intelligent conversation 
tracking, timeline analysis, and enterprise-ready reporting.
"""

__version__ = "1.0.0"
__author__ = "PR Analyzer"
__email__ = "contact@example.com"
__license__ = "MIT"
__url__ = "https://github.com/shvenkat-rh/PRLM"

# Import main classes and functions for easy access
try:
    from .main import PRAnalyzer, cli
    from .github_client import GitHubClient, PRData
    from .timeline_analyzer import TimelineAnalyzer
    from .llm_client import LLMClient
    from .repomix_integration import RepomixIntegration
    from .document_generator import DocumentGenerator
    from .conversation_analyzer import ConversationAnalyzer
    from .run_gui import main as launch_gui
except ImportError:
    # Handle case where dependencies might not be installed yet
    pass

__all__ = [
    "__version__",
    "__author__", 
    "__email__",
    "__license__",
    "__url__",
    "PRAnalyzer",
    "cli",
    "GitHubClient",
    "PRData", 
    "TimelineAnalyzer",
    "LLMClient",
    "RepomixIntegration",
    "DocumentGenerator",
    "ConversationAnalyzer",
    "launch_gui"
]
