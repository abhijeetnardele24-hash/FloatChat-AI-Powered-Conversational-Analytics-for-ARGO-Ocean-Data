"""
ARGO Database Loader
Loads parsed ARGO data into PostgreSQL database
Handles floats, profiles, and measurements tables
"""

import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text
from loguru import logger
import sys
from tqdm import tqdm

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.config import settings
from src.utils.logger import setup_logger
from src.database.connection import get_db_engine

# Setup logging
setup_logger()


def load_floats(floats_df, engine):
    """Load float data into database"""
    logger.info(f"Loading {len(floats_df):,} floats...")
    
    # Add metadata columns
    floats_df['platform_type'] = 'ARGO_FLOAT'
    floats_df['status'] = 'ACTIVE'
    floats_df['created_at'] = pd.Timestamp.now()
    floats_df['updated_at'] = pd.Timestamp.now()
    
    # Load to database (upsert - insert or update)
    floats_df.to_sql(
        'argo_floats',
        engine,
        if_exists='append',
        index=False,
        method='multi',
        chunksize=1000
    )
    
    logger.success(f"Loaded {len(floats_df):,} floats")


def load_profiles(profiles_df, engine):
    """Load profile data into database with PostGIS geometry"""
    logger.info(f"Loading {len(profiles_df):,} profiles...")
    
    # Add metadata
    profiles_df['created_at'] = pd.Timestamp.now()
    profiles_df['updated_at'] = pd.Timestamp.now()
    
    # Load in chunks with progress bar
    chunk_size = 1000
    total_chunks = (len(profiles_df) + chunk_size - 1) // chunk_size
    
    with tqdm(total=total_chunks, desc="Loading profiles") as pbar:
        for i in range(0, len(profiles_df), chunk_size):
            chunk = profiles_df.iloc[i:i+chunk_size].copy()
            
            # Create WKT geometry strings for PostGIS
            chunk['location_wkt'] = chunk.apply(
                lambda row: f"POINT({row['longitude']} {row['latitude']})",
                axis=1
            )
            
            # Insert chunk
            with engine.connect() as conn:
                for _, row in chunk.iterrows():
                    try:
                        conn.execute(text("""
                            INSERT INTO argo_profiles 
                            (profile_id, float_id, cycle_number, latitude, longitude, 
                             location, date, n_levels, created_at, updated_at)
                            VALUES 
                            (:profile_id, :float_id, :cycle_number, :latitude, :longitude,
                             ST_GeomFromText(:location_wkt, 4326), :date, :n_levels, 
                             :created_at, :updated_at)
                            ON CONFLICT (profile_id) DO NOTHING
                        """), {
                            'profile_id': row['profile_id'],
                            'float_id': row['float_id'],
                            'cycle_number': row['cycle_number'],
                            'latitude': row['latitude'],
                            'longitude': row['longitude'],
                            'location_wkt': row['location_wkt'],
                            'date': row['date'],
                            'n_levels': row['n_levels'],
                            'created_at': row['created_at'],
                            'updated_at': row['updated_at']
                        })
                    except Exception as e:
                        logger.error(f"Failed to insert profile {row['profile_id']}: {e}")
                
                conn.commit()
            
            pbar.update(1)
    
    logger.success(f"Loaded {len(profiles_df):,} profiles")


def load_measurements(measurements_df, engine):
    """Load measurement data into database"""
    logger.info(f"Loading {len(measurements_df):,} measurements...")
    
    # Add metadata
    measurements_df['created_at'] = pd.Timestamp.now()
    
    # Load in chunks with progress bar
    chunk_size = 5000
    total_chunks = (len(measurements_df) + chunk_size - 1) // chunk_size
    
    with tqdm(total=total_chunks, desc="Loading measurements") as pbar:
        for i in range(0, len(measurements_df), chunk_size):
            chunk = measurements_df.iloc[i:i+chunk_size]
            
            chunk.to_sql(
                'argo_measurements',
                engine,
                if_exists='append',
                index=False,
                method='multi',
                chunksize=1000
            )
            
            pbar.update(1)
    
    logger.success(f"Loaded {len(measurements_df):,} measurements")


def update_statistics(engine):
    """Update database statistics and vacuum"""
    logger.info("Updating database statistics...")
    
    with engine.connect() as conn:
        # Analyze tables
        conn.execute(text("ANALYZE argo_floats"))
        conn.execute(text("ANALYZE argo_profiles"))
        conn.execute(text("ANALYZE argo_measurements"))
        conn.commit()
    
    logger.success("Database statistics updated")


def print_database_stats(engine):
    """Print database statistics"""
    logger.info("\n" + "="*60)
    logger.info("DATABASE STATISTICS")
    logger.info("="*60)
    
    with engine.connect() as conn:
        # Count floats
        result = conn.execute(text("SELECT COUNT(*) FROM argo_floats"))
        float_count = result.scalar()
        logger.info(f"Total Floats: {float_count:,}")
        
        # Count profiles
        result = conn.execute(text("SELECT COUNT(*) FROM argo_profiles"))
        profile_count = result.scalar()
        logger.info(f"Total Profiles: {profile_count:,}")
        
        # Count measurements
        result = conn.execute(text("SELECT COUNT(*) FROM argo_measurements"))
        measurement_count = result.scalar()
        logger.info(f"Total Measurements: {measurement_count:,}")
        
        # Date range
        result = conn.execute(text("""
            SELECT MIN(date), MAX(date) 
            FROM argo_profiles
        """))
        min_date, max_date = result.fetchone()
        logger.info(f"Date Range: {min_date} to {max_date}")
        
        # Geographic bounds
        result = conn.execute(text("""
            SELECT 
                MIN(latitude), MAX(latitude),
                MIN(longitude), MAX(longitude)
            FROM argo_profiles
        """))
        min_lat, max_lat, min_lon, max_lon = result.fetchone()
        logger.info(f"Latitude Range: {min_lat:.2f}° to {max_lat:.2f}°")
        logger.info(f"Longitude Range: {min_lon:.2f}° to {max_lon:.2f}°")
    
    logger.info("="*60 + "\n")


def main():
    """Main execution"""
    logger.info("Starting ARGO Database Loading")
    
    try:
        # Load parsed data
        processed_dir = Path(settings.data_processed_dir)
        
        floats_file = processed_dir / "floats.parquet"
        profiles_file = processed_dir / "profiles.parquet"
        measurements_file = processed_dir / "measurements.parquet"
        
        if not all([floats_file.exists(), profiles_file.exists(), measurements_file.exists()]):
            logger.error("Parsed data files not found!")
            logger.info("Run parse_netcdf.py first!")
            return
        
        logger.info("Loading parsed data files...")
        floats_df = pd.read_parquet(floats_file)
        profiles_df = pd.read_parquet(profiles_file)
        measurements_df = pd.read_parquet(measurements_file)
        
        logger.info(f"Loaded {len(floats_df):,} floats")
        logger.info(f"Loaded {len(profiles_df):,} profiles")
        logger.info(f"Loaded {len(measurements_df):,} measurements")
        
        # Get database engine
        engine = get_db_engine()
        
        # Load data
        logger.info("\nLoading data into PostgreSQL...")
        
        # 1. Load floats
        load_floats(floats_df, engine)
        
        # 2. Load profiles
        load_profiles(profiles_df, engine)
        
        # 3. Load measurements
        load_measurements(measurements_df, engine)
        
        # 4. Update statistics
        update_statistics(engine)
        
        # 5. Print statistics
        print_database_stats(engine)
        
        logger.success("Database loading complete!")
        logger.info("Data is now ready for AI/RAG pipeline!")
        
    except Exception as e:
        logger.error(f"Failed: {e}")
        raise


if __name__ == "__main__":
    main()
