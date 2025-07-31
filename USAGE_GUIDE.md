# 📊 GitHub PR Analytics Platform - Usage Guide

> **Complete guide for using the enterprise-grade PR analytics platform**

## 🚀 Quick Start Options

### **Option 1: Professional GUI (Recommended)**
```bash
# Launch the enterprise GUI interface
python -m src.pr_analyzer.main gui
```

### **Option 2: Command Line Interface**
```bash
# Analyze a single PR
python -m src.pr_analyzer.main analyze https://github.com/owner/repo/pull/123

# Analyze multiple PRs
python -m src.pr_analyzer.main analyze \
  https://github.com/owner/repo/pull/123 \
  https://github.com/owner/repo/pull/124 \
  https://github.com/owner/repo/pull/125
```

### **Option 3: Demo Mode**
```bash
# Experience the full demo with professional showcase
python src/pr_analyzer/demo_setup.py
```

## 🎨 Professional GUI Interface

### **Launching the GUI**
```bash
# Method 1: CLI command (easiest)
python -m src.pr_analyzer.main gui

# Method 2: Direct launcher
python src/pr_analyzer/run_gui.py

# Method 3: Streamlit direct
streamlit run src/pr_analyzer/pr_analyzer_gui.py

# Method 4: Professional demo
python src/pr_analyzer/demo_setup.py
```

### **GUI Features**
- **🎨 Enterprise Design**: Professional gradients and modern typography
- **📊 Interactive Dashboard**: Real-time metrics and data visualization
- **🔄 Progress Tracking**: Multi-step analysis with detailed status updates
- **⚙️ Configuration Management**: Organized sidebar with intelligent defaults
- **📄 Report Generation**: Professional Word document creation and download

### **Using the Professional Interface**

#### **Step 1: Configuration**
1. **GitHub Token**: Enter your personal access token in the sidebar
2. **AI Model**: Select from available local LLM models
3. **Analysis Options**: Configure repository context and advanced features
4. **Initialize**: Click "Initialize Analytics Platform"

#### **Step 2: PR Input**
1. **URL Entry**: Paste GitHub PR URLs (one per line) in the main text area
2. **Validation**: Watch real-time validation with visual feedback
3. **Examples**: Use the expandable section for URL format guidance

#### **Step 3: Analysis**
1. **Start Analysis**: Click the professional "Start Analysis" button
2. **Progress Monitoring**: Watch the multi-step progress with detailed status
3. **Real-time Updates**: View live status messages and progress indicators

#### **Step 4: Results**
1. **Dashboard Metrics**: View professional metric cards with key statistics
2. **Download Report**: Get comprehensive Word document with analysis
3. **Detailed View**: Expand sections for in-depth analysis information

## 💻 Command Line Interface

### **Basic Commands**
```bash
# Setup and verification
python -m src.pr_analyzer.main setup

# Launch professional GUI
python -m src.pr_analyzer.main gui

# Analyze single PR
python -m src.pr_analyzer.main analyze https://github.com/owner/repo/pull/123

# Analyze multiple PRs (batch processing)
python -m src.pr_analyzer.main analyze \
  https://github.com/microsoft/vscode/pull/194520 \
  https://github.com/openshift/openshift-docs/pull/96102 \
  https://github.com/pytorch/pytorch/pull/91234
```

### **Advanced Options**
```bash
# Custom GitHub token
python -m src.pr_analyzer.main analyze \
  https://github.com/owner/repo/pull/123 \
  --github-token YOUR_TOKEN

# Different LLM model
python -m src.pr_analyzer.main analyze \
  https://github.com/owner/repo/pull/123 \
  --llm-model llama3:8b

# Custom output directory
python -m src.pr_analyzer.main analyze \
  https://github.com/owner/repo/pull/123 \
  --output-dir /path/to/reports

# Skip repository context (faster)
python -m src.pr_analyzer.main analyze \
  https://github.com/owner/repo/pull/123 \
  --no-repo-context

# Verbose output
python -m src.pr_analyzer.main analyze \
  https://github.com/owner/repo/pull/123 \
  --verbose
```

## 🔧 Configuration

### **Environment Variables**
```bash
# GitHub authentication
export GITHUB_TOKEN="ghp_your_token_here"

# Optional: Custom configurations
export PR_ANALYZER_LLM_MODEL="llama3:latest"
export PR_ANALYZER_OUTPUT_DIR="./reports"
```

### **Configuration File**
Edit `config/config.yaml` for advanced settings:
```yaml
github:
  default_timeout: 30
  rate_limit_retry: true

llm:
  default_model: "llama3:latest"
  temperature: 0.1
  max_tokens: 2048

analysis:
  max_files_to_analyze: 15
  include_conversation_analysis: true
  
output:
  default_directory: "output"
  include_appendix: true
```

## 📊 Analysis Examples

### **Single Repository Deep Dive**
```bash
# Comprehensive analysis of a complex PR
python -m src.pr_analyzer.main analyze \
  https://github.com/microsoft/vscode/pull/194520 \
  --verbose
```

### **Cross-Repository Comparison**
```bash
# Compare PRs across different repositories
python -m src.pr_analyzer.main analyze \
  https://github.com/pytorch/pytorch/pull/91234 \
  https://github.com/tensorflow/tensorflow/pull/56789 \
  https://github.com/microsoft/vscode/pull/194520
```

### **Team Performance Analysis**
```bash
# Analyze multiple PRs from a team/sprint
python -m src.pr_analyzer.main analyze \
  https://github.com/openshift/openshift-docs/pull/96102 \
  https://github.com/openshift/openshift-docs/pull/96103 \
  https://github.com/openshift/openshift-docs/pull/96104 \
  https://github.com/openshift/openshift-docs/pull/96105
```

## 🎯 Sample Workflows

### **Workflow 1: Quick PR Review**
```bash
# 1. Quick setup check
python -m src.pr_analyzer.main setup

# 2. Fast analysis without repo context
python -m src.pr_analyzer.main analyze \
  https://github.com/owner/repo/pull/123 \
  --no-repo-context
```

### **Workflow 2: Comprehensive Team Review**
```bash
# 1. Launch professional GUI
python -m src.pr_analyzer.main gui

# 2. Use GUI to:
#    - Configure GitHub token and AI model
#    - Enter multiple PR URLs
#    - Enable repository context
#    - Download comprehensive reports
```

### **Workflow 3: Automated CI/CD Integration**
```bash
#!/bin/bash
# CI script for automated PR analysis

# Set environment variables
export GITHUB_TOKEN="${GITHUB_TOKEN}"

# Analyze PR from CI environment
python -m src.pr_analyzer.main analyze \
  "${GITHUB_PR_URL}" \
  --output-dir "./ci-reports" \
  --no-repo-context \
  --llm-model llama3:8b
```

## 🔒 Security & Privacy

### **Token Management**
- **Secure Storage**: Tokens are never stored permanently
- **Environment Variables**: Use `GITHUB_TOKEN` environment variable
- **GUI Security**: Password-masked input fields
- **Session Management**: Secure session state handling

### **Data Privacy**
- **Local Processing**: All analysis runs on your machine
- **No Data Upload**: PR data never leaves your environment
- **Enterprise Standards**: Privacy-focused design
- **Audit Capabilities**: Comprehensive logging available

## 📈 Performance Optimization

### **Speed Tips**
```bash
# Fastest analysis (skip repo context)
python -m src.pr_analyzer.main analyze URL --no-repo-context

# Use smaller model for speed
python -m src.pr_analyzer.main analyze URL --llm-model llama3:8b

# Limit file analysis in config.yaml
analysis:
  max_files_to_analyze: 5
```

### **Quality vs Speed**
- **Maximum Quality**: Enable repository context, use llama3:latest
- **Balanced**: Repository context enabled, llama3:8b model
- **Maximum Speed**: No repository context, llama3:8b model

## 🛡️ Troubleshooting

### **Common Issues**

#### **GUI Won't Start**
```bash
# Check dependencies
pip install streamlit plotly pandas

# Try direct launch
streamlit run src/pr_analyzer/pr_analyzer_gui.py

# Check port availability
lsof -i :8501
```

#### **GitHub API Issues**
```bash
# Verify token
export GITHUB_TOKEN="your_token"
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user

# Check rate limits
python -m src.pr_analyzer.main setup
```

#### **LLM Model Issues**
```bash
# Verify Ollama is running
ollama list

# Pull required model
ollama pull llama3:latest

# Test model
ollama run llama3:latest "Hello"
```

### **Professional Support**
- **Error Messages**: GUI provides clear, actionable error descriptions
- **Status Indicators**: Real-time system health monitoring
- **Help Documentation**: Contextual help throughout the interface
- **Debug Mode**: Verbose logging for troubleshooting

## 🎓 Advanced Usage

### **Programmatic Access**
```python
from src.pr_analyzer.main import PRAnalyzer

# Initialize analyzer
analyzer = PRAnalyzer(
    github_token="your_token",
    llm_model="llama3:latest"
)

# Single PR analysis
report_path = analyzer.analyze_pr(
    "https://github.com/owner/repo/pull/123",
    use_repo_context=True
)

# Multiple PR analysis
report_path = analyzer.analyze_multiple_prs([
    "https://github.com/owner/repo/pull/123",
    "https://github.com/owner/repo/pull/124"
])
```

### **Custom Integration**
- **API Endpoints**: RESTful API for enterprise integration
- **Webhook Support**: Automated analysis on PR events
- **Custom Themes**: Configurable visual themes
- **Plugin Architecture**: Extensible analysis modules

---

## 🚀 Get Started Now

**Choose Your Experience:**

1. **🎨 Professional GUI**: `python -m src.pr_analyzer.main gui`
2. **⚡ Quick CLI**: `python -m src.pr_analyzer.main analyze <PR_URL>`
3. **🎯 Full Demo**: `python src/pr_analyzer/demo_setup.py`

**Experience the future of PR analysis with our enterprise-grade platform!** 