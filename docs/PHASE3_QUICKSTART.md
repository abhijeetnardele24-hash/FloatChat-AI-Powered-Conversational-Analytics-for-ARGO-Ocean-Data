# Phase 3: ARGO Data Acquisition - Quick Start Guide

## 🎯 Objective
Download real ARGO ocean data from the Indian Ocean (2020-2024) and load it into our PostgreSQL database.

## 📋 Prerequisites

✅ Phase 2 Complete:
- PostgreSQL 18 + PostGIS installed
- FloatChat database created
- Python environment with all packages

## 🚀 Quick Start (3 Commands)

### Option 1: Run Complete Pipeline (Recommended)

```bash
# Activate virtual environment
.\venv\Scripts\activate

# Run complete pipeline (downloads 100 files for testing)
python src/data/run_pipeline.py --limit 100

# This will:
# 1. Download ARGO index (~50 MB)
# 2. Filter for Indian Ocean 2020-2024
# 3. Download 100 NetCDF files (~200 MB)
# 4. Parse NetCDF files
# 5. Load into PostgreSQL database
```

**Time**: ~15-20 minutes  
**Data**: ~200 MB  
**Result**: ~100 profiles with ~10,000 measurements

### Option 2: Run Full Dataset

```bash
# Download ALL Indian Ocean data (2020-2024)
python src/data/run_pipeline.py --limit 0

# Warning: This will download 2-5 GB of data
# Time: 1-2 hours depending on internet speed
```

## 📝 Step-by-Step (Manual)

If you want to run each step separately:

### Step 1: Download ARGO Index
```bash
python src/data/download_index.py
```

**What it does**:
- Downloads global ARGO index file (~50 MB)
- Filters for Indian Ocean region (20°E-120°E, 40°S-30°N)
- Filters for 2020-2024 time period
- Saves filtered index to `data/raw/index/indian_ocean_2020_2024.csv`

**Output**: List of ~50,000-100,000 profiles in Indian Ocean

### Step 2: Download NetCDF Files
```bash
python src/data/download_netcdf.py
```

**What it does**:
- Reads filtered index
- Downloads NetCDF files in parallel (5 concurrent downloads)
- Saves to `data/raw/netcdf/`
- Default: 100 files for testing

**Output**: NetCDF files (~2 MB each)

### Step 3: Parse NetCDF Files
```bash
python src/data/parse_netcdf.py
```

**What it does**:
- Reads all downloaded NetCDF files
- Extracts float metadata
- Extracts profile data (lat, lon, date)
- Extracts measurements (pressure, temperature, salinity)
- Saves to parquet files in `data/processed/`

**Output**: 
- `floats.parquet` - Float metadata
- `profiles.parquet` - Profile data
- `measurements.parquet` - Measurement data

### Step 4: Load into Database
```bash
python src/data/load_database.py
```

**What it does**:
- Loads floats into `argo_floats` table
- Loads profiles into `argo_profiles` table (with PostGIS geometry)
- Loads measurements into `argo_measurements` table
- Updates database statistics

**Output**: Data in PostgreSQL database

## 📊 Expected Results (100 files)

```
Floats: ~20-30 unique floats
Profiles: ~100 profiles
Measurements: ~10,000-15,000 measurements
Database Size: ~5-10 MB
```

## 📊 Expected Results (Full Dataset)

```
Floats: ~200-300 unique floats
Profiles: ~50,000-100,000 profiles
Measurements: ~5-10 million measurements
Database Size: ~500 MB - 1 GB
```

## ✅ Verification

After running the pipeline, verify the data:

```bash
# Activate environment
.\venv\Scripts\activate

# Connect to database
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -p 5433 -d floatchat

# Check data
SELECT COUNT(*) FROM argo_floats;
SELECT COUNT(*) FROM argo_profiles;
SELECT COUNT(*) FROM argo_measurements;

# Check date range
SELECT MIN(date), MAX(date) FROM argo_profiles;

# Check geographic coverage
SELECT MIN(latitude), MAX(latitude), MIN(longitude), MAX(longitude) 
FROM argo_profiles;

# Exit
\q
```

## 🔧 Troubleshooting

### Issue: "Module not found"
**Solution**: Make sure virtual environment is activated
```bash
.\venv\Scripts\activate
```

### Issue: "Database connection failed"
**Solution**: Make sure PostgreSQL is running and password is correct in `.env`

### Issue: "Download failed"
**Solution**: Check internet connection, retry will happen automatically

### Issue: "Parsing failed"
**Solution**: Check logs in `data/logs/` for details

## 📁 Data Directory Structure

After running the pipeline:

```
data/
├── raw/
│   ├── index/
│   │   ├── ar_index_global_prof.txt      # Global index (~50 MB)
│   │   └── indian_ocean_2020_2024.csv    # Filtered index
│   └── netcdf/
│       ├── aoml/
│       │   └── 2901234/
│       │       └── profiles/
│       │           ├── D2901234_001.nc
│       │           └── D2901234_002.nc
│       └── ...
├── processed/
│   ├── floats.parquet                     # Float metadata
│   ├── profiles.parquet                   # Profile data
│   └── measurements.parquet               # Measurement data
└── logs/
    ├── download.log
    └── processing.log
```

## 🎯 Next Steps

After Phase 3 completion:
1. ✅ ARGO data loaded into database
2. ➡️ **Phase 4**: Build AI/RAG pipeline
3. ➡️ **Phase 5**: Create chatbot interface
4. ➡️ **Phase 6**: Build Streamlit dashboard

## 💡 Tips

1. **Start Small**: Use `--limit 100` first to test the pipeline
2. **Check Logs**: All operations are logged to `data/logs/`
3. **Monitor Progress**: Progress bars show download/parsing status
4. **Incremental**: You can run the pipeline multiple times, it won't duplicate data

---

**Ready to download ARGO data!** 🌊

Run: `python src/data/run_pipeline.py --limit 100`
