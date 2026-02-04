# FloatChat Ultra - Installation Guide

## Prerequisites

Before installing FloatChat, ensure you have the following:

- **Python 3.11+** (We're using Python 3.13.5 ✅)
- **PostgreSQL 15+** with PostGIS extension
- **Ollama** (for local LLM)
- **Git** (for version control)
- **8GB+ RAM** (16GB recommended)
- **50GB+ free disk space** (for ARGO data)

---

## Step 1: Virtual Environment Setup ✅

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
```

**Status**: ✅ Complete

---

## Step 2: Install Python Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt
```

**Status**: 🔄 In Progress

### Key Packages Being Installed:
- **Data Processing**: pandas, numpy, xarray, dask, netCDF4
- **Database**: sqlalchemy, psycopg2-binary, geoalchemy2
- **AI/ML**: langchain, chromadb, sentence-transformers
- **Visualization**: streamlit, plotly, folium
- **Utilities**: loguru, pydantic, python-dotenv

---

## Step 3: Install PostgreSQL with PostGIS

### Windows Installation:

1. **Download PostgreSQL 15+**
   - Visit: https://www.postgresql.org/download/windows/
   - Download the installer (PostgreSQL 15.x or 16.x)
   - Run the installer

2. **Installation Options**:
   - Components: Select all (PostgreSQL Server, pgAdmin 4, Command Line Tools, Stack Builder)
   - Port: 5432 (default)
   - Locale: Default locale
   - **Remember your password!**

3. **Install PostGIS Extension**:
   - Open Stack Builder (from Start Menu)
   - Select your PostgreSQL installation
   - Navigate to: Spatial Extensions → PostGIS
   - Select PostGIS 3.3+ for PostgreSQL 15
   - Install

### Alternative: Using Stack Builder
```
Start Menu → PostgreSQL 15 → Application Stack Builder
→ Spatial Extensions → PostGIS 3.3
```

### Verify Installation:
```bash
# Check PostgreSQL version
psql --version

# Should output: psql (PostgreSQL) 15.x or 16.x
```

---

## Step 4: Create FloatChat Database

```bash
# Open PowerShell or Command Prompt

# Create database (will prompt for password)
createdb -U postgres floatchat

# Or using psql
psql -U postgres
CREATE DATABASE floatchat;
\q
```

### Load Schema:
```bash
# Navigate to project directory
cd "c:\Users\Abhijeet Nardele\OneDrive\Desktop\Edi project"

# Load schema
psql -U postgres -d floatchat -f src/database/schema.sql
```

### Verify Database:
```bash
# Connect to database
psql -U postgres -d floatchat

# List tables
\dt

# Should show: argo_floats, argo_profiles, argo_measurements, etc.

# Check PostGIS
SELECT PostGIS_Version();

# Exit
\q
```

---

## Step 5: Install Ollama (LLM)

### Windows Installation:

1. **Download Ollama**
   - Visit: https://ollama.com/download
   - Download Windows installer
   - Run the installer

2. **Verify Installation**:
```bash
ollama --version
```

3. **Pull Mistral Model**:
```bash
# Pull Mistral 7B (4GB download)
ollama pull mistral:7b-instruct

# This will take 5-10 minutes depending on internet speed
```

4. **Test Ollama**:
```bash
# Test the model
ollama run mistral:7b-instruct "What is oceanography?"

# Should get a response about oceanography
# Press Ctrl+D to exit
```

5. **Start Ollama Server** (if not auto-started):
```bash
ollama serve
```

### Alternative Models:
```bash
# For better quality (requires 24GB RAM)
ollama pull mixtral:8x7b-instruct

# For faster responses (smaller model)
ollama pull mistral:7b
```

---

## Step 6: Configure Environment Variables

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings
```

### Update `.env` file:

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/floatchat
DB_USER=postgres
DB_PASSWORD=YOUR_PASSWORD
DB_NAME=floatchat

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral:7b-instruct

# Paths (keep defaults)
DATA_RAW_DIR=./data/raw
DATA_PROCESSED_DIR=./data/processed
CHROMA_PERSIST_DIRECTORY=./data/chromadb
```

**Important**: Replace `YOUR_PASSWORD` with your PostgreSQL password!

---

## Step 7: Test Database Connection

Create a test script:

```python
# test_connection.py
from src.database.connection import check_db_connection
from src.utils.logger import get_logger

logger = get_logger(__name__)

if check_db_connection():
    logger.info("✅ Database connection successful!")
else:
    logger.error("❌ Database connection failed!")
```

Run test:
```bash
python test_connection.py
```

---

## Step 8: Initialize ChromaDB

ChromaDB will be automatically initialized when you first run the application. No manual setup needed!

---

## Step 9: Verify Installation

Run this verification script:

```python
# verify_setup.py
import sys
from src.utils.logger import get_logger

logger = get_logger(__name__)

def verify_setup():
    checks = []
    
    # Check Python version
    python_version = sys.version_info
    if python_version >= (3, 11):
        logger.info(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        checks.append(True)
    else:
        logger.error(f"❌ Python version too old: {python_version}")
        checks.append(False)
    
    # Check imports
    try:
        import pandas
        logger.info(f"✅ Pandas {pandas.__version__}")
        checks.append(True)
    except ImportError:
        logger.error("❌ Pandas not installed")
        checks.append(False)
    
    try:
        import sqlalchemy
        logger.info(f"✅ SQLAlchemy {sqlalchemy.__version__}")
        checks.append(True)
    except ImportError:
        logger.error("❌ SQLAlchemy not installed")
        checks.append(False)
    
    try:
        import streamlit
        logger.info(f"✅ Streamlit {streamlit.__version__}")
        checks.append(True)
    except ImportError:
        logger.error("❌ Streamlit not installed")
        checks.append(False)
    
    # Check database
    try:
        from src.database.connection import check_db_connection
        if check_db_connection():
            logger.info("✅ Database connection")
            checks.append(True)
        else:
            logger.error("❌ Database connection failed")
            checks.append(False)
    except Exception as e:
        logger.error(f"❌ Database error: {e}")
        checks.append(False)
    
    # Summary
    logger.info(f"\n{'='*50}")
    logger.info(f"Verification: {sum(checks)}/{len(checks)} checks passed")
    logger.info(f"{'='*50}")
    
    return all(checks)

if __name__ == "__main__":
    if verify_setup():
        logger.info("🎉 All checks passed! Ready to build FloatChat!")
    else:
        logger.error("⚠️ Some checks failed. Please fix the issues above.")
```

---

## Troubleshooting

### PostgreSQL Issues

**Problem**: `psql: command not found`
**Solution**: Add PostgreSQL to PATH
```
C:\Program Files\PostgreSQL\15\bin
```

**Problem**: `FATAL: password authentication failed`
**Solution**: Check your password in `.env` file

**Problem**: `PostGIS not found`
**Solution**: Reinstall PostGIS via Stack Builder

### Ollama Issues

**Problem**: `ollama: command not found`
**Solution**: Restart terminal after installation

**Problem**: `connection refused`
**Solution**: Start Ollama server: `ollama serve`

**Problem**: Model download fails
**Solution**: Check internet connection, try again

### Python Package Issues

**Problem**: `pip install` fails
**Solution**: 
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install with verbose output
pip install -v package_name
```

**Problem**: `psycopg2` installation fails
**Solution**: Use `psycopg2-binary` instead (already in requirements.txt)

---

## Next Steps

Once installation is complete:

1. ✅ Verify all components
2. 🔄 Download ARGO data (Phase 3)
3. 🔄 Build RAG pipeline (Phase 4)
4. 🔄 Create Streamlit dashboard (Phase 5)

---

## Quick Reference

### Start Services:
```bash
# PostgreSQL (usually auto-starts)
# Check: services.msc → PostgreSQL

# Ollama
ollama serve

# Streamlit (later)
streamlit run app/Home.py
```

### Useful Commands:
```bash
# Activate venv
.\venv\Scripts\activate

# Check Python packages
pip list

# Database connection
psql -U postgres -d floatchat

# Test Ollama
ollama list
```

---

**Installation Time Estimate**: 30-45 minutes  
**Disk Space Required**: ~10GB (PostgreSQL + Ollama + Python packages)

---

*Last Updated: February 5, 2026*
