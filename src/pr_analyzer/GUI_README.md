# GitHub PR Analyzer GUI

A beautiful, modern graphical interface for analyzing GitHub Pull Requests with AI-powered insights.

## 🌟 Features

### ✨ **Modern Interface**
- Clean, responsive design with beautiful gradients and animations
- Real-time progress tracking and status updates
- Intuitive sidebar configuration
- Interactive charts and visualizations

### 🔍 **Analysis Capabilities**
- **Single PR Analysis** - Detailed analysis of individual pull requests
- **Multiple PR Analysis** - Batch analysis with comparative insights
- **Real-time Progress** - Live updates during analysis
- **Download Reports** - Generate Word documents with comprehensive analysis

### 🎯 **Key Sections**
1. **Configuration Panel** - GitHub token, LLM model selection, analysis options
2. **PR Input Area** - Simple URL input with validation
3. **Analysis Dashboard** - Progress tracking and status monitoring
4. **Results Viewer** - Metrics, charts, and download options

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install streamlit plotly pandas
```

### 2. Launch GUI
```bash
# Option 1: Use the launcher script
python gui/run_gui.py

# Option 2: Direct Streamlit command
streamlit run gui/pr_analyzer_gui.py
```

### 3. Access Interface
- Open your browser to: **http://localhost:8501**
- The GUI will automatically open in your default browser

## 💡 Usage Guide

### **Step 1: Configuration**
1. Enter your GitHub token in the sidebar
2. Select your preferred LLM model
3. Choose analysis options (repository context, etc.)
4. Click "Initialize Analyzer"

### **Step 2: Add PR URLs**
1. Paste GitHub PR URLs in the main text area
2. One URL per line for multiple PRs
3. URLs are automatically validated

### **Step 3: Run Analysis**
1. Click "Start Analysis" 
2. Watch real-time progress updates
3. Wait for completion notification

### **Step 4: Download Results**
1. View analysis metrics and summary
2. Download the comprehensive Word report
3. Access detailed insights and recommendations

## 🎨 Interface Components

### **Sidebar Configuration**
- **GitHub Token**: Secure input for authentication
- **LLM Model**: Select from available local models
- **Analysis Options**: Toggle repository context inclusion
- **System Status**: Real-time status indicators

### **Main Dashboard**
- **URL Input**: Large text area with validation
- **Progress Tracking**: Visual progress bars and status
- **Results Metrics**: Key statistics in beautiful cards
- **Download Center**: Easy access to generated reports

### **Visual Elements**
- **Gradient Backgrounds**: Modern visual appeal
- **Color-coded Status**: Green (success), blue (info), orange (warning)
- **Interactive Cards**: Hover effects and animations
- **Responsive Layout**: Works on different screen sizes

## 🔧 Configuration Options

### **GitHub Settings**
- **Token Input**: Your GitHub personal access token
- **Repository Access**: Automatically handles public/private repos

### **Analysis Settings**
- **LLM Model**: Choose from locally installed models
- **Repository Context**: Include/exclude full repo analysis
- **Progress Updates**: Real-time status and progress tracking

### **Output Settings**
- **Report Format**: Microsoft Word (.docx) documents
- **File Naming**: Automatic timestamp-based naming
- **Download Location**: Browser's default download folder

## 📊 Analysis Results

### **Metrics Dashboard**
- **PR Count**: Number of analyzed pull requests
- **Completion Status**: Success/failure indicators  
- **Timestamp**: When analysis was completed
- **Options Used**: Repository context and other settings

### **Report Contents**
- **Executive Summary**: High-level overview and metrics
- **Timeline Analysis**: Review cycles, merge times, response patterns
- **Conversation Analysis**: Reviewer comments and back-and-forth
- **Developer Insights**: Mistakes, learning opportunities, suggestions
- **Team Recommendations**: Process improvements and best practices

## 🎯 Examples

### **Single PR Analysis**
```
https://github.com/microsoft/vscode/pull/194520
```

### **Multiple PR Batch Analysis**
```
https://github.com/openshift/openshift-docs/pull/96102
https://github.com/openshift/openshift-docs/pull/96103
https://github.com/openshift/openshift-docs/pull/96104
```

### **Cross-Repository Analysis**
```
https://github.com/pytorch/pytorch/pull/91234
https://github.com/tensorflow/tensorflow/pull/56789
https://github.com/microsoft/vscode/pull/194520
```

## 🔒 Security

- **Token Security**: GitHub tokens are handled securely and not stored
- **Local Processing**: All analysis runs locally on your machine
- **No Data Upload**: No PR data is sent to external services
- **Privacy**: Full control over your analysis and reports

## 🎨 Customization

The GUI uses modern CSS with:
- **Gradient Themes**: Beautiful color gradients throughout
- **Responsive Design**: Adapts to different screen sizes
- **Custom Components**: Styled buttons, inputs, and cards
- **Interactive Elements**: Hover effects and smooth transitions

## 🚀 Performance

- **Async Processing**: Non-blocking analysis with progress updates
- **Resource Management**: Efficient memory and CPU usage
- **Parallel Analysis**: Multiple PRs processed efficiently
- **Progress Tracking**: Real-time updates during long-running analysis

The GUI provides a professional, user-friendly way to access all the powerful features of the GitHub PR Analyzer! 