# PostgreSQL Installation Guide for Windows

## Quick Install Steps

### 1. Download PostgreSQL

Visit: **https://www.postgresql.org/download/windows/**

- Download **PostgreSQL 16.x** (or 15.x) installer
- File size: ~250 MB
- Choose Windows x86-64

### 2. Run Installer

1. **Launch** the downloaded `.exe` file
2. **Installation Directory**: Keep default (`C:\Program Files\PostgreSQL\16`)
3. **Select Components**: Check ALL:
   - ✅ PostgreSQL Server
   - ✅ pgAdmin 4
   - ✅ Stack Builder
   - ✅ Command Line Tools

4. **Data Directory**: Keep default (`C:\Program Files\PostgreSQL\16\data`)
5. **Password**: Set a strong password (REMEMBER THIS!)
   - Example: `floatchat2026` (or your choice)
   - **Write it down!**

6. **Port**: Keep default `5432`
7. **Locale**: Default locale
8. **Click Next** and wait for installation (~5 minutes)

### 3. Install PostGIS Extension

**After PostgreSQL installation completes:**

1. **Stack Builder** should auto-launch (if not, find it in Start Menu)
2. Select your PostgreSQL installation from dropdown
3. Click **Next**
4. Expand **Spatial Extensions**
5. Check **PostGIS 3.4** (or latest version)
6. Click **Next** → **Next** → **Install**
7. Accept defaults and complete installation

### 4. Verify Installation

Open **Command Prompt** or **PowerShell**:

```bash
# Check PostgreSQL version
psql --version
# Should show: psql (PostgreSQL) 16.x

# If command not found, add to PATH:
# C:\Program Files\PostgreSQL\16\bin
```

### 5. Create FloatChat Database

```bash
# Method 1: Using createdb command
createdb -U postgres floatchat

# Method 2: Using psql
psql -U postgres
# Enter password when prompted
# Then run:
CREATE DATABASE floatchat;
\q
```

### 6. Load Database Schema

```bash
# Navigate to project directory
cd "c:\Users\Abhijeet Nardele\OneDrive\Desktop\Edi project"

# Load schema
psql -U postgres -d floatchat -f src/database/schema.sql
```

### 7. Verify Database Setup

```bash
# Connect to database
psql -U postgres -d floatchat

# List tables
\dt

# You should see:
# - argo_floats
# - argo_profiles
# - argo_measurements
# - argo_ocean_properties
# - argo_summaries
# - ocean_regions
# - schema_version

# Check PostGIS
SELECT PostGIS_Version();

# Should show PostGIS version

# Exit
\q
```

## Troubleshooting

### Issue: "psql: command not found"

**Solution**: Add PostgreSQL to PATH

1. Open **Environment Variables**:
   - Right-click **This PC** → **Properties**
   - **Advanced system settings** → **Environment Variables**

2. Under **System Variables**, find **Path**, click **Edit**

3. Click **New** and add:
   ```
   C:\Program Files\PostgreSQL\16\bin
   ```

4. Click **OK** on all windows

5. **Restart** Command Prompt/PowerShell

### Issue: "password authentication failed"

**Solution**: Use the password you set during installation

### Issue: "PostGIS not found"

**Solution**: 
1. Reinstall PostGIS via Stack Builder
2. Or manually: `CREATE EXTENSION postgis;` in psql

## Quick Reference

```bash
# Start PostgreSQL service
net start postgresql-x64-16

# Stop PostgreSQL service
net stop postgresql-x64-16

# Connect to database
psql -U postgres -d floatchat

# List databases
psql -U postgres -l

# Backup database
pg_dump -U postgres floatchat > backup.sql

# Restore database
psql -U postgres floatchat < backup.sql
```

## Next Step

After PostgreSQL is installed, update your `.env` file:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/floatchat
DB_USER=postgres
DB_PASSWORD=YOUR_PASSWORD
DB_NAME=floatchat
```

Replace `YOUR_PASSWORD` with the password you set!

---

**Installation Time**: ~15 minutes  
**Disk Space**: ~1 GB
