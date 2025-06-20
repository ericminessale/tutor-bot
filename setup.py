#!/usr/bin/env python3
"""
Setup script for SignalWire AI Tutor Bot Demo
Handles dependency installation and environment configuration
"""

import os
import sys
import subprocess
import platform


def run_command(cmd):
    """Run a command and return success status"""
    print(f"Running: {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def main():
    print("🎓 SignalWire AI Tutor Bot Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Create virtual environment if it doesn't exist
    if not os.path.exists("venv"):
        print("\n📦 Creating virtual environment...")
        if not run_command(f"{sys.executable} -m venv venv"):
            print("❌ Failed to create virtual environment")
            sys.exit(1)
    
    # Determine activation command based on OS
    if platform.system() == "Windows":
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
        python_cmd = "venv\\Scripts\\python"
    else:
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
        python_cmd = "venv/bin/python"
    
    print(f"\n💡 To activate virtual environment: {activate_cmd}")
    
    # Upgrade pip
    print("\n📦 Upgrading pip...")
    run_command(f"{pip_cmd} install --upgrade pip")
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    if not run_command(f"{pip_cmd} install -r requirements.txt"):
        print("❌ Failed to install dependencies")
        print("💡 Try running: pip install -r requirements.txt")
        sys.exit(1)
    
    print("\n✅ Dependencies installed successfully!")
    
    # Check if .env file exists
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            print("\n🔐 Creating .env file from template...")
            with open(".env.example", "r") as src, open(".env", "w") as dst:
                dst.write(src.read())
            print("✅ Created .env file from .env.example")
            print("💡 Edit .env file to customize configuration")
        else:
            print("\n🔐 .env file found - configuration ready")
    else:
        print("\n✅ .env file already exists")
    
    print("\n🎉 Setup Complete!")
    print("\n📖 Next steps:")
    print(f"1. Activate virtual environment: {activate_cmd}")
    print("2. Edit .env file if needed (optional)")
    print("3. Run the demo: python tutor_bot_demo.py")
    print("\n💡 The service will run on http://localhost:3000/tutor")
    print("\n🎓 Available Tutors:")
    print("   • Math - Professor Marcus (systematic problem-solving)")
    print("   • Spanish - Señora Lopez (immersion-based learning)")
    print("   • French - Madame Dubois (elegance and precision)")
    print("   • Japanese - Tanaka-sensei (cultural understanding)")
    print("   • Science - Dr. Stevens (inquiry-based learning)")
    print("   • History - Professor Thompson (narrative analysis)")
    print("\n✨ Features Demonstrated:")
    print("   • Context-level prompts with unique teaching philosophies")
    print("   • Context isolation for maintaining pedagogical integrity")
    print("   • Multi-language support for language tutoring")
    print("   • Structured learning workflows with clear progression")
    print("\n📚 Future Enhancements:")
    print("   • Add web_search skill for smarter tutoring")
    print("   • Add math skill for calculations")
    print("   • Add datetime skill for scheduling")
    print("   • See requirements.txt for optional dependencies")


if __name__ == "__main__":
    main() 