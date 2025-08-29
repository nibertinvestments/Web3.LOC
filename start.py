#!/usr/bin/env python3
"""
Web3.LOC Startup Script - Launch the complete contract discovery platform
This script provides an easy way to start the Web3.LOC system with all components.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def check_env_file():
    """Check if .env file exists and has required keys."""
    env_path = Path('.env')
    if not env_path.exists():
        print("❌ Error: .env file not found")
        print("Please create a .env file with your API keys:")
        print("")
        print("ETHERSCAN_API_KEY=your_etherscan_api_key_here")
        print("BASESCAN_API_KEY=your_basescan_api_key_here")
        print("SUPPORTED_CHAINS=ethereum,base")
        print("RATE_LIMIT=4")
        print("")
        return False
    
    # Check for required keys
    required_keys = ['ETHERSCAN_API_KEY', 'BASESCAN_API_KEY']
    env_content = env_path.read_text()
    
    missing_keys = []
    for key in required_keys:
        if key not in env_content or f"{key}=" not in env_content:
            missing_keys.append(key)
    
    if missing_keys:
        print(f"❌ Error: Missing required environment variables: {', '.join(missing_keys)}")
        return False
    
    print("✅ Environment configuration found")
    return True

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True, text=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print("Error output:", e.stderr)
        return False

def create_directories():
    """Create necessary directories."""
    directories = ['./exports', './contract_readmes', './logs']
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    print("✅ Directories created")

def launch_web_interface():
    """Launch the Streamlit web interface."""
    print("🚀 Launching Web3.LOC web interface...")
    print("🌐 The interface will open in your default browser")
    print("📊 Navigate to different pages using the sidebar")
    print("🔍 Start with the Discovery page to scan for contracts")
    print("")
    
    try:
        # Launch Streamlit
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'web3_loc_gui.py', 
                       '--server.headless', 'false'])
    except KeyboardInterrupt:
        print("\n👋 Web3.LOC shutdown gracefully")
    except Exception as e:
        print(f"❌ Failed to launch web interface: {e}")
        print("\n🔧 Trying alternative launch method...")
        try:
            subprocess.run(['streamlit', 'run', 'web3_loc_gui.py'])
        except Exception as e2:
            print(f"❌ Alternative launch failed: {e2}")
            print("\n📋 Manual launch instructions:")
            print("1. Open terminal in project directory")
            print("2. Run: streamlit run web3_loc_gui.py")

def launch_cli():
    """Launch the CLI interface."""
    print("🖥️  Launching Web3.LOC CLI interface...")
    try:
        subprocess.run([sys.executable, 'main.py'])
    except KeyboardInterrupt:
        print("\n👋 Web3.LOC CLI shutdown gracefully")
    except Exception as e:
        print(f"❌ Failed to launch CLI: {e}")

def main():
    """Main startup function."""
    print("🔍 Web3.LOC - Smart Contract Discovery Platform")
    print("=" * 50)
    
    # Pre-flight checks
    check_python_version()
    
    if not check_env_file():
        sys.exit(1)
    
    # Install dependencies if needed
    try:
        import streamlit
        import plotly
        import aiohttp
        print("✅ Core dependencies available")
    except ImportError:
        if not install_dependencies():
            sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Choose interface
    print("\n🎯 Choose your interface:")
    print("1. 🌐 Web Interface (Recommended)")
    print("2. 🖥️  Command Line Interface")
    print("3. 🔧 Install dependencies only")
    
    try:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1" or choice == "":
            launch_web_interface()
        elif choice == "2":
            launch_cli()
        elif choice == "3":
            print("✅ Dependencies installed. You can now run:")
            print("   Web Interface: streamlit run web3_loc_gui.py")
            print("   CLI Interface: python main.py")
        else:
            print("❌ Invalid choice")
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()
