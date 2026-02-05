"""
ARGO Data Pipeline - Master Script
Runs the complete data acquisition and processing pipeline:
1. Download ARGO index
2. Download NetCDF files
3. Parse NetCDF files
4. Load into database
"""

from pathlib import Path
from loguru import logger
import sys

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.logger import setup_logger

# Setup logging
setup_logger()


def run_pipeline(download_limit=100):
    """Run the complete ARGO data pipeline"""
    
    logger.info("="*70)
    logger.info("ARGO DATA ACQUISITION PIPELINE")
    logger.info("="*70)
    logger.info(f"Download Limit: {download_limit} files")
    logger.info("="*70 + "\n")
    
    try:
        # Step 1: Download and filter index
        logger.info("STEP 1: Downloading ARGO Index...")
        logger.info("-" * 70)
        from src.data.download_index import main as download_index_main
        download_index_main()
        logger.info("\n")
        
        # Step 2: Download NetCDF files
        logger.info("STEP 2: Downloading NetCDF Files...")
        logger.info("-" * 70)
        from src.data.download_netcdf import load_filtered_index, download_netcdf_files, get_download_statistics
        
        df = load_filtered_index()
        download_netcdf_files(df, limit=download_limit)
        get_download_statistics()
        logger.info("\n")
        
        # Step 3: Parse NetCDF files
        logger.info("STEP 3: Parsing NetCDF Files...")
        logger.info("-" * 70)
        from src.data.parse_netcdf import parse_all_netcdf_files
        parse_all_netcdf_files()
        logger.info("\n")
        
        # Step 4: Load into database
        logger.info("STEP 4: Loading into Database...")
        logger.info("-" * 70)
        from src.data.load_database import main as load_database_main
        load_database_main()
        logger.info("\n")
        
        # Success!
        logger.info("="*70)
        logger.success("PIPELINE COMPLETE!")
        logger.info("="*70)
        logger.info("✅ ARGO data successfully loaded into FloatChat database")
        logger.info("✅ Ready for AI/RAG pipeline development")
        logger.info("="*70 + "\n")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise


def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ARGO Data Acquisition Pipeline')
    parser.add_argument(
        '--limit',
        type=int,
        default=100,
        help='Number of NetCDF files to download (default: 100, use 0 for all)'
    )
    
    args = parser.parse_args()
    
    download_limit = None if args.limit == 0 else args.limit
    
    run_pipeline(download_limit=download_limit)


if __name__ == "__main__":
    main()
