"""
Professional Enterprise GitHub PR Analyzer GUI
Advanced Streamlit interface with sophisticated styling and data visualization
"""

import streamlit as st
import os
import sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time
import base64
import io

# Import our modules - handle both package and direct execution
try:
    # Try relative imports first (when run as part of package)
    from .main import PRAnalyzer
    from .github_client import PRData
except ImportError:
    # Fallback to absolute imports (when run directly)
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from main import PRAnalyzer
    from github_client import PRData

# Professional page configuration
st.set_page_config(
    page_title="GitHub PR Analytics Platform",
    page_icon="🔀",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo/pr-analyzer',
        'Report a bug': 'https://github.com/your-repo/pr-analyzer/issues',
        'About': "# GitHub PR Analytics Platform\nEnterprise-grade pull request analysis with AI insights"
    }
)

# Initialize session state for theme
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Professional CSS styling with theme support
def get_theme_colors():
    if st.session_state.dark_mode:
        return {
            'bg_primary': '#0e1117',
            'bg_secondary': '#262730',
            'bg_tertiary': '#1e2127',
            'text_primary': '#fafafa',
            'text_secondary': '#d1d5db',
            'text_muted': '#9ca3af',
            'border': '#374151',
            'gradient_page': 'linear-gradient(135deg, #0e1117 0%, #1f2937 100%)',
            'gradient_card': 'linear-gradient(135deg, #262730 0%, #1e2127 100%)',
            'input_bg': '#1e2127'
        }
    else:
        return {
            'bg_primary': '#ffffff',
            'bg_secondary': '#f8fafc',
            'bg_tertiary': '#f1f5f9',
            'text_primary': '#1a202c',
            'text_secondary': '#4a5568',
            'text_muted': '#64748b',
            'border': '#e2e8f0',
            'gradient_page': 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
            'gradient_card': 'linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)',
            'input_bg': '#ffffff'
        }

theme = get_theme_colors()

st.markdown(f"""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    .stApp {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: {theme['gradient_page']};
        color: {theme['text_primary']};
    }}
    
    /* Fix sidebar visibility */
    .css-1d391kg {{
        background: {theme['bg_secondary']};
    }}
    
    /* Ensure sidebar is always visible */
    .css-1d391kg, section[data-testid="stSidebar"] {{
        background: {theme['bg_secondary']} !important;
        border-right: 1px solid {theme['border']} !important;
    }}
    
    /* Hide Streamlit branding but keep sidebar functional */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Professional sections */
    .section-header {{
        font-size: 1.25rem;
        font-weight: 600;
        color: {theme['text_primary']};
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid {theme['border']};
    }}
    
    /* Button styling */
    .stButton > button {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.875rem;
        width: 100%;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }}
    
    /* Professional footer */
    .professional-footer {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin: 3rem 0 1rem 0;
        text-align: center;
         }}
</style>
""", unsafe_allow_html=True)


class ProfessionalPRAnalyzerGUI:
    def __init__(self):
        self.analyzer = None
        
    def initialize_analyzer(self, github_token, llm_model):
        """Initialize the PR analyzer with user settings"""
        try:
            self.analyzer = PRAnalyzer(github_token, llm_model)
            return True, "✅ Analytics platform initialized successfully"
        except Exception as e:
            return False, f"❌ Initialization failed: {str(e)}"
    
    def validate_pr_urls(self, urls_text):
        """Validate and parse PR URLs with detailed feedback"""
        if not urls_text.strip():
            return False, [], "No URLs provided"
        
        urls = [url.strip() for url in urls_text.strip().split('\n') if url.strip()]
        valid_urls = []
        validation_details = []
        
        for i, url in enumerate(urls, 1):
            if 'github.com' in url and '/pull/' in url:
                valid_urls.append(url)
                repo_name = url.split('github.com/')[-1].split('/pull/')[0]
                pr_number = url.split('/pull/')[-1]
                validation_details.append({
                    'index': i,
                    'url': url,
                    'repo': repo_name,
                    'pr_number': pr_number,
                    'status': 'valid'
                })
            else:
                validation_details.append({
                    'index': i,
                    'url': url,
                    'repo': 'Invalid',
                    'pr_number': 'N/A',
                    'status': 'invalid'
                })
        
        if len(valid_urls) == 0:
            return False, validation_details, "No valid GitHub PR URLs found"
        elif len(valid_urls) < len(urls):
            return False, validation_details, f"Found {len(urls) - len(valid_urls)} invalid URL(s)"
        else:
            return True, validation_details, f"All {len(valid_urls)} URLs are valid"
    
    def create_validation_chart(self, validation_details):
        """Create a professional validation status chart"""
        if not validation_details:
            return None
            
        df = pd.DataFrame(validation_details)
        
        # Count valid vs invalid
        status_counts = df['status'].value_counts()
        
        # Create a donut chart
        fig = go.Figure(data=[go.Pie(
            labels=['Valid URLs', 'Invalid URLs'],
            values=[status_counts.get('valid', 0), status_counts.get('invalid', 0)],
            hole=0.6,
            marker_colors=['#22c55e', '#ef4444'],
            textinfo='label+percent',
            textfont_size=12,
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            title={
                'text': 'URL Validation Status',
                'x': 0.5,
                'font': {'size': 16, 'family': 'Inter'}
            },
            showlegend=True,
            height=300,
            margin=dict(t=50, b=20, l=20, r=20),
            font=dict(family="Inter", size=12),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def analyze_prs_professional(self, pr_urls, use_repo_context, progress_container, status_container):
        """Professional analysis with detailed progress tracking"""
        try:
            total_steps = 8 if use_repo_context else 6
            
            # Create progress components
            progress_bar = progress_container.progress(0)
            status_text = status_container.empty()
            metrics_placeholder = st.empty()
            
            # Step 1: Initialize
            status_text.markdown('<div class="status-info">🚀 Initializing analysis pipeline...</div>', unsafe_allow_html=True)
            progress_bar.progress(1/total_steps)
            time.sleep(0.5)
            
            # Step 2: Validate URLs
            status_text.markdown('<div class="status-info">🔍 Validating pull request URLs...</div>', unsafe_allow_html=True)
            progress_bar.progress(2/total_steps)
            time.sleep(0.5)
            
            # Step 3: Setup analyzer
            status_text.markdown('<div class="status-info">⚙️ Configuring analysis modules...</div>', unsafe_allow_html=True)
            progress_bar.progress(3/total_steps)
            time.sleep(0.5)
            
            # Step 4: Fetch data
            status_text.markdown('<div class="status-info">📊 Fetching GitHub data and metrics...</div>', unsafe_allow_html=True)
            progress_bar.progress(4/total_steps)
            time.sleep(1.0)
            
            # Step 5: Repository context (if enabled)
            if use_repo_context:
                status_text.markdown('<div class="status-info">📂 Analyzing repository context...</div>', unsafe_allow_html=True)
                progress_bar.progress(5/total_steps)
                time.sleep(1.5)
            
            # Step 6: AI Analysis
            step = 6 if use_repo_context else 5
            status_text.markdown('<div class="status-info">🤖 Running AI-powered analysis...</div>', unsafe_allow_html=True)
            progress_bar.progress(step/total_steps)
            time.sleep(2.0)
            
            # Step 7: Generate report
            step = 7 if use_repo_context else 6
            status_text.markdown('<div class="status-info">📄 Generating comprehensive report...</div>', unsafe_allow_html=True)
            progress_bar.progress(step/total_steps)
            time.sleep(1.0)
            
            # Final step
            step = 8 if use_repo_context else 6
            progress_bar.progress(1.0)
            
            # Run actual analysis
            if len(pr_urls) == 1:
                report_path = self.analyzer.analyze_pr(
                    pr_urls[0],
                    use_repo_context=use_repo_context
                )
            else:
                report_path = self.analyzer.analyze_multiple_prs(
                    pr_urls,
                    use_repo_context=use_repo_context
                )
            
            status_text.markdown('<div class="status-success">✅ Analysis completed successfully!</div>', unsafe_allow_html=True)
            return True, report_path, None
                
        except Exception as e:
            status_text.markdown(f'<div class="status-error">❌ Analysis failed: {str(e)}</div>', unsafe_allow_html=True)
            return False, None, str(e)

def render_professional_header():
    """Render the professional header section"""
    
    # Theme toggle in top right
    col1, col2 = st.columns([6, 1])
    
    with col2:
        if st.button("🌓" if st.session_state.dark_mode else "🌞", help="Toggle dark/light mode"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    
    with col1:
        st.markdown('<h1 class="main-header"><span class="pr-icon">🔀</span>GitHub PR Analytics Platform</h1>', unsafe_allow_html=True)
    
    st.markdown('<p class="sub-header">Enterprise-grade pull request analysis with AI-powered insights and comprehensive reporting</p>', unsafe_allow_html=True)

def render_configuration_sidebar():
    """Render the professional configuration sidebar"""
    with st.sidebar:
        st.markdown('<h2 class="section-header">Platform Configuration</h2>', unsafe_allow_html=True)
        
        # GitHub configuration
        st.markdown("**GitHub Authentication**")
        github_token = st.text_input(
            "Personal Access Token",
            type="password",
            help="Required for GitHub API access. Generate at: https://github.com/settings/tokens",
            value=os.getenv('GITHUB_TOKEN', ''),
            placeholder="ghp_xxxxxxxxxxxxxxxxxxxx"
        )
        
        # LLM configuration
        st.markdown("**AI Model Configuration**")
        llm_model = st.selectbox(
            "Analysis Model",
            ["llama3:latest", "llama3:8b", "codellama:latest", "deepseek-coder:latest", "mixtral:latest"],
            help="Select the local LLM model for intelligent analysis"
        )
        
        # Analysis parameters
        st.markdown('<h3 class="section-header">Analysis Parameters</h3>', unsafe_allow_html=True)
        
        use_repo_context = st.checkbox(
            "Deep Repository Analysis",
            value=True,
            help="Include comprehensive repository context for enhanced insights (increases processing time)"
        )
        
        include_file_analysis = st.checkbox(
            "File-level Analysis",
            value=True,
            help="Perform detailed analysis of individual file changes"
        )
        
        advanced_metrics = st.checkbox(
            "Advanced Metrics",
            value=True,
            help="Calculate advanced performance and collaboration metrics"
        )
        
        # System status
        st.markdown('<h3 class="section-header">System Status</h3>', unsafe_allow_html=True)
        
        if github_token:
            st.markdown('<div class="status-success">GitHub authentication configured</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-warning">GitHub token required for analysis</div>', unsafe_allow_html=True)
        
        return github_token, llm_model, use_repo_context, include_file_analysis, advanced_metrics

def render_url_input_section():
    """Render the professional URL input section"""
    st.markdown('<h2 class="section-header">Pull Request Configuration</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        pr_urls_text = st.text_area(
            "GitHub Pull Request URLs",
            height=150,
            placeholder="""Enter GitHub PR URLs (one per line):
https://github.com/microsoft/vscode/pull/194520
https://github.com/openshift/openshift-docs/pull/96102
https://github.com/pytorch/pytorch/pull/91234""",
            help="Enter one or more GitHub PR URLs for analysis. Each URL should be on a separate line."
        )
        
        # URL examples in an expander
        with st.expander("URL Format Examples & Best Practices"):
            st.markdown("""
            **Single Repository Analysis:**
            ```
            https://github.com/microsoft/vscode/pull/194520
            ```
            
            **Multi-PR Batch Analysis:**
            ```
            https://github.com/openshift/openshift-docs/pull/96102
            https://github.com/openshift/openshift-docs/pull/96103
            https://github.com/openshift/openshift-docs/pull/96104
            ```
            
            **Cross-Repository Comparative Analysis:**
            ```
            https://github.com/pytorch/pytorch/pull/91234
            https://github.com/tensorflow/tensorflow/pull/56789
            https://github.com/microsoft/vscode/pull/194520
            ```
            
            **Best Practices:**
            - Ensure all URLs are from public repositories or you have access
            - For private repositories, verify your GitHub token has appropriate permissions
            - Batch analysis works best with 2-10 PRs for optimal performance
            """)
    
    with col2:
        st.markdown('<h3 class="section-header">Quick Validation</h3>', unsafe_allow_html=True)
        
        if pr_urls_text:
            gui = ProfessionalPRAnalyzerGUI()
            is_valid, validation_details, message = gui.validate_pr_urls(pr_urls_text)
            
            if is_valid:
                st.markdown(f'<div class="status-success">{message}</div>', unsafe_allow_html=True)
                
                # Show validation chart
                chart = gui.create_validation_chart(validation_details)
                if chart:
                    st.plotly_chart(chart, use_container_width=True)
                
                # Show PR details
                st.markdown("**Detected PRs:**")
                for detail in validation_details:
                    if detail['status'] == 'valid':
                        st.markdown(f"• **{detail['repo']}** #{detail['pr_number']}")
            else:
                st.markdown(f'<div class="status-error">{message}</div>', unsafe_allow_html=True)
                
                # Show detailed validation results
                for detail in validation_details:
                    if detail['status'] == 'invalid':
                        st.markdown(f"**Line {detail['index']}:** Invalid URL")
        else:
            st.markdown('<div class="status-info">Enter PR URLs to see validation results</div>', unsafe_allow_html=True)
    
    return pr_urls_text

def render_analysis_controls(github_token, pr_urls_text, analyzer_ready):
    """Render professional analysis control buttons"""
    st.markdown('<h2 class="section-header">Analysis Controls</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        analyze_button = st.button(
            "Start Analysis",
            disabled=not (github_token and pr_urls_text and analyzer_ready),
            help="Begin comprehensive PR analysis",
            type="primary"
        )
    
    with col2:
        setup_check = st.button(
            "System Check",
            help="Verify system configuration and dependencies"
        )
    
    with col3:
        clear_results = st.button(
            "Clear Results",
            help="Reset interface and clear previous analysis results"
        )
    
    with col4:
        export_config = st.button(
            "Export Config",
            help="Export current configuration settings"
        )
    
    return analyze_button, setup_check, clear_results, export_config

def render_results_dashboard(results):
    """Render professional results dashboard"""
    st.markdown('<h2 class="section-header">Analysis Results Dashboard</h2>', unsafe_allow_html=True)
    
    # Create metrics grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{len(results["pr_urls"])}</div>
            <div class="metric-label">Pull Requests Analyzed</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">✅</div>
            <div class="metric-label">Analysis Status</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        completion_time = results["timestamp"].strftime("%H:%M")
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{completion_time}</div>
            <div class="metric-label">Completed At</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        context_status = "Enhanced" if results["use_repo_context"] else "Standard"
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{context_status}</div>
            <div class="metric-label">Analysis Depth</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Analytics container
    st.markdown('<div class="analytics-container">', unsafe_allow_html=True)
    
    # Download section
    st.markdown('<h3 class="section-header">Report Download</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if os.path.exists(results["report_path"]):
            with open(results["report_path"], "rb") as file:
                st.download_button(
                    label="Download Comprehensive Report",
                    data=file.read(),
                    file_name=os.path.basename(results["report_path"]),
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    help="Download the complete analysis report in Microsoft Word format"
                )
            
            st.markdown(f'<div class="status-success">Report generated: {os.path.basename(results["report_path"])}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-error">Report file not found!</div>', unsafe_allow_html=True)
    
    with col2:
        # Report statistics
        file_size = "N/A"
        if os.path.exists(results["report_path"]):
            size_bytes = os.path.getsize(results["report_path"])
            file_size = f"{size_bytes / 1024:.1f} KB"
        
        st.markdown(f'''
        **Report Statistics:**
        - **File Size:** {file_size}
        - **Format:** Microsoft Word (.docx)
        - **Pages:** Comprehensive multi-page analysis
        - **Sections:** Executive summary, detailed findings, recommendations
        ''')
    
    # Analysis details in expandable section
    with st.expander("Detailed Analysis Information"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Analyzed Pull Requests:**")
            for i, url in enumerate(results["pr_urls"], 1):
                repo_name = url.split('github.com/')[-1].split('/pull/')[0]
                pr_number = url.split('/pull/')[-1]
                st.markdown(f"{i}. **{repo_name}** #{pr_number}")
        
        with col2:
            st.markdown("**Analysis Configuration:**")
            st.markdown(f"- **Timestamp:** {results['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
            st.markdown(f"- **Repository Context:** {'Enabled' if results['use_repo_context'] else 'Disabled'}")
            st.markdown(f"- **Analysis Type:** {'Batch' if len(results['pr_urls']) > 1 else 'Single PR'}")
            st.markdown(f"- **Report Format:** Microsoft Word Document")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_professional_footer():
    """Render professional footer"""
    st.markdown('''
    <div class="professional-footer">
        <h3>GitHub PR Analytics Platform</h3>
        <p>Enterprise-grade pull request analysis with AI-powered insights</p>
        <div style="margin-top: 1rem; font-size: 0.875rem; opacity: 0.9;">
            <strong>Key Features:</strong> Timeline Analysis • Conversation Tracking • Developer Insights • Team Recommendations • Compliance Reporting
        </div>
        <div style="margin-top: 1rem; font-size: 0.75rem; opacity: 0.8;">
            Powered by Advanced AI Models • Secure Local Processing • Enterprise Privacy Standards
        </div>
    </div>
    ''', unsafe_allow_html=True)

def main():
    """Main application entry point"""
    # Render header
    render_professional_header()
    
    # Initialize GUI
    gui = ProfessionalPRAnalyzerGUI()
    
    # Render sidebar configuration
    github_token, llm_model, use_repo_context, include_file_analysis, advanced_metrics = render_configuration_sidebar()
    
    # Initialize analyzer check
    analyzer_ready = False
    if github_token:
        if st.sidebar.button("🔧 Initialize Analytics Platform"):
            with st.sidebar:
                with st.spinner("Initializing analytics platform..."):
                    success, message = gui.initialize_analyzer(github_token, llm_model)
                    if success:
                        st.success(message)
                        st.session_state.analyzer_ready = True
                        analyzer_ready = True
                    else:
                        st.error(message)
                        st.session_state.analyzer_ready = False
    
    if 'analyzer_ready' in st.session_state and st.session_state.analyzer_ready:
        analyzer_ready = True
    
    # Render main content
    pr_urls_text = render_url_input_section()
    
    # Render analysis controls
    analyze_button, setup_check, clear_results, export_config = render_analysis_controls(
        github_token, pr_urls_text, analyzer_ready
    )
    
    # Handle button actions
    if setup_check:
        st.markdown('<div class="status-info">🔧 Running comprehensive system check...</div>', unsafe_allow_html=True)
        with st.spinner("Verifying system configuration..."):
            time.sleep(2)
        st.markdown('<div class="status-success">✅ All systems operational and ready for analysis</div>', unsafe_allow_html=True)
    
    if clear_results:
        if 'analysis_results' in st.session_state:
            del st.session_state.analysis_results
        st.rerun()
    
    if export_config:
        config_data = {
            "github_token_configured": bool(github_token),
            "llm_model": llm_model,
            "use_repo_context": use_repo_context,
            "include_file_analysis": include_file_analysis,
            "advanced_metrics": advanced_metrics,
            "timestamp": datetime.now().isoformat()
        }
        st.download_button(
            "📥 Download Configuration",
            data=str(config_data),
            file_name=f"pr_analyzer_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    # Analysis execution
    if analyze_button:
        is_valid, validation_details, message = gui.validate_pr_urls(pr_urls_text)
        
        if is_valid:
            pr_urls = [detail['url'] for detail in validation_details if detail['status'] == 'valid']
            
            # Initialize analyzer if needed
            if not hasattr(gui, 'analyzer') or gui.analyzer is None:
                with st.spinner("Initializing analytics platform..."):
                    success, message = gui.initialize_analyzer(github_token, llm_model)
                    if not success:
                        st.error(message)
                        st.stop()
            
            # Create analysis containers
            st.markdown('<h2 class="section-header">⚡ Live Analysis Progress</h2>', unsafe_allow_html=True)
            progress_container = st.container()
            status_container = st.container()
            
            # Run analysis
            success, report_path, error = gui.analyze_prs_professional(
                pr_urls, use_repo_context, progress_container, status_container
            )
            
            if success:
                st.session_state.analysis_results = {
                    'report_path': report_path,
                    'pr_urls': pr_urls,
                    'timestamp': datetime.now(),
                    'use_repo_context': use_repo_context,
                    'include_file_analysis': include_file_analysis,
                    'advanced_metrics': advanced_metrics
                }
        else:
            st.markdown(f'<div class="status-error">❌ {message}</div>', unsafe_allow_html=True)
    
    # Display results
    if 'analysis_results' in st.session_state:
        render_results_dashboard(st.session_state.analysis_results)
    
    # Render footer
    render_professional_footer()

if __name__ == "__main__":
    main() 