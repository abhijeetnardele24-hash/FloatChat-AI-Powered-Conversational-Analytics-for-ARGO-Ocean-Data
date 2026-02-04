# PostgreSQL Setup Commands

## After PostGIS Installation Completes

### Step 1: Create FloatChat Database

```bash
# Open PowerShell and run:
createdb -U postgres -p 5433 floatchat

# You'll be prompted for password: 1234
```

### Step 2: Load Database Schema

```bash
# Navigate to project directory
cd "c:\Users\Abhijeet Nardele\OneDrive\Desktop\Edi project"

# Load the schema (creates all tables, indexes, PostGIS setup)
psql -U postgres -p 5433 -d floatchat -f src/database/schema.sql

# Password: 1234
```

### Step 3: Verify Database Setup

```bash
# Connect to database
psql -U postgres -p 5433 -d floatchat

# Inside psql, run these commands:

# List all tables
\dt

# You should see:
# - argo_floats
# - argo_profiles
# - argo_measurements
# - argo_ocean_properties
# - argo_summaries
# - ocean_regions
# - schema_version

# Check PostGIS version
SELECT PostGIS_Version();

# Should show PostGIS version (e.g., "3.4" or "3.5")

# Exit psql
\q
```

### Step 4: Test Connection from Python

```bash
# Activate virtual environment
.\venv\Scripts\activate

# Run verification script
python verify_setup.py
```

You should see:
```
✅ PASS Database
✅ PASS PostgreSQL connection
```

---

## Troubleshooting

### Issue: "createdb: command not found"

**Solution**: Add PostgreSQL to PATH

1. Open Environment Variables
2. Add to PATH: `C:\Program Files\PostgreSQL\18\bin`
3. Restart PowerShell

### Issue: "password authentication failed"

**Solution**: Use the correct password (1234)

### Issue: "database already exists"

**Solution**: Database already created, skip to Step 2

---

## Quick Reference

```bash
# Connect to database
psql -U postgres -p 5433 -d floatchat

# List databases
psql -U postgres -p 5433 -l

# Drop database (if needed to start fresh)
dropdb -U postgres -p 5433 floatchat

# Backup database
pg_dump -U postgres -p 5433 floatchat > backup.sql

# Restore database
psql -U postgres -p 5433 floatchat < backup.sql
```

---

*Ready to run after PostGIS installation completes!*
