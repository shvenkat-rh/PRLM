#!/usr/bin/env python3
"""
Example usage of the PR Analyzer tool.

This script demonstrates how to analyze GitHub Pull Requests programmatically.
"""

import os
from src.pr_analyzer.main import PRAnalyzer

def main():
    """Example usage of the PR Analyzer"""
    
    # Example PR URLs to analyze (replace with real PRs)
    example_prs = [
        # You can test with any public GitHub PR:
        # "https://github.com/microsoft/vscode/pull/194520",
        # "https://github.com/pytorch/pytorch/pull/91234",
        # "https://github.com/tensorflow/tensorflow/pull/56789",
    ]
    
    if not example_prs:
        print("Please add some PR URLs to the example_prs list in this script")
        print("Example: https://github.com/owner/repo/pull/123")
        return
    
    # Check if GitHub token is set
    if not os.getenv('GITHUB_TOKEN'):
        print("Please set your GITHUB_TOKEN environment variable")
        print("Get a token from: https://github.com/settings/tokens")
        return
    
    try:
        # Initialize the analyzer
        print("Initializing PR Analyzer...")
        analyzer = PRAnalyzer()
        
        # Analyze each PR
        for pr_url in example_prs:
            print(f"\nAnalyzing PR: {pr_url}")
            
            # Run analysis
            report_path = analyzer.analyze_pr(
                pr_url,
                use_repo_context=True,  # Set to False for faster analysis without repo context
                output_path=None        # Let it auto-generate the filename
            )
            
            print(f"✅ Analysis complete! Report saved to: {report_path}")
            
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        print("Make sure:")
        print("1. GITHUB_TOKEN is set correctly")
        print("2. Ollama is running with llama3:latest")
        print("3. The PR URL is valid and accessible")

if __name__ == "__main__":
    main() 