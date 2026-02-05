# Phase 3: ARGO Data Acquisition & Processing

## Overview

In this phase, we'll download real ARGO ocean data and load it into our PostgreSQL database. ARGO is a global network of autonomous profiling floats that measure ocean temperature, salinity, and pressure.

## Data Source

**ARGO GDAC (Global Data Assembly Center)**
- **Primary Server**: https://data-argo.ifremer.fr (France)
- **Mirror**: https://usgodae.org/ftp/outgoing/argo (USA)
- **Data Format**: NetCDF (Network Common Data Form)
- **Coverage**: Global ocean, 2000-present
- **Update Frequency**: Real-time (daily updates)

## Our Strategy

### 1. **Focused Dataset** (Manageable Size)
Instead of downloading ALL ARGO data (100+ GB), we'll focus on:
- **Region**: Indian Ocean
- **Time Period**: 2020-2024 (5 years)
- **Estimated Size**: ~2-5 GB
- **Float Count**: ~200-300 floats
- **Profiles**: ~50,000-100,000 profiles

### 2. **Data Download Approach**

We'll use the **ARGO Index File** approach:
1. Download the global index file (lists all available profiles)
2. Filter for Indian Ocean region (lat/lon bounds)
3. Filter for 2020-2024 time period
4. Download only matching NetCDF files
5. Process and load into database

### 3. **Indian Ocean Bounds**
```
Latitude: -40°S to 30°N
Longitude: 20°E to 120°E
```

This covers:
- Arabian Sea
- Bay of Bengal
- Southern Indian Ocean
- East African Coast
- Western Australian Coast

## Data Processing Pipeline

```
┌─────────────────┐
│  ARGO GDAC FTP  │
│  (ifremer.fr)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Download Index  │
│   (CSV file)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Filter Profiles │
│ (Indian Ocean)  │
│  (2020-2024)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Download NetCDF │
│     Files       │
│  (Parallel)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Parse NetCDF   │
│   (xarray)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Extract Data:   │
│ - Float info    │
│ - Profiles      │
│ - Measurements  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Load into       │
│  PostgreSQL     │
│  (floatchat)    │
└─────────────────┘
```

## Implementation Steps

### Step 1: Create Data Downloader
- Script to download ARGO index file
- Filter for Indian Ocean region
- Download NetCDF files in parallel
- Verify checksums
- Handle errors and retries

### Step 2: Create NetCDF Parser
- Use xarray to read NetCDF files
- Extract float metadata
- Extract profile data (lat, lon, date)
- Extract measurements (pressure, temperature, salinity)
- Handle quality control flags

### Step 3: Create Database Loader
- Insert float records
- Insert profile records with PostGIS geometry
- Insert measurement records
- Calculate derived properties
- Update summary statistics

### Step 4: Data Quality Assurance
- Validate data ranges
- Check for duplicates
- Apply ARGO QC flags
- Log processing statistics

## Expected Results

After Phase 3 completion:
- ✅ 200-300 ARGO floats in database
- ✅ 50,000-100,000 profiles
- ✅ 5-10 million measurements
- ✅ Spatial coverage of Indian Ocean
- ✅ Temporal coverage 2020-2024
- ✅ Ready for AI/RAG pipeline

## File Structure

```
data/
├── raw/
│   ├── index/
│   │   └── ar_index_global_prof.txt  # Global index
│   └── netcdf/
│       ├── 2901234_001.nc
│       ├── 2901234_002.nc
│       └── ...
├── processed/
│   ├── floats.parquet
│   ├── profiles.parquet
│   └── measurements.parquet
└── logs/
    ├── download.log
    └── processing.log
```

## Scripts to Create

1. **`src/data/download_index.py`** - Download and filter ARGO index
2. **`src/data/download_netcdf.py`** - Download NetCDF files
3. **`src/data/parse_netcdf.py`** - Parse NetCDF to DataFrames
4. **`src/data/load_database.py`** - Load data into PostgreSQL
5. **`src/data/validate_data.py`** - Data quality checks

## Time Estimate

- **Index Download**: 2 minutes
- **NetCDF Download**: 30-60 minutes (depends on internet speed)
- **Data Processing**: 15-30 minutes
- **Database Loading**: 10-20 minutes
- **Total**: ~1.5-2 hours

## Next Steps

1. Create download scripts
2. Download ARGO index file
3. Filter for Indian Ocean
4. Download sample NetCDF files (start with 10-20 floats)
5. Test parsing and loading
6. Scale up to full dataset

---

**Ready to start building the data acquisition pipeline!** 🚀
