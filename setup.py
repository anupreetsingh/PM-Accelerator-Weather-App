# Just run this file to setup environment and install dependencies for the project

import subprocess
import sys
import os

def run_command(command, description):
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🌤️  Weather App Setup")
    print("=" * 30)
    
    # Checks if Python is installed
    if not run_command("python --version", "Checking Python installation"):
        print("❌ Python is not installed or not in PATH")
        return
    
    # Creates virtual environment
    if not os.path.exists(".venv"):
        if not run_command("python -m venv .venv", "Creating virtual environment"):
            return
    else:
        print("✅ Virtual environment already exists")
    
    # Activates virtual environment and install dependencies
    if sys.platform == "win32":
        activate_cmd = ".venv\\Scripts\\activate"
        pip_cmd = ".venv\\Scripts\\pip"
    else:
        activate_cmd = "source .venv/bin/activate"
        pip_cmd = ".venv/bin/pip"
    
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies"):
        return
    
    print("\n🎉 Setup completed successfully!")
    print("\nTo run the app:")
    print("1. Activate the virtual environment:")
    if sys.platform == "win32":
        print("   .venv\\Scripts\\activate")
    else:
        print("   source .venv/bin/activate")
    print("2. Start the backend server:")
    print("   cd backend && python main.py")
    print("3. Open frontend/index.html in your browser")

if __name__ == "__main__":
    main()
