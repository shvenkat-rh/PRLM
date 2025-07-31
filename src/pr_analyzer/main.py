"""
Main CLI interface for the PR Analyzer tool.
"""

import click
import logging
import os
import sys
from typing import Optional, List
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text
import traceback

# Import our modules
# Handle both package and direct execution imports
try:
    from .github_client import GitHubClient, PRData
    from .timeline_analyzer import TimelineAnalyzer
    from .llm_client import LLMClient
    from .repomix_integration import RepomixIntegration
    from .document_generator import DocumentGenerator
    from .conversation_analyzer import ConversationAnalyzer
except ImportError:
    from github_client import GitHubClient, PRData
    from timeline_analyzer import TimelineAnalyzer
    from llm_client import LLMClient
    from repomix_integration import RepomixIntegration
    from document_generator import DocumentGenerator
    from conversation_analyzer import ConversationAnalyzer

# Set up console for rich output
console = Console()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pr_analyzer.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class PRAnalyzer:
    """Main PR Analyzer orchestrator"""
    
    def __init__(self, github_token: Optional[str] = None, llm_model: str = "llama3:latest"):
        """Initialize the PR Analyzer"""
        self.github_client = None
        self.timeline_analyzer = TimelineAnalyzer()
        self.llm_client = None
        self.repomix_integration = RepomixIntegration()
        self.document_generator = DocumentGenerator()
        self.conversation_analyzer = ConversationAnalyzer()
        
        # Initialize GitHub client
        try:
            self.github_client = GitHubClient(github_token)
            console.print("✓ GitHub client initialized", style="green")
        except Exception as e:
            console.print(f"✗ Failed to initialize GitHub client: {e}", style="red")
            raise
        
        # Initialize LLM client
        try:
            self.llm_client = LLMClient(llm_model)
            console.print(f"✓ LLM client initialized with {llm_model}", style="green")
        except Exception as e:
            console.print(f"✗ Failed to initialize LLM client: {e}", style="red")
            console.print("Make sure ollama is running and llama3:latest is installed", style="yellow")
            raise
    
    def analyze_pr(self, pr_url: str, use_repo_context: bool = True, output_path: Optional[str] = None) -> str:
        """
        Analyze a PR and generate a comprehensive report
        
        Args:
            pr_url: GitHub PR URL
            use_repo_context: Whether to use repository context from repomix
            output_path: Custom output path for the Word document
            
        Returns:
            Path to generated report
        """
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            
            # Step 1: Fetch PR data
            task1 = progress.add_task("Fetching PR data from GitHub...", total=None)
            try:
                pr_data = self.github_client.fetch_pr_data(pr_url)
                progress.update(task1, description="✓ PR data fetched")
                console.print(f"Analyzing PR: {pr_data.title}", style="bold blue")
            except Exception as e:
                progress.update(task1, description="✗ Failed to fetch PR data")
                console.print(f"Error fetching PR data: {e}", style="red")
                raise
            
            # Step 2: Analyze timeline
            task2 = progress.add_task("Analyzing PR timeline...", total=None)
            try:
                timeline_metrics = self.timeline_analyzer.analyze_timeline(pr_data)
                progress.update(task2, description="✓ Timeline analyzed")
            except Exception as e:
                progress.update(task2, description="✗ Timeline analysis failed")
                console.print(f"Error analyzing timeline: {e}", style="red")
                raise
            
            # Step 3: Get repository context (optional)
            repo_context = ""
            if use_repo_context:
                task3 = progress.add_task("Getting repository context with repomix...", total=None)
                try:
                    # Extract repo URL from PR URL
                    repo_url = pr_url.split('/pull/')[0] + '.git'
                    
                    # Get focused context for changed files
                    changed_file_paths = [f['filename'] for f in pr_data.changed_files[:10]]  # Limit to 10 files
                    repo_context = self.repomix_integration.get_focused_context(
                        repo_url, changed_file_paths
                    )
                    progress.update(task3, description="✓ Repository context obtained")
                except Exception as e:
                    progress.update(task3, description="⚠ Repository context failed (continuing without)")
                    console.print(f"Warning: Could not get repository context: {e}", style="yellow")
                    repo_context = ""
            
            # Step 4: Analyze conversations
            task4 = progress.add_task("Analyzing conversations and comments...", total=None)
            try:
                conversation_analysis = self.conversation_analyzer.analyze_conversations(pr_data)
                progress.update(task4, description="✓ Conversation analysis complete")
            except Exception as e:
                progress.update(task4, description="⚠ Conversation analysis failed (continuing)")
                console.print(f"Warning: Conversation analysis failed: {e}", style="yellow")
                conversation_analysis = {}
            
            # Step 5: Perform LLM analysis
            task5 = progress.add_task("Performing AI analysis...", total=None)
            try:
                analysis_result = self.llm_client.analyze_pr_comprehensive(
                    pr_data, timeline_metrics, repo_context
                )
                progress.update(task5, description="✓ AI analysis complete")
            except Exception as e:
                progress.update(task5, description="✗ AI analysis failed")
                console.print(f"Error during AI analysis: {e}", style="red")
                raise
            
            # Step 6: Detailed file analysis
            task6 = progress.add_task("Analyzing individual files...", total=None)
            try:
                file_analysis = self.llm_client.analyze_code_changes(
                    pr_data.changed_files, pr_data.title + " " + (pr_data.description[:200] if pr_data.description else "")
                )
                progress.update(task6, description="✓ File analysis complete")
            except Exception as e:
                progress.update(task6, description="⚠ File analysis failed (continuing)")
                console.print(f"Warning: File analysis failed: {e}", style="yellow")
                file_analysis = {}
            
            # Step 7: Generate document
            task7 = progress.add_task("Generating comprehensive Word document...", total=None)
            try:
                report_path = self.document_generator.create_pr_analysis_report(
                    pr_data, timeline_metrics, analysis_result, file_analysis, conversation_analysis, output_path
                )
                progress.update(task7, description="✓ Document generated")
            except Exception as e:
                progress.update(task7, description="✗ Document generation failed")
                console.print(f"Error generating document: {e}", style="red")
                raise
        
        # Display summary
        self._display_analysis_summary(pr_data, timeline_metrics, analysis_result, report_path)
        
        return report_path
    
    def analyze_multiple_prs(self, pr_urls: List[str], use_repo_context: bool = True, output_path: Optional[str] = None) -> str:
        """
        Analyze multiple PRs and generate a combined comprehensive report
        
        Args:
            pr_urls: List of GitHub PR URLs
            use_repo_context: Whether to use repository context from repomix
            output_path: Custom output path for the Word document
            
        Returns:
            Path to generated combined report
        """
        
        console.print(f"\n[bold blue]Analyzing {len(pr_urls)} Pull Requests[/bold blue]")
        
        all_pr_data = []
        all_timeline_metrics = []
        all_analysis_results = []
        all_file_analyses = []
        all_conversation_analyses = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            
            for i, pr_url in enumerate(pr_urls, 1):
                console.print(f"\n[bold yellow]Processing PR {i}/{len(pr_urls)}[/bold yellow]")
                
                try:
                    # Step 1: Fetch PR data
                    task1 = progress.add_task(f"Fetching PR {i} data from GitHub...", total=None)
                    pr_data = self.github_client.fetch_pr_data(pr_url)
                    progress.update(task1, description=f"✓ PR {i} data fetched")
                    console.print(f"  PR {i}: {pr_data.title[:60]}...")
                    
                    # Step 2: Analyze timeline
                    task2 = progress.add_task(f"Analyzing PR {i} timeline...", total=None)
                    timeline_metrics = self.timeline_analyzer.analyze_timeline(pr_data)
                    progress.update(task2, description=f"✓ PR {i} timeline analyzed")
                    
                    # Step 3: Get repository context (optional, only for first PR to avoid redundancy)
                    repo_context = ""
                    if use_repo_context and i == 1:  # Only get context for first PR
                        task3 = progress.add_task(f"Getting repository context...", total=None)
                        try:
                            repo_url = pr_url.split('/pull/')[0] + '.git'
                            changed_file_paths = [f['filename'] for f in pr_data.changed_files[:10]]
                            repo_context = self.repomix_integration.get_focused_context(
                                repo_url, changed_file_paths
                            )
                            progress.update(task3, description="✓ Repository context obtained")
                        except Exception as e:
                            progress.update(task3, description="⚠ Repository context failed (continuing)")
                            console.print(f"Warning: Could not get repository context: {e}", style="yellow")
                            repo_context = ""
                    
                    # Step 4: Analyze conversations
                    task4 = progress.add_task(f"Analyzing PR {i} conversations...", total=None)
                    try:
                        conversation_analysis = self.conversation_analyzer.analyze_conversations(pr_data)
                        progress.update(task4, description=f"✓ PR {i} conversation analysis complete")
                    except Exception as e:
                        progress.update(task4, description=f"⚠ PR {i} conversation analysis failed")
                        console.print(f"Warning: Conversation analysis failed for PR {i}: {e}", style="yellow")
                        conversation_analysis = {}
                    
                    # Step 5: Perform LLM analysis
                    task5 = progress.add_task(f"Performing AI analysis for PR {i}...", total=None)
                    try:
                        analysis_result = self.llm_client.analyze_pr_comprehensive(
                            pr_data, timeline_metrics, repo_context
                        )
                        progress.update(task5, description=f"✓ PR {i} AI analysis complete")
                    except Exception as e:
                        progress.update(task5, description=f"✗ PR {i} AI analysis failed")
                        console.print(f"Error during AI analysis for PR {i}: {e}", style="red")
                        # Continue with empty analysis rather than failing
                        analysis_result = None
                    
                    # Step 6: Detailed file analysis
                    task6 = progress.add_task(f"Analyzing PR {i} files...", total=None)
                    try:
                        file_analysis = self.llm_client.analyze_code_changes(
                            pr_data.changed_files, pr_data.title + " " + (pr_data.description[:200] if pr_data.description else "")
                        )
                        progress.update(task6, description=f"✓ PR {i} file analysis complete")
                    except Exception as e:
                        progress.update(task6, description=f"⚠ PR {i} file analysis failed")
                        console.print(f"Warning: File analysis failed for PR {i}: {e}", style="yellow")
                        file_analysis = {}
                    
                    # Store results
                    all_pr_data.append(pr_data)
                    all_timeline_metrics.append(timeline_metrics)
                    all_analysis_results.append(analysis_result)
                    all_file_analyses.append(file_analysis)
                    all_conversation_analyses.append(conversation_analysis)
                    
                except Exception as e:
                    console.print(f"[bold red]✗ Failed to analyze PR {i}: {e}[/bold red]")
                    # Continue with remaining PRs
                    continue
            
            # Step 7: Generate combined document
            task7 = progress.add_task("Generating combined analysis report...", total=None)
            try:
                report_path = self.document_generator.create_combined_pr_analysis_report(
                    all_pr_data, all_timeline_metrics, all_analysis_results, 
                    all_file_analyses, all_conversation_analyses, output_path
                )
                progress.update(task7, description="✓ Combined document generated")
            except Exception as e:
                progress.update(task7, description="✗ Document generation failed")
                console.print(f"Error generating combined document: {e}", style="red")
                raise
        
        # Display combined summary
        self._display_combined_analysis_summary(all_pr_data, all_timeline_metrics, all_analysis_results, report_path)
        
        return report_path
    
    def _display_analysis_summary(self, pr_data: PRData, timeline_metrics, analysis_result, report_path: str):
        """Display a summary of the analysis results"""
        
        # Create summary panel
        summary_text = Text()
        summary_text.append(f"PR: {pr_data.title}\n", style="bold")
        summary_text.append(f"Author: {pr_data.author}\n")
        summary_text.append(f"Files changed: {len(pr_data.changed_files)}\n")
        summary_text.append(f"Comments: {len(pr_data.comments)}\n")
        summary_text.append(f"Review cycles: {timeline_metrics.review_cycles}\n")
        
        if timeline_metrics.time_to_first_review:
            summary_text.append(f"Time to first review: {timeline_metrics.time_to_first_review:.1f} hours\n")
        
        if timeline_metrics.time_to_merge:
            summary_text.append(f"Time to merge: {timeline_metrics.time_to_merge:.1f} hours\n")
            
        summary_text.append(f"\nReport saved to: {report_path}", style="green bold")
        
        panel = Panel(
            summary_text,
            title="[bold blue]Analysis Complete[/bold blue]",
            border_style="blue"
        )
        
        console.print(panel)
        
        # Display key insights
        if analysis_result:
            if analysis_result.key_changes:
                console.print("\n[bold yellow]Key Changes:[/bold yellow]")
                for i, change in enumerate(analysis_result.key_changes[:3], 1):
                    console.print(f"  {i}. {change}")
            
            if analysis_result.developer_mistakes:
                console.print("\n[bold red]Learning Opportunities:[/bold red]")
                for i, mistake in enumerate(analysis_result.developer_mistakes[:3], 1):
                    console.print(f"  {i}. {mistake}")
    
    def _display_combined_analysis_summary(self, all_pr_data: List[PRData], all_timeline_metrics, all_analysis_results, report_path: str):
        """Display a summary of the combined analysis results"""
        
        # Create combined summary panel
        summary_text = Text()
        summary_text.append(f"Combined Analysis of {len(all_pr_data)} Pull Requests\n\n", style="bold")
        
        total_files = sum(len(pr.changed_files) for pr in all_pr_data)
        total_comments = sum(len(pr.comments) for pr in all_pr_data)
        avg_time_to_review = sum(tm.time_to_first_review or 0 for tm in all_timeline_metrics) / len(all_timeline_metrics)
        avg_time_to_merge = sum(tm.time_to_merge or 0 for tm in all_timeline_metrics if tm.time_to_merge) / max(1, len([tm for tm in all_timeline_metrics if tm.time_to_merge]))
        
        summary_text.append(f"Total files changed: {total_files}\n")
        summary_text.append(f"Total comments: {total_comments}\n")
        summary_text.append(f"Average time to first review: {avg_time_to_review:.1f} hours\n")
        if avg_time_to_merge > 0:
            summary_text.append(f"Average time to merge: {avg_time_to_merge:.1f} hours\n")
        
        summary_text.append(f"\nCombined report saved to: {report_path}", style="green bold")
        
        panel = Panel(
            summary_text,
            title="[bold blue]Combined Analysis Complete[/bold blue]",
            border_style="blue"
        )
        
        console.print(panel)
        
        # Show individual PR summaries
        console.print("\n[bold yellow]Individual PR Summary:[/bold yellow]")
        for i, (pr_data, timeline_metrics) in enumerate(zip(all_pr_data, all_timeline_metrics), 1):
            console.print(f"  {i}. {pr_data.title[:80]}...")
            console.print(f"     Author: {pr_data.author} | Files: {len(pr_data.changed_files)} | Comments: {len(pr_data.comments)}")
            if timeline_metrics.time_to_merge:
                console.print(f"     Time to merge: {timeline_metrics.time_to_merge:.1f} hours")
            console.print()

@click.command()
@click.argument('pr_urls', nargs=-1, required=True)
@click.option('--github-token', '-t', 
              help='GitHub access token (or set GITHUB_TOKEN env var)')
@click.option('--llm-model', '-m', default='llama3:latest',
              help='LLM model to use for analysis (default: llama3:latest)')
@click.option('--output', '-o', 
              help='Output path for the Word document')
@click.option('--no-repo-context', is_flag=True,
              help='Skip repository context generation (faster but less detailed)')
@click.option('--verbose', '-v', is_flag=True,
              help='Enable verbose logging')
def analyze_pr_cmd(pr_urls: tuple, github_token: Optional[str], llm_model: str, 
                   output: Optional[str], no_repo_context: bool, verbose: bool):
    """
    Analyze one or more GitHub Pull Requests and generate a comprehensive report.
    
    PR_URLS: One or more GitHub Pull Request URLs (e.g., https://github.com/owner/repo/pull/123)
    
    Examples:
    
        # Single PR analysis
        pr-analyzer https://github.com/microsoft/vscode/pull/12345
        
        # Multiple PR analysis in one report
        pr-analyzer https://github.com/owner/repo/pull/123 https://github.com/owner/repo/pull/124
        
        # Multiple PRs with custom output
        pr-analyzer https://github.com/owner/repo/pull/123 https://github.com/owner/repo/pull/124 --output batch_analysis.docx
        
        # Fast analysis without repo context
        pr-analyzer https://github.com/owner/repo/pull/123 https://github.com/owner/repo/pull/124 --no-repo-context
    """
    
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    console.print(Panel.fit(
        "[bold blue]GitHub PR Analyzer[/bold blue]\n"
        "Analyzing pull request with AI-powered insights",
        border_style="blue"
    ))
    
    try:
        # Initialize analyzer
        analyzer = PRAnalyzer(github_token, llm_model)
        
        # Convert tuple to list
        pr_url_list = list(pr_urls)
        
        if len(pr_url_list) == 1:
            # Single PR analysis
            report_path = analyzer.analyze_pr(
                pr_url_list[0], 
                use_repo_context=not no_repo_context,
                output_path=output
            )
        else:
            # Multiple PR analysis
            report_path = analyzer.analyze_multiple_prs(
                pr_url_list,
                use_repo_context=not no_repo_context,
                output_path=output
            )
        
        console.print(f"\n[bold green]✓ Analysis complete![/bold green]")
        console.print(f"Report saved to: [bold]{report_path}[/bold]")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Analysis interrupted by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]✗ Analysis failed:[/bold red] {str(e)}")
        if verbose:
            console.print("[dim]" + traceback.format_exc() + "[/dim]")
        sys.exit(1)

@click.group()
def cli():
    """GitHub PR Analyzer - Comprehensive analysis of pull requests"""
    pass

@cli.command()
def setup():
    """Set up the PR analyzer environment"""
    console.print(Panel.fit(
        "[bold blue]PR Analyzer Setup[/bold blue]\n"
        "Checking and setting up environment",
        border_style="blue"
    ))
    
    # Check GitHub token
    github_token = os.getenv('GITHUB_TOKEN')
    if github_token:
        console.print("✓ GitHub token found in environment", style="green")
    else:
        console.print("⚠ GitHub token not found. Set GITHUB_TOKEN environment variable", style="yellow")
        console.print("  Get a token from: https://github.com/settings/tokens")
    
    # Check ollama and llama3
    try:
        import ollama
        models = ollama.list()
        if 'models' in models:
            model_names = []
            for model in models['models']:
                if hasattr(model, 'model'):
                    model_names.append(model.model)
                elif isinstance(model, dict):
                    model_names.append(model.get('name', model.get('model', '')))
                else:
                    model_names.append(str(model))
        else:
            model_names = []
        
        if 'llama3:latest' in model_names:
            console.print("✓ llama3:latest model found", style="green")
        else:
            console.print("⚠ llama3:latest not found. Install with: ollama pull llama3:latest", style="yellow")
            console.print(f"  Available models: {', '.join(model_names[:5])}")
            
    except Exception as e:
        console.print(f"✗ Ollama not available: {e}", style="red")
        console.print("  Install ollama from: https://ollama.ai")
    
    # Check repomix
    try:
        import subprocess
        result = subprocess.run(['repomix', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            console.print("✓ Repomix available", style="green")
        else:
            console.print("⚠ Repomix not found. Install with: npm install -g repomix", style="yellow")
    except Exception:
        console.print("⚠ Repomix not found. Install with: npm install -g repomix", style="yellow")
    
    # Create output directory
    os.makedirs('output', exist_ok=True)
    console.print("✓ Output directory created", style="green")
    
    console.print("\n[bold green]Setup check complete![/bold green]")

# Add commands to the CLI group
cli.add_command(analyze_pr_cmd, name='analyze')

@cli.command('gui')
def launch_gui_cmd():
    """Launch the professional GUI interface"""
    import subprocess
    import os
    
    # Get the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gui_launcher = os.path.join(script_dir, "run_gui.py")
    
    print("🚀 Launching Professional GitHub PR Analytics Platform...")
    print("📊 Opening enterprise-grade GUI interface...")
    
    try:
        subprocess.run([sys.executable, gui_launcher])
    except KeyboardInterrupt:
        print("\n👋 GUI stopped by user")
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")
        print("💡 Try running: streamlit run src/pr_analyzer/pr_analyzer_gui.py")

def main():
    """Main entry point"""
    cli()

if __name__ == '__main__':
    main() 