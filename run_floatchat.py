"""
FloatChat Ultra - Main Launcher
Quick start script to launch the Streamlit chat interface
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Launch FloatChat Streamlit app"""
    
    print("="*70)
    print("🌊 FloatChat Ultra - AI-Powered ARGO Ocean Data Explorer")
    print("="*70)
    print()
    print("Starting Streamlit chat interface...")
    print()
    print("📝 Note: Make sure Ollama is running!")
    print("   Start Ollama: ollama serve")
    print()
    print("="*70)
    print()
    
    # Get app path
    app_path = Path(__file__).parent / "app" / "chat_interface.py"
    
    # Launch Streamlit
    subprocess.run([
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(app_path),
        "--server.port=8501",
        "--server.address=localhost"
    ])


if __name__ == "__main__":
    main()
