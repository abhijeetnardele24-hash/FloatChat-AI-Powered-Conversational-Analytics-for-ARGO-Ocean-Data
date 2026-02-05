"""
ARGO NetCDF File Downloader
Downloads NetCDF profile files based on filtered index
Supports parallel downloads with progress tracking
"""

import requests
import pandas as pd
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from loguru import logger
import sys
import time
from tqdm import tqdm

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.config import settings
from src.utils.logger import setup_logger

# Setup logging
setup_logger()

# ARGO GDAC Base URL
ARGO_BASE_URL = "https://data-argo.ifremer.fr"

# Download settings for GLOBAL dataset (20-25 GB)
MAX_WORKERS = 10  # Parallel downloads (increased for faster download)
CHUNK_SIZE = 8192  # Download chunk size
RETRY_ATTEMPTS = 3  # Retry failed downloads
BATCH_SIZE = 1000  # Process in batches for progress tracking


def load_filtered_index():
    """Load the filtered index file (GLOBAL coverage)"""
    index_file = Path(settings.data_raw_dir) / "index" / "global_argo_2018_2024.csv"
    
    if not index_file.exists():
        logger.error(f"Filtered index not found: {index_file}")
        logger.info("Run download_index.py first!")
        raise FileNotFoundError(f"Index file not found: {index_file}")
    
    df = pd.read_csv(index_file)
    logger.info(f"Loaded {len(df):,} profiles from GLOBAL index (2018-2024)")
    
    return df


def download_file(url, output_path, retry=0):
    """Download a single file with retry logic"""
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        # Create parent directory
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Download file
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                f.write(chunk)
        
        return True, None
        
    except Exception as e:
        if retry < RETRY_ATTEMPTS:
            logger.warning(f"Retry {retry + 1}/{RETRY_ATTEMPTS} for {url}")
            time.sleep(2 ** retry)  # Exponential backoff
            return download_file(url, output_path, retry + 1)
        else:
            return False, str(e)


def download_netcdf_files(df, limit=None):
    """Download NetCDF files in parallel"""
    logger.info("Starting NetCDF file downloads...")
    
    # Limit number of files if specified (for testing)
    if limit:
        df = df.head(limit)
        logger.info(f"Limiting to {limit} files for testing")
    
    # Prepare download list
    downloads = []
    netcdf_dir = Path(settings.data_raw_dir) / "netcdf"
    
    for idx, row in df.iterrows():
        file_path = row['file']  # e.g., "aoml/2901234/profiles/D2901234_001.nc"
        url = f"{ARGO_BASE_URL}/{file_path}"
        
        # Create local path
        local_path = netcdf_dir / file_path
        
        # Skip if already downloaded
        if local_path.exists():
            continue
        
        downloads.append((url, local_path))
    
    logger.info(f"Files to download: {len(downloads):,}")
    
    if len(downloads) == 0:
        logger.success("All files already downloaded!")
        return
    
    # Download in parallel with progress bar
    successful = 0
    failed = 0
    failed_urls = []
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit all downloads
        futures = {
            executor.submit(download_file, url, path): (url, path)
            for url, path in downloads
        }
        
        # Process completed downloads with progress bar
        with tqdm(total=len(downloads), desc="Downloading", unit="file") as pbar:
            for future in as_completed(futures):
                url, path = futures[future]
                success, error = future.result()
                
                if success:
                    successful += 1
                else:
                    failed += 1
                    failed_urls.append((url, error))
                    logger.error(f"Failed: {url} - {error}")
                
                pbar.update(1)
                pbar.set_postfix({
                    'success': successful,
                    'failed': failed
                })
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("DOWNLOAD SUMMARY")
    logger.info("="*60)
    logger.info(f"Successful: {successful:,}")
    logger.info(f"Failed: {failed:,}")
    logger.info(f"Total: {len(downloads):,}")
    logger.info("="*60 + "\n")
    
    # Save failed URLs for retry
    if failed_urls:
        failed_file = Path(settings.data_raw_dir) / "index" / "failed_downloads.txt"
        with open(failed_file, 'w') as f:
            for url, error in failed_urls:
                f.write(f"{url}\t{error}\n")
        logger.warning(f"Failed URLs saved to: {failed_file}")


def get_download_statistics():
    """Get statistics about downloaded files"""
    netcdf_dir = Path(settings.data_raw_dir) / "netcdf"
    
    if not netcdf_dir.exists():
        logger.info("No NetCDF files downloaded yet")
        return
    
    # Count files
    nc_files = list(netcdf_dir.rglob("*.nc"))
    total_files = len(nc_files)
    
    # Calculate total size
    total_size = sum(f.stat().st_size for f in nc_files)
    total_size_mb = total_size / 1024 / 1024
    
    # Count unique floats
    float_dirs = set(f.parent.parent.name for f in nc_files)
    
    logger.info("\n" + "="*60)
    logger.info("DOWNLOADED FILES STATISTICS")
    logger.info("="*60)
    logger.info(f"Total Files: {total_files:,}")
    logger.info(f"Unique Floats: {len(float_dirs):,}")
    logger.info(f"Total Size: {total_size_mb:.2f} MB")
    logger.info(f"Average File Size: {total_size_mb/total_files:.2f} MB")
    logger.info("="*60 + "\n")


def main():
    """Main execution"""
    logger.info("Starting ARGO NetCDF Download (GLOBAL Dataset)")
    logger.info("Target: 20-25 GB, All Ocean Regions, 2018-2024")
    
    try:
        # Load filtered index
        df = load_filtered_index()
        
        # Download ALL files for global coverage
        logger.info("Downloading COMPLETE global dataset...")
        logger.info(f"Expected download time: 4-6 hours (depends on internet speed)")
        logger.info(f"Parallel workers: {MAX_WORKERS}")
        
        download_netcdf_files(df, limit=None)  # No limit - download all
        
        # Show statistics
        get_download_statistics()
        
        logger.success("NetCDF download complete!")
        logger.info("Next step: Parse NetCDF files using: python src/data/parse_netcdf.py")
        
    except Exception as e:
        logger.error(f"Failed: {e}")
        raise


if __name__ == "__main__":
    main()
