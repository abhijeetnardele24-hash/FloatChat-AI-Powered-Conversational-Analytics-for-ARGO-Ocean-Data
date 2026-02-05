"""
ARGO Data Downloader - Index File
Downloads and filters the ARGO global index file for Indian Ocean region
"""

import requests
import pandas as pd
from pathlib import Path
from datetime import datetime
from loguru import logger
import sys

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.config import settings
from src.utils.logger import setup_logger

# Setup logging
setup_logger()

# ARGO Index URL
ARGO_INDEX_URL = "https://data-argo.ifremer.fr/ar_index_global_prof.txt"

# Indian Ocean Bounds
INDIAN_OCEAN_BOUNDS = {
    'lat_min': -40.0,  # 40°S
    'lat_max': 30.0,   # 30°N
    'lon_min': 20.0,   # 20°E
    'lon_max': 120.0   # 120°E
}

# Date range
DATE_START = "2020-01-01"
DATE_END = "2024-12-31"


def download_index_file():
    """Download the ARGO global index file"""
    logger.info(f"Downloading ARGO index from {ARGO_INDEX_URL}")
    
    # Create index directory
    index_dir = Path(settings.data_raw_dir) / "index"
    index_dir.mkdir(parents=True, exist_ok=True)
    
    index_file = index_dir / "ar_index_global_prof.txt"
    
    try:
        # Download with progress
        response = requests.get(ARGO_INDEX_URL, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        logger.info(f"Index file size: {total_size / 1024 / 1024:.2f} MB")
        
        # Save to file
        with open(index_file, 'wb') as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    progress = (downloaded / total_size) * 100
                    print(f"\rDownloading: {progress:.1f}%", end='', flush=True)
        
        print()  # New line after progress
        logger.success(f"Index file downloaded: {index_file}")
        return index_file
        
    except Exception as e:
        logger.error(f"Failed to download index: {e}")
        raise


def parse_index_file(index_file):
    """Parse the ARGO index file into a DataFrame"""
    logger.info(f"Parsing index file: {index_file}")
    
    try:
        # Read the index file (comma-separated)
        # Skip comment lines starting with #
        df = pd.read_csv(
            index_file,
            comment='#',
            skipinitialspace=True
        )
        
        logger.info(f"Total profiles in index: {len(df):,}")
        logger.info(f"Columns: {list(df.columns)}")
        
        return df
        
    except Exception as e:
        logger.error(f"Failed to parse index: {e}")
        raise


def filter_indian_ocean(df):
    """Filter profiles for Indian Ocean region"""
    logger.info("Filtering for Indian Ocean region...")
    
    # Filter by latitude and longitude
    mask = (
        (df['latitude'] >= INDIAN_OCEAN_BOUNDS['lat_min']) &
        (df['latitude'] <= INDIAN_OCEAN_BOUNDS['lat_max']) &
        (df['longitude'] >= INDIAN_OCEAN_BOUNDS['lon_min']) &
        (df['longitude'] <= INDIAN_OCEAN_BOUNDS['lon_max'])
    )
    
    filtered_df = df[mask].copy()
    
    logger.info(f"Profiles in Indian Ocean: {len(filtered_df):,}")
    logger.info(f"Reduction: {(1 - len(filtered_df)/len(df)) * 100:.1f}%")
    
    return filtered_df


def filter_by_date(df):
    """Filter profiles by date range"""
    logger.info(f"Filtering for dates: {DATE_START} to {DATE_END}")
    
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d%H%M%S', errors='coerce')
    
    # Filter by date range
    start_date = pd.to_datetime(DATE_START)
    end_date = pd.to_datetime(DATE_END)
    
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    filtered_df = df[mask].copy()
    
    logger.info(f"Profiles in date range: {len(filtered_df):,}")
    
    return filtered_df


def save_filtered_index(df):
    """Save filtered index to CSV"""
    output_file = Path(settings.data_raw_dir) / "index" / "indian_ocean_2020_2024.csv"
    
    df.to_csv(output_file, index=False)
    logger.success(f"Filtered index saved: {output_file}")
    
    return output_file


def print_statistics(df):
    """Print statistics about the filtered dataset"""
    logger.info("\n" + "="*60)
    logger.info("FILTERED DATASET STATISTICS")
    logger.info("="*60)
    
    logger.info(f"Total Profiles: {len(df):,}")
    logger.info(f"Unique Floats: {df['file'].str.split('/').str[0].nunique():,}")
    logger.info(f"Date Range: {df['date'].min()} to {df['date'].max()}")
    logger.info(f"Latitude Range: {df['latitude'].min():.2f}° to {df['latitude'].max():.2f}°")
    logger.info(f"Longitude Range: {df['longitude'].min():.2f}° to {df['longitude'].max():.2f}°")
    
    # Profiles per year
    df['year'] = df['date'].dt.year
    profiles_per_year = df.groupby('year').size()
    logger.info("\nProfiles per year:")
    for year, count in profiles_per_year.items():
        logger.info(f"  {year}: {count:,}")
    
    logger.info("="*60 + "\n")


def main():
    """Main execution"""
    logger.info("Starting ARGO Index Download and Filtering")
    logger.info(f"Target Region: Indian Ocean")
    logger.info(f"Target Period: {DATE_START} to {DATE_END}")
    
    try:
        # Step 1: Download index
        index_file = download_index_file()
        
        # Step 2: Parse index
        df = parse_index_file(index_file)
        
        # Step 3: Filter by region
        df = filter_indian_ocean(df)
        
        # Step 4: Filter by date
        df = filter_by_date(df)
        
        # Step 5: Save filtered index
        output_file = save_filtered_index(df)
        
        # Step 6: Print statistics
        print_statistics(df)
        
        logger.success("Index download and filtering complete!")
        logger.info(f"Next step: Download NetCDF files using: python src/data/download_netcdf.py")
        
        return output_file
        
    except Exception as e:
        logger.error(f"Failed: {e}")
        raise


if __name__ == "__main__":
    main()
