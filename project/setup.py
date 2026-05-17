"""
Setup and Installation Script
Automated setup for the steganography project
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """
    Run a shell command and report results
    """
    print(f"\\n→ {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  ✓ Success")
            return True
        else:
            print(f"  ✗ Failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        return False


def main():
    """
    Perform automated setup
    """
    print("\\n" + "="*60)
    print("  ADAPTIVE IMAGE STEGANOGRAPHY - SETUP INSTALLER")
    print("="*60)
    
    # Check Python version
    print(f"\\nPython version: {sys.version}")
    if sys.version_info < (3, 8):
        print("✗ Python 3.8 or higher required!")
        return False
    
    print("✓ Python version OK")
    
    # Create directories
    print("\\n→ Creating project directories...")
    os.makedirs("sample_images", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    print("  ✓ Directories created")
    
    # Install dependencies
    print("\\n→ Installing Python dependencies...")
    if run_command(f"{sys.executable} -m pip install -r requirements.txt", 
                   "Installing packages"):
        print("  ✓ All packages installed")
    else:
        print("  ⚠ Some packages may have failed to install")
    
    # Generate sample images
    print("\\n→ Generating sample images...")
    if run_command(f"{sys.executable} generate_samples.py", 
                   "Creating test images"):
        print("  ✓ Sample images created")
    else:
        print("  ⚠ Sample image generation may have issues")
    
    # Run tests
    print("\\n→ Running tests...")
    if run_command(f"{sys.executable} test_steganography.py", 
                   "Executing test suite"):
        print("  ✓ Tests completed")
    else:
        print("  ⚠ Some tests may have failed")
    
    # Final message
    print("\\n" + "="*60)
    print("  SETUP COMPLETE!")
    print("="*60)
    print("\\nYou can now run the application with:")
    print("  python app.py")
    print("\\nFor more information, see README.md")
    print("="*60 + "\\n")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
