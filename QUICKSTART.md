# FloatChat Ultra - Quick Start Guide

## 🚀 Get Started in 5 Steps

### Step 1: Install PostgreSQL ✅ (15 minutes)

Follow the guide: [INSTALL_POSTGRESQL.md](docs/INSTALL_POSTGRESQL.md)

**Quick version**:
1. Download from https://www.postgresql.org/download/windows/
2. Install with PostGIS extension
3. Create database: `createdb -U postgres floatchat`
4. Load schema: `psql -U postgres -d floatchat -f src/database/schema.sql`

### Step 2: Install Ollama ✅ (20 minutes)

Follow the guide: [INSTALL_OLLAMA.md](docs/INSTALL_OLLAMA.md)

**Quick version**:
1. Download from https://ollama.com/download
2. Install Ollama
3. Pull model: `ollama pull mistral:7b-instruct`
4. Verify: `ollama list`

### Step 3: Configure Environment ✅ (2 minutes)

Edit the `.env` file (already created from .env.example):

```env
# Update these lines with your PostgreSQL password
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/floatchat
DB_PASSWORD=YOUR_PASSWORD
```

Replace `YOUR_PASSWORD` with your PostgreSQL password!

### Step 4: Verify Setup ✅ (1 minute)

```bash
# Activate virtual environment
.\venv\Scripts\activate

# Run verification script
python verify_setup.py
```

You should see:
```
✅ PASS Python Version
✅ PASS Python Packages
✅ PASS Project Directories
✅ PASS Configuration
✅ PASS Database
✅ PASS Ollama LLM

Result: 6/6 checks passed
🎉 All checks passed! FloatChat is ready to use!
```

### Step 5: Run FloatChat 🎉 (Coming Soon)

```bash
# Start the dashboard (Phase 5)
streamlit run app/Home.py
```

---

## Current Status

### ✅ Completed
- [x] Project structure
- [x] Python dependencies (160 packages)
- [x] Database schema
- [x] Configuration files
- [x] Installation guides

### 🔄 Next Steps
- [ ] Install PostgreSQL
- [ ] Install Ollama
- [ ] Download ARGO data
- [ ] Build RAG pipeline
- [ ] Create dashboard

---

## Troubleshooting

### Issue: Python packages not installed

```bash
# Activate venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Issue: Database connection fails

1. Check PostgreSQL is running: `services.msc` → PostgreSQL
2. Verify password in `.env` file
3. Test connection: `psql -U postgres -d floatchat`

### Issue: Ollama not responding

```bash
# Start Ollama server
ollama serve

# In another terminal, test:
ollama list
```

---

## File Structure

```
floatchat/
├── .env                      # Your configuration (UPDATE THIS!)
├── verify_setup.py           # Verification script
├── requirements.txt          # Python dependencies
│
├── docs/                     # Documentation
│   ├── INSTALLATION.md       # Full installation guide
│   ├── INSTALL_POSTGRESQL.md # PostgreSQL guide
│   └── INSTALL_OLLAMA.md     # Ollama guide
│
├── src/                      # Source code
│   ├── database/             # Database layer
│   │   ├── schema.sql        # Database schema
│   │   ├── models.py         # ORM models
│   │   └── connection.py     # DB connection
│   ├── utils/                # Utilities
│   │   ├── config.py         # Configuration
│   │   ├── logger.py         # Logging
│   │   └── helpers.py        # Helper functions
│   └── ...
│
└── data/                     # Data storage
    ├── raw/                  # NetCDF files (coming soon)
    ├── processed/            # Processed data
    ├── chromadb/             # Vector database
    └── logs/                 # Application logs
```

---

## Need Help?

1. **Check Installation Guides**:
   - [Full Installation Guide](docs/INSTALLATION.md)
   - [PostgreSQL Guide](docs/INSTALL_POSTGRESQL.md)
   - [Ollama Guide](docs/INSTALL_OLLAMA.md)

2. **Run Verification**:
   ```bash
   python verify_setup.py
   ```

3. **Check Logs**:
   ```bash
   # View latest logs
   cat data/logs/floatchat.log
   ```

---

## What's Next?

Once PostgreSQL and Ollama are installed:

1. **Phase 3**: Download ARGO ocean data
2. **Phase 4**: Build RAG pipeline for AI queries
3. **Phase 5**: Create Streamlit dashboard
4. **Phase 6**: Add visualizations and maps
5. **Phase 7**: Deploy to production

---

**Estimated Time to Full Setup**: 45 minutes  
**Ready to Start**: Follow Step 1 above! 🚀

---

*Last Updated: February 5, 2026*
