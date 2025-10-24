#!/usr/bin/env python3
"""
Code formatting script for PixelMorph project.
Ensures consistent code style across all Python files.
"""
import os
import subprocess
import sys
from pathlib import Path


def run_command(command: list, description: str) -> bool:
    """Run a command and return success status."""
    print(f"Running {description}...")
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed:")
        print(f"  Error: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"✗ {description} failed: Command not found")
        return False


def get_python_files() -> list:
    """Get all Python files in the project."""
    python_files = []
    for file_path in Path(".").rglob("*.py"):
        if "venv" not in str(file_path) and "__pycache__" not in str(file_path):
            python_files.append(str(file_path))
    return python_files


def check_code_style() -> bool:
    """Check code style with flake8."""
    python_files = get_python_files()
    if not python_files:
        print("No Python files found")
        return True
    
    # Check if flake8 is available
    try:
        subprocess.run(["flake8", "--version"], capture_output=True, check=True)
        return run_command(["flake8"] + python_files, "flake8 style check")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("flake8 not available, skipping style check")
        return True


def format_imports() -> bool:
    """Format imports with isort."""
    python_files = get_python_files()
    if not python_files:
        return True
    
    try:
        subprocess.run(["isort", "--version"], capture_output=True, check=True)
        return run_command(["isort", "--check-only", "--diff"] + python_files, 
                          "import sorting check")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("isort not available, skipping import formatting")
        return True


def format_code() -> bool:
    """Format code with black."""
    python_files = get_python_files()
    if not python_files:
        return True
    
    try:
        subprocess.run(["black", "--version"], capture_output=True, check=True)
        return run_command(["black", "--check", "--diff"] + python_files, 
                          "code formatting check")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("black not available, skipping code formatting")
        return True


def main():
    """Main function to run all code style checks."""
    print("PixelMorph Code Style Checker")
    print("=" * 40)
    
    success = True
    
    # Check code style
    if not check_code_style():
        success = False
    
    # Check import formatting
    if not format_imports():
        success = False
    
    # Check code formatting
    if not format_code():
        success = False
    
    print("\n" + "=" * 40)
    if success:
        print("✓ All code style checks passed!")
        return 0
    else:
        print("✗ Some code style checks failed")
        print("Run the following commands to fix issues:")
        print("  isort .")
        print("  black .")
        return 1


if __name__ == "__main__":
    sys.exit(main())