"""
Verification script to check if all components are properly installed
Run this after completing installation to verify setup
"""

import sys
from pathlib import Path

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version >= (3, 11):
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (Need 3.11+)")
        return False

def check_package(package_name, import_name=None):
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        module = __import__(import_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"   ✅ {package_name}: {version}")
        return True
    except ImportError:
        print(f"   ❌ {package_name}: Not installed")
        return False

def check_packages():
    """Check all required packages"""
    print("📦 Checking Python packages...")
    
    packages = [
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('xarray', 'xarray'),
        ('dask', 'dask'),
        ('netCDF4', 'netCDF4'),
        ('h3', 'h3'),
        ('sqlalchemy', 'sqlalchemy'),
        ('psycopg2', 'psycopg2'),
        ('geoalchemy2', 'geoalchemy2'),
        ('langchain', 'langchain'),
        ('chromadb', 'chromadb'),
        ('sentence-transformers', 'sentence_transformers'),
        ('streamlit', 'streamlit'),
        ('plotly', 'plotly'),
        ('folium', 'folium'),
        ('loguru', 'loguru'),
        ('pydantic', 'pydantic'),
        ('fastapi', 'fastapi'),
    ]
    
    results = []
    for pkg_name, import_name in packages:
        results.append(check_package(pkg_name, import_name))
    
    return all(results)

def check_database():
    """Check database connection"""
    print("🗄️  Checking database connection...")
    
    try:
        from src.database.connection import check_db_connection
        if check_db_connection():
            print("   ✅ PostgreSQL connection successful")
            return True
        else:
            print("   ❌ PostgreSQL connection failed")
            print("   ℹ️  Make sure PostgreSQL is running and .env is configured")
            return False
    except Exception as e:
        print(f"   ❌ Database check error: {e}")
        print("   ℹ️  Make sure PostgreSQL is installed and configured")
        return False

def check_ollama():
    """Check if Ollama is available"""
    print("🤖 Checking Ollama LLM...")
    
    try:
        import requests
        from src.utils.config import settings
        
        response = requests.get(f"{settings.ollama_base_url}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            if models:
                print(f"   ✅ Ollama running with {len(models)} model(s)")
                for model in models:
                    print(f"      • {model.get('name', 'unknown')}")
                return True
            else:
                print("   ⚠️  Ollama running but no models installed")
                print("   ℹ️  Run: ollama pull mistral:7b-instruct")
                return False
        else:
            print("   ❌ Ollama not responding")
            return False
    except Exception as e:
        print(f"   ❌ Ollama check failed: {e}")
        print("   ℹ️  Make sure Ollama is installed and running")
        print("   ℹ️  Start with: ollama serve")
        return False

def check_directories():
    """Check if required directories exist"""
    print("📁 Checking project directories...")
    
    required_dirs = [
        'data/raw',
        'data/processed',
        'data/chromadb',
        'data/logs',
        'src/data',
        'src/database',
        'src/ai',
        'src/visualization',
        'src/api',
        'src/utils',
        'app',
        'tests',
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"   ✅ {dir_path}")
        else:
            print(f"   ❌ {dir_path} (missing)")
            all_exist = False
    
    return all_exist

def check_config():
    """Check configuration"""
    print("⚙️  Checking configuration...")
    
    env_file = Path('.env')
    if env_file.exists():
        print("   ✅ .env file exists")
        
        # Try to load config
        try:
            from src.utils.config import settings
            print(f"   ✅ Configuration loaded")
            print(f"      • Database: {settings.db_name}")
            print(f"      • Ollama Model: {settings.ollama_model}")
            return True
        except Exception as e:
            print(f"   ❌ Configuration error: {e}")
            return False
    else:
        print("   ❌ .env file not found")
        print("   ℹ️  Copy .env.example to .env and configure")
        return False

def main():
    """Run all verification checks"""
    print_header("FloatChat Ultra - Installation Verification")
    
    checks = {
        'Python Version': check_python_version(),
        'Python Packages': check_packages(),
        'Project Directories': check_directories(),
        'Configuration': check_config(),
        'Database': check_database(),
        'Ollama LLM': check_ollama(),
    }
    
    # Summary
    print_header("Verification Summary")
    
    passed = sum(checks.values())
    total = len(checks)
    
    for check_name, result in checks.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:12} {check_name}")
    
    print(f"\n{'='*60}")
    print(f"  Result: {passed}/{total} checks passed")
    print(f"{'='*60}\n")
    
    if passed == total:
        print("🎉 All checks passed! FloatChat is ready to use!")
        print("\nNext steps:")
        print("  1. Download ARGO data (Phase 3)")
        print("  2. Build RAG pipeline (Phase 4)")
        print("  3. Create dashboard (Phase 5)")
        return 0
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  • Missing packages: pip install -r requirements.txt")
        print("  • Database: Install PostgreSQL and run schema.sql")
        print("  • Ollama: Install from https://ollama.com")
        print("  • Config: Copy .env.example to .env")
        return 1

if __name__ == "__main__":
    sys.exit(main())
