#!/usr/bin/env python3
"""
Setup script for the AI Travel Agent with worldwide location support.
This script helps users get started quickly with proper configuration.
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Print a welcome banner."""
    print("=" * 70)
    print("🌍 AI TRAVEL AGENT - WORLDWIDE SETUP 🌍")
    print("=" * 70)
    print("Setting up your global travel planning assistant...")
    print()

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 11):
        print("❌ Error: Python 3.11 or higher is required.")
        print(f"   Current version: {sys.version}")
        print("   Please upgrade Python and try again.")
        sys.exit(1)
    else:
        print(f"✅ Python version: {sys.version.split()[0]}")

def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")
    
    try:
        # Install requirements from current directory
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        
        print("✅ Dependencies installed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        print("   Please run manually: pip install -r requirements.txt")
    except FileNotFoundError:
        print("❌ Error: requirements.txt not found.")
        print("   Please run this script from the project root directory.")
        sys.exit(1)

def create_env_file():
    """Create .env file if it doesn't exist."""
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    if env_path.exists():
        print("✅ .env file already exists")
        return
    
    print("\n🔑 Creating .env configuration file...")
    
    # Read the example file
    if env_example_path.exists():
        with open(env_example_path, 'r') as f:
            example_content = f.read()
    else:
        # Create a basic template
        example_content = """# LLM Configuration (Required)
PROVIDER=OpenRouter
BASE_URL=https://openrouter.ai/api/v1
LLM_API_KEY=your_api_key_here
MODEL_CHOICE=qwen/qwen3-14b:free

# Travel APIs (Optional - enables real worldwide data)
WEATHER_API_KEY=your_openweathermap_key
FLIGHT_API_KEY=your_aviationstack_key
HOTEL_API_KEY=your_rapidapi_key
"""
    
    # Write to .env file
    with open(env_path, 'w') as f:
        f.write(example_content)
    
    print("✅ .env file created from template")
    print("📝 Please edit .env with your actual API keys")

def test_setup():
    """Test if the setup is working."""
    print("\n🧪 Testing setup...")
    
    try:
        # Test API integration
        result = subprocess.run([sys.executable, "test_apis.py"], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ API integration test completed")
            print("   Check the output above for API status")
        else:
            print("⚠️  API test completed with warnings")
            print("   This is normal if you haven't configured API keys yet")
            
    except subprocess.TimeoutExpired:
        print("⚠️  API test timed out (this is normal)")
    except FileNotFoundError:
        print("⚠️  Could not run API test (test_apis.py not found)")

def print_next_steps():
    """Print instructions for next steps."""
    print("\n" + "=" * 70)
    print("🎉 SETUP COMPLETE! 🎉")
    print("=" * 70)
    print()
    print("📋 NEXT STEPS:")
    print()
    print("1. 🔑 Configure API Keys (Optional but recommended):")
    print("   Edit: .env")
    print("   Add your API keys for real worldwide data")
    print()
    print("2. 🚀 Start the Travel Agent:")
    print("   streamlit run streamlit_ui.py")
    print()
    print("3. 🧪 Test API Integration:")
    print("   python test_apis.py")
    print()
    print("4. 🌍 Start Planning:")
    print("   Open http://localhost:8501 in your browser")
    print("   Try: 'I want to go to Tokyo from New York'")
    print()
    print("💡 The system works without API keys using smart mock data!")
    print("💡 With API keys, you get real flight/hotel/weather data worldwide!")
    print()
    print("🌟 Happy travels! ✈️🌍")

def main():
    """Main setup function."""
    print_banner()
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Create .env file
    create_env_file()
    
    # Test setup
    test_setup()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()
