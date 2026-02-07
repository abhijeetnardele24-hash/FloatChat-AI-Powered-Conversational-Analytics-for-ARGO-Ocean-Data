"""
FloatChat Ultra Dashboard Launcher
Launch the premium glassmorphism dashboard
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Launch FloatChat Ultra Dashboard"""
    
    print("="*70)
    print("🌊 FloatChat Ultra - Premium Dashboard")
    print("="*70)
    print()
    print("✨ Features:")
    print("  • Glassmorphism design with animations")
    print("  • Multiple specialized tabs")
    print("  • AI chatbot integration")
    print("  • Interactive visualizations")
    print("  • Real-time analytics")
    print()
    print("🚀 Starting dashboard...")
    print("📍 URL: http://localhost:8501")
    print()
    print("="*70)
    print()
    
    # Get app path
    app_path = Path(__file__).parent / "app" / "dashboard.py"
    
    # Launch Streamlit
    subprocess.run([
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(app_path),
        "--server.port=8501",
        "--server.address=localhost",
        "--theme.base=dark"
    ])


if __name__ == "__main__":
    main()
