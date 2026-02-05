"""
ARGO NetCDF Parser
Parses ARGO NetCDF files and extracts float, profile, and measurement data
Uses xarray for efficient NetCDF reading
"""

import xarray as xr
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from loguru import logger
import sys
from tqdm import tqdm

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.config import settings
from src.utils.logger import setup_logger

# Setup logging
setup_logger()


def parse_netcdf_file(nc_file):
    """Parse a single NetCDF file and extract data"""
    try:
        # Open NetCDF file
        ds = xr.open_dataset(nc_file)
        
        # Extract float information
        float_id = str(nc_file.parent.parent.name)  # e.g., "2901234"
        
        # Extract profile data
        profiles = []
        measurements = []
        
        # Get number of profiles in this file
        n_prof = ds.dims.get('N_PROF', 1)
        n_levels = ds.dims.get('N_LEVELS', 0)
        
        for prof_idx in range(n_prof):
            # Profile metadata
            if n_prof == 1:
                lat = float(ds['LATITUDE'].values)
                lon = float(ds['LONGITUDE'].values)
                date = pd.to_datetime(str(ds['JULD'].values))
                cycle = int(ds['CYCLE_NUMBER'].values) if 'CYCLE_NUMBER' in ds else prof_idx
            else:
                lat = float(ds['LATITUDE'].values[prof_idx])
                lon = float(ds['LONGITUDE'].values[prof_idx])
                date = pd.to_datetime(str(ds['JULD'].values[prof_idx]))
                cycle = int(ds['CYCLE_NUMBER'].values[prof_idx]) if 'CYCLE_NUMBER' in ds else prof_idx
            
            profile_id = f"{float_id}_{cycle:03d}"
            
            # Profile record
            profile = {
                'profile_id': profile_id,
                'float_id': float_id,
                'cycle_number': cycle,
                'latitude': lat,
                'longitude': lon,
                'date': date,
                'n_levels': n_levels
            }
            profiles.append(profile)
            
            # Extract measurements
            if n_levels > 0:
                # Get pressure, temperature, salinity
                if n_prof == 1:
                    pres = ds['PRES'].values
                    temp = ds['TEMP'].values if 'TEMP' in ds else np.full(n_levels, np.nan)
                    psal = ds['PSAL'].values if 'PSAL' in ds else np.full(n_levels, np.nan)
                    
                    # Quality flags
                    pres_qc = ds['PRES_QC'].values if 'PRES_QC' in ds else np.full(n_levels, '1')
                    temp_qc = ds['TEMP_QC'].values if 'TEMP_QC' in ds else np.full(n_levels, '1')
                    psal_qc = ds['PSAL_QC'].values if 'PSAL_QC' in ds else np.full(n_levels, '1')
                else:
                    pres = ds['PRES'].values[prof_idx, :]
                    temp = ds['TEMP'].values[prof_idx, :] if 'TEMP' in ds else np.full(n_levels, np.nan)
                    psal = ds['PSAL'].values[prof_idx, :] if 'PSAL' in ds else np.full(n_levels, np.nan)
                    
                    pres_qc = ds['PRES_QC'].values[prof_idx, :] if 'PRES_QC' in ds else np.full(n_levels, '1')
                    temp_qc = ds['TEMP_QC'].values[prof_idx, :] if 'TEMP_QC' in ds else np.full(n_levels, '1')
                    psal_qc = ds['PSAL_QC'].values[prof_idx, :] if 'PSAL_QC' in ds else np.full(n_levels, '1')
                
                # Create measurement records
                for level_idx in range(n_levels):
                    # Skip if all values are NaN
                    if np.isnan(pres[level_idx]) and np.isnan(temp[level_idx]) and np.isnan(psal[level_idx]):
                        continue
                    
                    # Convert QC flags to strings
                    pres_qc_str = str(pres_qc[level_idx]) if isinstance(pres_qc[level_idx], (int, float)) else pres_qc[level_idx].decode() if isinstance(pres_qc[level_idx], bytes) else '1'
                    temp_qc_str = str(temp_qc[level_idx]) if isinstance(temp_qc[level_idx], (int, float)) else temp_qc[level_idx].decode() if isinstance(temp_qc[level_idx], bytes) else '1'
                    psal_qc_str = str(psal_qc[level_idx]) if isinstance(psal_qc[level_idx], (int, float)) else psal_qc[level_idx].decode() if isinstance(psal_qc[level_idx], bytes) else '1'
                    
                    measurement = {
                        'profile_id': profile_id,
                        'level': level_idx,
                        'pressure': float(pres[level_idx]) if not np.isnan(pres[level_idx]) else None,
                        'temperature': float(temp[level_idx]) if not np.isnan(temp[level_idx]) else None,
                        'salinity': float(psal[level_idx]) if not np.isnan(psal[level_idx]) else None,
                        'pressure_qc': pres_qc_str,
                        'temperature_qc': temp_qc_str,
                        'salinity_qc': psal_qc_str
                    }
                    measurements.append(measurement)
        
        ds.close()
        
        return {
            'float_id': float_id,
            'profiles': profiles,
            'measurements': measurements,
            'success': True,
            'error': None
        }
        
    except Exception as e:
        logger.error(f"Failed to parse {nc_file}: {e}")
        return {
            'float_id': None,
            'profiles': [],
            'measurements': [],
            'success': False,
            'error': str(e)
        }


def parse_all_netcdf_files():
    """Parse all downloaded NetCDF files"""
    logger.info("Starting NetCDF parsing...")
    
    netcdf_dir = Path(settings.data_raw_dir) / "netcdf"
    
    if not netcdf_dir.exists():
        logger.error(f"NetCDF directory not found: {netcdf_dir}")
        logger.info("Run download_netcdf.py first!")
        return
    
    # Find all NetCDF files
    nc_files = list(netcdf_dir.rglob("*.nc"))
    logger.info(f"Found {len(nc_files):,} NetCDF files")
    
    if len(nc_files) == 0:
        logger.warning("No NetCDF files found!")
        return
    
    # Parse all files
    all_floats = set()
    all_profiles = []
    all_measurements = []
    failed_files = []
    
    for nc_file in tqdm(nc_files, desc="Parsing NetCDF files"):
        result = parse_netcdf_file(nc_file)
        
        if result['success']:
            all_floats.add(result['float_id'])
            all_profiles.extend(result['profiles'])
            all_measurements.extend(result['measurements'])
        else:
            failed_files.append((nc_file, result['error']))
    
    # Convert to DataFrames
    logger.info("Converting to DataFrames...")
    
    floats_df = pd.DataFrame([{'float_id': fid} for fid in all_floats])
    profiles_df = pd.DataFrame(all_profiles)
    measurements_df = pd.DataFrame(all_measurements)
    
    # Save to parquet
    processed_dir = Path(settings.data_processed_dir)
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    floats_df.to_parquet(processed_dir / "floats.parquet", index=False)
    profiles_df.to_parquet(processed_dir / "profiles.parquet", index=False)
    measurements_df.to_parquet(processed_dir / "measurements.parquet", index=False)
    
    logger.success(f"Saved floats: {len(floats_df):,}")
    logger.success(f"Saved profiles: {len(profiles_df):,}")
    logger.success(f"Saved measurements: {len(measurements_df):,}")
    
    # Print statistics
    logger.info("\n" + "="*60)
    logger.info("PARSING STATISTICS")
    logger.info("="*60)
    logger.info(f"Files Processed: {len(nc_files):,}")
    logger.info(f"Files Failed: {len(failed_files):,}")
    logger.info(f"Unique Floats: {len(floats_df):,}")
    logger.info(f"Total Profiles: {len(profiles_df):,}")
    logger.info(f"Total Measurements: {len(measurements_df):,}")
    logger.info(f"Avg Measurements/Profile: {len(measurements_df)/len(profiles_df):.1f}")
    logger.info("="*60 + "\n")
    
    if failed_files:
        failed_log = Path(settings.data_logs_dir) / "failed_parsing.txt"
        failed_log.parent.mkdir(parents=True, exist_ok=True)
        with open(failed_log, 'w') as f:
            for file, error in failed_files:
                f.write(f"{file}\t{error}\n")
        logger.warning(f"Failed files logged to: {failed_log}")
    
    return floats_df, profiles_df, measurements_df


def main():
    """Main execution"""
    logger.info("Starting ARGO NetCDF Parsing")
    
    try:
        floats_df, profiles_df, measurements_df = parse_all_netcdf_files()
        
        logger.success("NetCDF parsing complete!")
        logger.info("Next step: Load into database using: python src/data/load_database.py")
        
    except Exception as e:
        logger.error(f"Failed: {e}")
        raise


if __name__ == "__main__":
    main()
