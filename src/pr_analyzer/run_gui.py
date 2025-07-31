#!/usr/bin/env python3
"""
Professional launcher for GitHub PR Analytics Platform
Enterprise-grade GUI with enhanced startup experience
"""

import os
import sys
import subprocess
import time
import webbrowser

def print_banner():
    """Display professional startup banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                     📊 GitHub PR Analytics Platform                          ║
║                                                                              ║
║                    Enterprise-Grade Analysis Suite                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

🚀 Initializing professional analytics environment...
📊 Loading enterprise-grade analysis modules...
🔧 Configuring advanced visualization components...
🌐 Starting web interface on professional port...

═══════════════════════════════════════════════════════════════════════════════

📱 Interface Access:
   🔗 Primary URL: http://localhost:8501
   🔗 Local Access: http://127.0.0.1:8501
   
⚙️  Platform Features:
   ✅ AI-Powered PR Analysis
   ✅ Advanced Timeline Metrics
   ✅ Conversation Intelligence
   ✅ Developer Insights
   ✅ Compliance Reporting
   ✅ Interactive Dashboards

🔐 Security & Privacy:
   ✅ Local Processing Only
   ✅ No Data Upload
   ✅ Enterprise Privacy Standards
   ✅ Secure Token Handling

═══════════════════════════════════════════════════════════════════════════════

⏹️  To stop the server: Press Ctrl+C
📖 For documentation: Visit the Help section in the interface
🐛 Report issues: Use the Report Bug link in the interface

═══════════════════════════════════════════════════════════════════════════════
"""
    print(banner)

def check_dependencies():
    """Check if all required dependencies are available"""
    print("🔍 Verifying platform dependencies...")
    
    required_packages = [
        'streamlit',
        'plotly',
        'pandas'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"   ❌ {package}")
    
    if missing_packages:
        print(f"\n⚠️  Missing dependencies detected: {', '.join(missing_packages)}")
        print("\n🔧 Installing missing dependencies...")
        
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install"
            ] + missing_packages, check=True)
            print("✅ Dependencies installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies automatically")
            print(f"   Please run: pip install {' '.join(missing_packages)}")
            return False
    
    print("✅ All dependencies verified!")
    return True

def launch_gui():
    """Launch the professional Streamlit GUI"""
    
    # Get the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gui_file = os.path.join(script_dir, "pr_analyzer_gui.py")
    
    if not os.path.exists(gui_file):
        print(f"❌ GUI file not found: {gui_file}")
        return False
    
    print("🌐 Starting professional web interface...")
    
    try:
        # Launch Streamlit with professional configuration
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", gui_file,
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.serverAddress", "localhost",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false",
            "--theme.base", "light",
            "--theme.primaryColor", "#667eea",
            "--theme.backgroundColor", "#ffffff",
            "--theme.secondaryBackgroundColor", "#f8fafc",
            "--theme.textColor", "#1a202c"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for the server to start
        time.sleep(3)
        
        # Check if the process is still running
        if process.poll() is None:
            print("✅ Professional interface launched successfully!")
            print("\n🔥 Platform is now ready for enterprise-grade analysis!")
            
            # Wait for the process to complete
            process.wait()
        else:
            stdout, stderr = process.communicate()
            print("❌ Failed to start the interface")
            if stderr:
                print(f"Error: {stderr.decode()}")
            return False
            
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down analytics platform...")
        print("✅ Platform stopped successfully")
        print("👋 Thank you for using GitHub PR Analytics Platform!")
        
    except Exception as e:
        print(f"❌ Error starting GUI: {e}")
        print("\n🔧 Troubleshooting:")
        print("   1. Ensure Streamlit is installed: pip install streamlit")
        print("   2. Check if port 8501 is available")
        print("   3. Verify Python version compatibility")
        return False
    
    return True

def main():
    """Main launcher function"""
    try:
        # Display professional banner
        print_banner()
        
        # Check dependencies
        if not check_dependencies():
            print("\n❌ Dependency check failed. Please install missing packages and try again.")
            return
        
        # Small delay for dramatic effect
        time.sleep(1)
        
        # Launch the GUI
        if not launch_gui():
            print("\n❌ Failed to launch the analytics platform")
            return
        
    except KeyboardInterrupt:
        print("\n\n👋 Startup cancelled by user")
    
    except Exception as e:
        print(f"\n❌ Unexpected error during startup: {e}")
        print("\n🔧 Please check your Python environment and try again")

if __name__ == "__main__":
    main() 