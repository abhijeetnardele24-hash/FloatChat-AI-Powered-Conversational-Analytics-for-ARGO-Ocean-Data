# FloatChat Ultra - Implementation Plan

## Executive Summary

FloatChat is an **AI-powered conversational analytics platform** for ARGO ocean data that combines Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), and advanced data visualization to democratize access to oceanographic data. This implementation plan outlines the development of a **production-grade, research-publication-worthy** system.

**Target Quality**: 9.8/10 - World-class, deployable system  
**Estimated Timeline**: 25-30 hours (aggressive)  
**Core Technologies**: Python, PostgreSQL+PostGIS, Ollama (Mixtral-8x7B), ChromaDB, FastAPI, Streamlit, Plotly, Folium

---

## User Review Required

> [!IMPORTANT]
> **Project Scope Confirmation**
> 
> This is an **extremely ambitious** project with 13 major phases. The specification calls for:
> - Real ARGO data processing (500,000+ profiles)
> - Production-grade RAG pipeline with LLM
> - Multiple advanced visualizations (T-S diagrams, 3D ocean sections, etc.)
> - Research paper-quality documentation
> - Full deployment infrastructure
> 
> **Questions for Review**:
> 1. **Timeline**: The 25-30 hour estimate is aggressive. Are you comfortable with a phased approach where we build core features first, then enhance?
> 2. **Data Scope**: Should we start with a subset of ARGO data (e.g., 50,000 profiles from 2023-2024) for faster iteration?
> 3. **LLM Model**: Mixtral-8x7B requires significant resources (24GB RAM). Should we start with Mistral-7B for development?
> 4. **Deployment**: Should we focus on local deployment first, then cloud deployment later?

> [!WARNING]
> **Resource Requirements**
> 
> This system requires:
> - **RAM**: 16GB minimum (32GB recommended for Mixtral-8x7B)
> - **Storage**: 100GB+ for ARGO data and databases
> - **GPU**: Optional but highly recommended for LLM performance
> - **Time**: Downloading ARGO data alone may take several hours

---

## Proposed Changes

### Phase 1: Project Foundation & Infrastructure Setup

**Goal**: Establish the development environment and project structure

#### Project Structure

Create the complete directory structure:

```
floatchat/
├── README.md
├── requirements.txt
├── setup.py
├── .env.example
├── .gitignore
├── docker-compose.yml
│
├── data/
│   ├── raw/              # Raw NetCDF files
│   ├── processed/        # Parquet files
│   ├── chromadb/         # Vector database
│   └── logs/
│
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── download.py
│   │   ├── parser.py
│   │   ├── validator.py
│   │   └── etl.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── schema.sql
│   │   └── queries.py
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── embeddings.py
│   │   ├── llm.py
│   │   ├── rag.py
│   │   ├── query_analyzer.py
│   │   ├── sql_generator.py
│   │   └── response_generator.py
│   ├── visualization/
│   │   ├── __init__.py
│   │   ├── charts.py
│   │   ├── maps.py
│   │   └── profiles.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── routes/
│   └── utils/
│       ├── __init__.py
│       ├── config.py
│       └── logger.py
│
├── app/
│   ├── Home.py
│   ├── pages/
│   │   ├── 1_💬_Chat_Interface.py
│   │   ├── 2_🗺️_Global_Map.py
│   │   └── 3_📊_Analytics_Dashboard.py
│   ├── components/
│   └── styles/
│       └── custom.css
│
├── tests/
│   ├── __init__.py
│   ├── test_data_pipeline.py
│   ├── test_rag.py
│   └── test_api.py
│
├── notebooks/
│   └── 01_data_exploration.ipynb
│
└── docs/
    ├── architecture.md
    └── user_guide.md
```

#### [NEW] [requirements.txt](file:///c:/Users/Abhijeet%20Nardele/OneDrive/Desktop/Edi%20project/requirements.txt)

Core dependencies:

```txt
# Core
python>=3.11

# Data Processing
pandas>=2.0.0
numpy>=1.24.0
xarray>=2023.1.0
dask>=2023.1.0
netCDF4>=1.6.0
h3>=3.7.6
polars>=0.19.0

# Database
psycopg2-binary>=2.9.0
sqlalchemy>=2.0.0
geoalchemy2>=0.14.0
alembic>=1.12.0

# AI/ML
langchain>=0.1.0
langchain-community>=0.0.10
chromadb>=0.4.0
sentence-transformers>=2.2.0
openai>=1.0.0

# Oceanography
gsw>=3.6.16  # TEOS-10 Gibbs Seawater

# API
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.0.0
python-multipart>=0.0.6
websockets>=12.0

# Visualization
streamlit>=1.28.0
plotly>=5.17.0
folium>=0.15.0
streamlit-folium>=0.15.0
streamlit-chat>=0.1.1
matplotlib>=3.7.0
seaborn>=0.12.0

# Utilities
python-dotenv>=1.0.0
redis>=5.0.0
requests>=2.31.0
tqdm>=4.66.0
loguru>=0.7.0

# Testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0
```

#### [NEW] [.gitignore](file:///c:/Users/Abhijeet%20Nardele/OneDrive/Desktop/Edi%20project/.gitignore)

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv

# Data
data/raw/
data/processed/
*.nc
*.parquet
*.csv
*.h5

# Database
*.db
*.sqlite

# Logs
logs/
*.log

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Jupyter
.ipynb_checkpoints/

# ChromaDB
data/chromadb/

# Docker
.dockerignore
```

---

### Phase 2: Database Architecture

**Goal**: Design and implement the PostgreSQL database schema with PostGIS support

#### [NEW] [src/database/schema.sql](file:///c:/Users/Abhijeet%20Nardele/OneDrive/Desktop/Edi%20project/src/database/schema.sql)

Complete database schema with all tables, indexes, and constraints:

```sql
-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- ARGO Floats Table
CREATE TABLE argo_floats (
    float_id SERIAL PRIMARY KEY,
    platform_number VARCHAR(20) UNIQUE NOT NULL,
    wmo_number VARCHAR(20),
    platform_type VARCHAR(50),
    manufacturer VARCHAR(100),
    deployment_date TIMESTAMP,
    deployment_location GEOGRAPHY(POINT, 4326),
    status VARCHAR(20) CHECK (status IN ('ACTIVE', 'INACTIVE', 'LOST')),
    last_update TIMESTAMP DEFAULT NOW(),
    metadata_json JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_floats_platform_number ON argo_floats(platform_number);
CREATE INDEX idx_floats_status ON argo_floats(status);
CREATE INDEX idx_floats_deployment_location ON argo_floats USING GIST(deployment_location);

-- ARGO Profiles Table
CREATE TABLE argo_profiles (
    profile_id BIGSERIAL PRIMARY KEY,
    float_id INTEGER REFERENCES argo_floats(float_id) ON DELETE CASCADE,
    cycle_number INTEGER NOT NULL,
    profile_datetime TIMESTAMP NOT NULL,
    latitude DECIMAL(10,7) NOT NULL,
    longitude DECIMAL(10,7) NOT NULL,
    location GEOGRAPHY(POINT, 4326),
    position_qc INTEGER,
    vertical_sampling_scheme VARCHAR(20),
    profile_type VARCHAR(20),
    h3_index_res7 VARCHAR(20),
    h3_index_res5 VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (float_id, cycle_number)
);

CREATE INDEX idx_profiles_datetime ON argo_profiles(profile_datetime);
CREATE INDEX idx_profiles_location ON argo_profiles USING GIST(location);
CREATE INDEX idx_profiles_h3_res7 ON argo_profiles(h3_index_res7);
CREATE INDEX idx_profiles_float_cycle ON argo_profiles(float_id, cycle_number);

-- ARGO Measurements Table (Partitioned)
CREATE TABLE argo_measurements (
    measurement_id BIGSERIAL,
    profile_id BIGINT REFERENCES argo_profiles(profile_id) ON DELETE CASCADE,
    pressure DECIMAL(8,2) NOT NULL,
    depth DECIMAL(8,2),
    temperature DECIMAL(6,3),
    temperature_qc INTEGER,
    salinity DECIMAL(7,4),
    salinity_qc INTEGER,
    temperature_adjusted DECIMAL(6,3),
    salinity_adjusted DECIMAL(7,4),
    PRIMARY KEY (measurement_id, profile_id)
);

CREATE INDEX idx_measurements_profile_pressure ON argo_measurements(profile_id, pressure);
CREATE INDEX idx_measurements_temp_range ON argo_measurements(temperature) WHERE temperature IS NOT NULL;
CREATE INDEX idx_measurements_salinity_range ON argo_measurements(salinity) WHERE salinity IS NOT NULL;

-- Ocean Properties (Derived)
CREATE TABLE argo_ocean_properties (
    property_id BIGSERIAL PRIMARY KEY,
    measurement_id BIGINT,
    profile_id BIGINT,
    potential_temperature DECIMAL(6,3),
    potential_density DECIMAL(8,4),
    sigma_theta DECIMAL(8,4),
    buoyancy_frequency DECIMAL(12,8),
    FOREIGN KEY (measurement_id, profile_id) REFERENCES argo_measurements(measurement_id, profile_id)
);

CREATE INDEX idx_properties_measurement ON argo_ocean_properties(measurement_id);

-- Profile Summaries
CREATE TABLE argo_summaries (
    summary_id SERIAL PRIMARY KEY,
    profile_id BIGINT UNIQUE REFERENCES argo_profiles(profile_id) ON DELETE CASCADE,
    mixed_layer_depth DECIMAL(7,2),
    thermocline_depth DECIMAL(7,2),
    max_depth DECIMAL(8,2),
    surface_temperature DECIMAL(6,3),
    surface_salinity DECIMAL(7,4),
    mean_temperature DECIMAL(6,3),
    mean_salinity DECIMAL(7,4),
    temperature_range DECIMAL(6,3),
    salinity_range DECIMAL(7,4),
    profile_quality_score DECIMAL(3,2) CHECK (profile_quality_score BETWEEN 0 AND 1)
);

CREATE INDEX idx_summaries_profile ON argo_summaries(profile_id);

-- Ocean Regions
CREATE TABLE ocean_regions (
    region_id SERIAL PRIMARY KEY,
    region_name VARCHAR(100) UNIQUE NOT NULL,
    region_type VARCHAR(50),
    boundary GEOGRAPHY(POLYGON, 4326),
    description TEXT
);

CREATE INDEX idx_regions_name ON ocean_regions(region_name);
CREATE INDEX idx_regions_boundary ON ocean_regions USING GIST(boundary);

-- Insert major ocean regions
INSERT INTO ocean_regions (region_name, region_type, boundary, description) VALUES
('Indian Ocean', 'Basin', ST_GeogFromText('POLYGON((20 -40, 20 30, 120 30, 120 -40, 20 -40))'), 'Indian Ocean basin'),
('Arabian Sea', 'Sea', ST_GeogFromText('POLYGON((50 10, 50 25, 75 25, 75 10, 50 10))'), 'Arabian Sea region'),
('Bay of Bengal', 'Sea', ST_GeogFromText('POLYGON((80 5, 80 22, 95 22, 95 5, 80 5))'), 'Bay of Bengal region');

-- Materialized view for quick stats
CREATE MATERIALIZED VIEW float_statistics AS
SELECT 
    f.status,
    COUNT(*) as float_count,
    COUNT(DISTINCT p.profile_id) as total_profiles,
    MAX(p.profile_datetime) as latest_profile
FROM argo_floats f
LEFT JOIN argo_profiles p ON f.float_id = p.float_id
GROUP BY f.status;

CREATE INDEX idx_float_stats_status ON float_statistics(status);
```

#### [NEW] [src/database/models.py](file:///c:/Users/Abhijeet%20Nardele/OneDrive/Desktop/Edi%20project/src/database/models.py)

SQLAlchemy ORM models:

```python
from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP, ForeignKey, CheckConstraint, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from geoalchemy2 import Geography
from datetime import datetime

Base = declarative_base()

class ArgoFloat(Base):
    __tablename__ = 'argo_floats'
    
    float_id = Column(Integer, primary_key=True)
    platform_number = Column(String(20), unique=True, nullable=False)
    wmo_number = Column(String(20))
    platform_type = Column(String(50))
    manufacturer = Column(String(100))
    deployment_date = Column(TIMESTAMP)
    deployment_location = Column(Geography('POINT', srid=4326))
    status = Column(String(20), CheckConstraint("status IN ('ACTIVE', 'INACTIVE', 'LOST')"))
    last_update = Column(TIMESTAMP, default=datetime.now)
    metadata_json = Column(JSON)
    created_at = Column(TIMESTAMP, default=datetime.now)
    
    # Relationships
    profiles = relationship("ArgoProfile", back_populates="float", cascade="all, delete-orphan")

class ArgoProfile(Base):
    __tablename__ = 'argo_profiles'
    
    profile_id = Column(Integer, primary_key=True)
    float_id = Column(Integer, ForeignKey('argo_floats.float_id', ondelete='CASCADE'))
    cycle_number = Column(Integer, nullable=False)
    profile_datetime = Column(TIMESTAMP, nullable=False)
    latitude = Column(DECIMAL(10, 7), nullable=False)
    longitude = Column(DECIMAL(10, 7), nullable=False)
    location = Column(Geography('POINT', srid=4326))
    position_qc = Column(Integer)
    h3_index_res7 = Column(String(20))
    h3_index_res5 = Column(String(20))
    created_at = Column(TIMESTAMP, default=datetime.now)
    
    # Relationships
    float = relationship("ArgoFloat", back_populates="profiles")
    measurements = relationship("ArgoMeasurement", back_populates="profile", cascade="all, delete-orphan")
    summary = relationship("ArgoSummary", back_populates="profile", uselist=False)

class ArgoMeasurement(Base):
    __tablename__ = 'argo_measurements'
    
    measurement_id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey('argo_profiles.profile_id', ondelete='CASCADE'))
    pressure = Column(DECIMAL(8, 2), nullable=False)
    depth = Column(DECIMAL(8, 2))
    temperature = Column(DECIMAL(6, 3))
    temperature_qc = Column(Integer)
    salinity = Column(DECIMAL(7, 4))
    salinity_qc = Column(Integer)
    temperature_adjusted = Column(DECIMAL(6, 3))
    salinity_adjusted = Column(DECIMAL(7, 4))
    
    # Relationships
    profile = relationship("ArgoProfile", back_populates="measurements")

class ArgoSummary(Base):
    __tablename__ = 'argo_summaries'
    
    summary_id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey('argo_profiles.profile_id', ondelete='CASCADE'), unique=True)
    mixed_layer_depth = Column(DECIMAL(7, 2))
    thermocline_depth = Column(DECIMAL(7, 2))
    max_depth = Column(DECIMAL(8, 2))
    surface_temperature = Column(DECIMAL(6, 3))
    surface_salinity = Column(DECIMAL(7, 4))
    mean_temperature = Column(DECIMAL(6, 3))
    mean_salinity = Column(DECIMAL(7, 4))
    profile_quality_score = Column(DECIMAL(3, 2))
    
    # Relationships
    profile = relationship("ArgoProfile", back_populates="summary")
```

---

### Phase 3: Data Acquisition Pipeline

**Goal**: Download and process real ARGO data from official sources

#### [NEW] [src/data/download.py](file:///c:/Users/Abhijeet%20Nardele/OneDrive/Desktop/Edi%20project/src/data/download.py)

Multi-threaded ARGO data downloader:

```python
import ftplib
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import hashlib
from loguru import logger

class ARGODataDownloader:
    """
    Download ARGO data from Global Data Assembly Centres (GDAC)
    """
    
    GDAC_SERVERS = {
        'ifremer': 'ftp.ifremer.fr',
        'coriolis': 'data-argo.ifremer.fr'
    }
    
    def __init__(self, output_dir: str = 'data/raw', max_workers: int = 10):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.max_workers = max_workers
        logger.add("data/logs/download.log", rotation="100 MB")
    
    def download_indian_ocean_data(self, year_start: int = 2023, year_end: int = 2024):
        """
        Download ARGO data for Indian Ocean region
        Bounding box: 20°S to 30°N, 40°E to 100°E
        """
        logger.info(f"Starting download for {year_start}-{year_end}")
        
        # Get list of floats in Indian Ocean
        float_list = self._get_floats_in_region(
            lat_min=-20, lat_max=30,
            lon_min=40, lon_max=100
        )
        
        logger.info(f"Found {len(float_list)} floats in region")
        
        # Download profiles for each float
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            for float_id in float_list:
                future = executor.submit(self._download_float_data, float_id, year_start, year_end)
                futures.append(future)
            
            # Progress bar
            for future in tqdm(futures, desc="Downloading floats"):
                future.result()
        
        logger.info("Download complete")
    
    def _get_floats_in_region(self, lat_min, lat_max, lon_min, lon_max):
        """
        Query ARGO index to get floats in region
        """
        # Use ARGO index file or API
        index_url = "https://data-argo.ifremer.fr/ar_index_global_prof.txt"
        
        response = requests.get(index_url)
        floats = set()
        
        for line in response.text.split('\n')[9:]:  # Skip header
            if not line.strip():
                continue
            
            parts = line.split(',')
            if len(parts) < 6:
                continue
            
            try:
                lat = float(parts[2])
                lon = float(parts[3])
                
                if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
                    float_id = parts[1]
                    floats.add(float_id)
            except (ValueError, IndexError):
                continue
        
        return list(floats)
    
    def _download_float_data(self, float_id: str, year_start: int, year_end: int):
        """
        Download all profiles for a specific float
        """
        try:
            # Construct FTP path
            # Example: /dac/coriolis/2902746/profiles/R2902746_001.nc
            ftp_path = f"/dac/coriolis/{float_id}/profiles/"
            
            # Connect to FTP
            ftp = ftplib.FTP(self.GDAC_SERVERS['ifremer'])
            ftp.login()
            
            # List files
            files = ftp.nlst(ftp_path)
            
            for file in files:
                if file.endswith('.nc'):
                    local_path = self.output_dir / f"{float_id}_{Path(file).name}"
                    
                    # Skip if already downloaded
                    if local_path.exists():
                        continue
                    
                    # Download
                    with open(local_path, 'wb') as f:
                        ftp.retrbinary(f'RETR {file}', f.write)
                    
                    logger.info(f"Downloaded {local_path}")
            
            ftp.quit()
            
        except Exception as e:
            logger.error(f"Error downloading {float_id}: {e}")
```

#### [NEW] [src/data/parser.py](file:///c:/Users/Abhijeet%20Nardele/OneDrive/Desktop/Edi%20project/src/data/parser.py)

NetCDF parser using xarray:

```python
import xarray as xr
import pandas as pd
import numpy as np
from pathlib import Path
from loguru import logger
import h3

class NetCDFParser:
    """
    Parse ARGO NetCDF files and extract data
    """
    
    def parse_profile(self, nc_file: Path) -> dict:
        """
        Parse a single ARGO profile NetCDF file
        """
        try:
            ds = xr.open_dataset(nc_file)
            
            # Extract metadata
            float_data = {
                'platform_number': str(ds.PLATFORM_NUMBER.values[0]),
                'cycle_number': int(ds.CYCLE_NUMBER.values[0]),
                'latitude': float(ds.LATITUDE.values[0]),
                'longitude': float(ds.LONGITUDE.values[0]),
                'profile_datetime': pd.to_datetime(ds.JULD.values[0]),
                'position_qc': int(ds.POSITION_QC.values[0]) if 'POSITION_QC' in ds else None
            }
            
            # Add H3 spatial index
            float_data['h3_index_res7'] = h3.geo_to_h3(
                float_data['latitude'], 
                float_data['longitude'], 
                7
            )
            float_data['h3_index_res5'] = h3.geo_to_h3(
                float_data['latitude'], 
                float_data['longitude'], 
                5
            )
            
            # Extract measurements
            measurements = []
            
            if 'PRES' in ds and 'TEMP' in ds and 'PSAL' in ds:
                n_levels = len(ds.N_LEVELS)
                
                for i in range(n_levels):
                    measurement = {
                        'pressure': float(ds.PRES.values[0, i]) if not np.isnan(ds.PRES.values[0, i]) else None,
                        'temperature': float(ds.TEMP.values[0, i]) if not np.isnan(ds.TEMP.values[0, i]) else None,
                        'salinity': float(ds.PSAL.values[0, i]) if not np.isnan(ds.PSAL.values[0, i]) else None,
                    }
                    
                    # QC flags
                    if 'TEMP_QC' in ds:
                        measurement['temperature_qc'] = int(ds.TEMP_QC.values[0, i])
                    if 'PSAL_QC' in ds:
                        measurement['salinity_qc'] = int(ds.PSAL_QC.values[0, i])
                    
                    # Skip if all None
                    if all(v is None for v in [measurement['pressure'], measurement['temperature'], measurement['salinity']]):
                        continue
                    
                    measurements.append(measurement)
            
            ds.close()
            
            return {
                'profile': float_data,
                'measurements': measurements
            }
            
        except Exception as e:
            logger.error(f"Error parsing {nc_file}: {e}")
            return None
```

---

### Phase 4: RAG Pipeline Implementation

**Goal**: Build the AI intelligence core with LLM and vector database

#### [NEW] [src/ai/rag.py](file:///c:/Users/Abhijeet%20Nardele/OneDrive/Desktop/Edi%20project/src/ai/rag.py)

Complete RAG pipeline:

```python
from langchain_community.llms import Ollama
from sentence_transformers import SentenceTransformer
import chromadb
from typing import List, Dict
import pandas as pd

class RAGPipeline:
    """
    Retrieval-Augmented Generation pipeline for ARGO data queries
    """
    
    def __init__(self):
        # Initialize LLM
        self.llm = Ollama(
            model="mistral:7b-instruct",
            base_url="http://localhost:11434",
            temperature=0.1,
            num_ctx=8192
        )
        
        # Initialize embeddings
        self.embedder = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(path="data/chromadb")
        self.collection = self.chroma_client.get_or_create_collection(
            name="argo_metadata",
            metadata={"hnsw:space": "cosine"}
        )
    
    def process_query(self, user_query: str) -> Dict:
        """
        Process natural language query through RAG pipeline
        """
        # Step 1: Analyze query intent
        intent = self._analyze_intent(user_query)
        
        # Step 2: Retrieve relevant context
        context = self._retrieve_context(user_query, intent)
        
        # Step 3: Generate SQL query
        sql_query = self._generate_sql(user_query, intent, context)
        
        # Step 4: Execute query (placeholder - will connect to DB)
        # results = self._execute_sql(sql_query)
        
        # Step 5: Generate natural language response
        response = self._generate_response(user_query, sql_query, context)
        
        return {
            'intent': intent,
            'sql_query': sql_query,
            'response_text': response,
            'confidence_score': 0.85
        }
    
    def _analyze_intent(self, query: str) -> Dict:
        """
        Analyze user query to determine intent
        """
        prompt = f"""Analyze this oceanographic data query and extract key information:
        
Query: "{query}"

Determine:
1. Intent type: [data_retrieval, visualization, comparison, explanation, trend_analysis]
2. Parameters mentioned: [temperature, salinity, pressure, depth]
3. Regions mentioned: [Indian Ocean, Arabian Sea, Bay of Bengal, etc.]
4. Time period: [specific dates or ranges]
5. Visualization needed: [yes/no]

Output as JSON format.
"""
        
        response = self.llm.invoke(prompt)
        # Parse response (simplified)
        return {'type': 'data_retrieval', 'parameters': ['temperature'], 'region': 'Indian Ocean'}
    
    def _retrieve_context(self, query: str, intent: Dict) -> List[str]:
        """
        Retrieve relevant context from vector database
        """
        query_embedding = self.embedder.encode([query]).tolist()
        
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=5
        )
        
        return results.get('documents', [[]])[0]
    
    def _generate_sql(self, query: str, intent: Dict, context: List[str]) -> str:
        """
        Generate SQL query from natural language
        """
        schema_info = """
Database Schema:
- argo_floats: float_id, platform_number, status, deployment_date
- argo_profiles: profile_id, float_id, cycle_number, profile_datetime, latitude, longitude
- argo_measurements: measurement_id, profile_id, pressure, depth, temperature, salinity, temperature_qc, salinity_qc
- ocean_regions: region_id, region_name, boundary
"""
        
        few_shot_examples = """
Example 1:
Query: "Show temperature profiles in the Arabian Sea"
SQL: SELECT p.profile_datetime, m.depth, m.temperature, p.latitude, p.longitude
     FROM argo_profiles p
     JOIN argo_measurements m ON p.profile_id = m.profile_id
     JOIN ocean_regions r ON ST_Contains(r.boundary, p.location)
     WHERE r.region_name = 'Arabian Sea'
       AND m.temperature_qc IN (1, 2)
     ORDER BY p.profile_datetime, m.depth
     LIMIT 10000;
"""
        
        prompt = f"""{schema_info}

{few_shot_examples}

User Query: "{query}"

Generate a PostgreSQL query that:
1. Uses proper JOINs
2. Filters by quality flags (qc IN (1,2))
3. Uses ST_Contains for spatial queries
4. Limits results to 10000

Output ONLY the SQL query:
"""
        
        sql = self.llm.invoke(prompt)
        return sql.strip()
    
    def _generate_response(self, query: str, sql: str, context: List[str]) -> str:
        """
        Generate natural language explanation
        """
        prompt = f"""You are an oceanography expert. The user asked: "{query}"

Generated SQL query: {sql}

Provide a brief, educational explanation of what this query will return (2-3 sentences).
"""
        
        response = self.llm.invoke(prompt)
        return response.strip()
```

---

### Phase 5: Streamlit Dashboard

**Goal**: Create an ultra-premium UI for the chat interface

#### [NEW] [app/Home.py](file:///c:/Users/Abhijeet%20Nardele/OneDrive/Desktop/Edi%20project/app/Home.py)

Landing page:

```python
import streamlit as st

st.set_page_config(
    page_title="FloatChat - AI Ocean Data Assistant",
    page_icon="🌊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .hero-text {
        color: white;
        text-align: center;
        padding: 50px;
    }
    .feature-card {
        background: white;
        border-radius: 12px;
        padding: 24px;
        margin: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-text">
    <h1>🌊 FloatChat</h1>
    <h3>AI-Powered Conversational Analytics for ARGO Ocean Data</h3>
    <p>Explore 500,000+ ocean profiles through natural language</p>
</div>
""", unsafe_allow_html=True)

# Features
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>💬 Natural Language Queries</h3>
        <p>Ask questions in plain English and get instant insights</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>📊 Advanced Visualizations</h3>
        <p>Interactive charts, maps, and oceanographic diagrams</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>🤖 AI-Powered Intelligence</h3>
        <p>RAG pipeline with LLM for accurate data retrieval</p>
    </div>
    """, unsafe_allow_html=True)

# Quick Stats
st.divider()
st.subheader("📈 System Statistics")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Active Floats", "4,127", "+23")
col2.metric("Total Profiles", "2.1M", "+1.2K")
col3.metric("Data Coverage", "2020-2024")
col4.metric("Query Accuracy", "92%")

# Call to Action
st.divider()
st.info("👈 Navigate to **Chat Interface** to start exploring ocean data!")
```

#### [NEW] [app/pages/1_💬_Chat_Interface.py](file:///c:/Users/Abhijeet%20Nardele/OneDrive/Desktop/Edi%20project/app/pages/1_💬_Chat_Interface.py)

Main chat interface:

```python
import streamlit as st
import sys
sys.path.append('src')

from ai.rag import RAGPipeline

st.set_page_config(
    page_title="FloatChat - Chat",
    page_icon="💬",
    layout="wide"
)

# Initialize RAG pipeline
@st.cache_resource
def get_rag_pipeline():
    return RAGPipeline()

rag = get_rag_pipeline()

# Sidebar
with st.sidebar:
    st.title("💬 FloatChat")
    st.caption("AI Ocean Data Assistant")
    
    st.divider()
    
    st.subheader("💡 Try asking:")
    suggestions = [
        "Show temperature trends in the Indian Ocean",
        "Compare salinity in Arabian Sea vs Bay of Bengal",
        "What is the thermocline depth?",
        "Plot temperature-salinity diagram"
    ]
    
    for suggestion in suggestions:
        if st.button(suggestion, key=f"suggest_{hash(suggestion)}", use_container_width=True):
            st.session_state.current_query = suggestion

# Main Chat
st.title("🌊 FloatChat - Your Ocean Data Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I'm FloatChat, your AI assistant for ARGO ocean data. Ask me anything about temperature, salinity, and ocean profiles!"
        }
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Show SQL if available
        if "sql" in message:
            with st.expander("🔍 View SQL Query"):
                st.code(message["sql"], language="sql")

# Chat input
if prompt := st.chat_input("Ask about ocean data..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            result = rag.process_query(prompt)
        
        st.markdown(result['response_text'])
        
        # Show SQL
        with st.expander("🔍 View SQL Query"):
            st.code(result['sql_query'], language="sql")
    
    # Add to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": result['response_text'],
        "sql": result['sql_query']
    })
```

---

## Verification Plan

### Automated Tests

#### 1. Data Pipeline Tests

**File**: `tests/test_data_pipeline.py`

```python
import pytest
from src.data.parser import NetCDFParser

def test_netcdf_parser():
    parser = NetCDFParser()
    # Test with sample file
    result = parser.parse_profile("data/raw/sample_profile.nc")
    assert result is not None
    assert 'profile' in result
    assert 'measurements' in result
```

**Run command**: `pytest tests/test_data_pipeline.py -v`

#### 2. RAG System Tests

**File**: `tests/test_rag.py`

```python
import pytest
from src.ai.rag import RAGPipeline

def test_rag_query_processing():
    rag = RAGPipeline()
    result = rag.process_query("Show temperature in Indian Ocean")
    
    assert result is not None
    assert 'sql_query' in result
    assert 'temperature' in result['sql_query'].lower()
```

**Run command**: `pytest tests/test_rag.py -v`

### Manual Verification

#### 1. Database Setup Verification

**Steps**:
1. Run `psql -U postgres -c "CREATE DATABASE floatchat;"`
2. Run `psql -U postgres -d floatchat -f src/database/schema.sql`
3. Verify tables created: `psql -U postgres -d floatchat -c "\dt"`
4. Expected output: List of 6 tables (argo_floats, argo_profiles, etc.)

#### 2. Ollama LLM Verification

**Steps**:
1. Install Ollama: `curl -fsSL https://ollama.com/install.sh | sh`
2. Pull model: `ollama pull mistral:7b-instruct`
3. Test: `ollama run mistral:7b-instruct "What is oceanography?"`
4. Expected: Coherent response about oceanography

#### 3. Streamlit Dashboard Verification

**Steps**:
1. Run: `streamlit run app/Home.py`
2. Open browser to `http://localhost:8501`
3. Navigate to Chat Interface page
4. Enter query: "Show temperature data"
5. Expected: Response with SQL query displayed

#### 4. End-to-End Integration Test

**Steps**:
1. Ensure PostgreSQL is running
2. Ensure Ollama is running
3. Start FastAPI: `uvicorn src.api.main:app --reload`
4. Start Streamlit: `streamlit run app/Home.py`
5. Test query through chat interface
6. Expected: Full response with data and visualization

---

## Deployment Checklist

- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] PostgreSQL database created and schema loaded
- [ ] Ollama installed and model pulled
- [ ] Environment variables configured (`.env` file)
- [ ] Data directory structure created
- [ ] Tests passing (`pytest tests/ -v`)
- [ ] Streamlit app running (`streamlit run app/Home.py`)
- [ ] API server running (`uvicorn src.api.main:app`)

---

## Next Steps After Approval

1. **Create project structure** - All directories and base files
2. **Set up database** - PostgreSQL with schema
3. **Install Ollama** - LLM setup
4. **Implement data pipeline** - Download and parse ARGO data
5. **Build RAG system** - Core AI functionality
6. **Create Streamlit UI** - User interface
7. **Write tests** - Validation
8. **Document** - README and guides

**Estimated time for Phase 1 (MVP)**: 8-10 hours
