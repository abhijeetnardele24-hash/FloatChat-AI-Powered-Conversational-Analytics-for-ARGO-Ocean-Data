-- ============================================
-- FloatChat Ultra - PostgreSQL Database Schema
-- ============================================
-- Version: 1.0.0
-- Description: Complete schema for ARGO ocean data storage
-- Requires: PostgreSQL 15+ with PostGIS extension

-- ============================================
-- Enable Required Extensions
-- ============================================
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- ARGO Floats Table
-- Stores metadata about individual ARGO floats
-- ============================================
CREATE TABLE IF NOT EXISTS argo_floats (
    float_id SERIAL PRIMARY KEY,
    platform_number VARCHAR(20) UNIQUE NOT NULL,
    wmo_number VARCHAR(20),
    platform_type VARCHAR(50),
    manufacturer VARCHAR(100),
    deployment_date TIMESTAMP,
    deployment_location GEOGRAPHY(POINT, 4326),
    status VARCHAR(20) CHECK (status IN ('ACTIVE', 'INACTIVE', 'LOST', 'UNKNOWN')),
    last_update TIMESTAMP DEFAULT NOW(),
    metadata_json JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for argo_floats
CREATE INDEX IF NOT EXISTS idx_floats_platform_number ON argo_floats(platform_number);
CREATE INDEX IF NOT EXISTS idx_floats_wmo_number ON argo_floats(wmo_number);
CREATE INDEX IF NOT EXISTS idx_floats_status ON argo_floats(status);
CREATE INDEX IF NOT EXISTS idx_floats_deployment_location ON argo_floats USING GIST(deployment_location);
CREATE INDEX IF NOT EXISTS idx_floats_deployment_date ON argo_floats(deployment_date);

-- ============================================
-- ARGO Profiles Table
-- Stores individual profile measurements
-- ============================================
CREATE TABLE IF NOT EXISTS argo_profiles (
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
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (float_id, cycle_number)
);

-- Indexes for argo_profiles
CREATE INDEX IF NOT EXISTS idx_profiles_float_id ON argo_profiles(float_id);
CREATE INDEX IF NOT EXISTS idx_profiles_datetime ON argo_profiles(profile_datetime);
CREATE INDEX IF NOT EXISTS idx_profiles_location ON argo_profiles USING GIST(location);
CREATE INDEX IF NOT EXISTS idx_profiles_h3_res7 ON argo_profiles(h3_index_res7);
CREATE INDEX IF NOT EXISTS idx_profiles_h3_res5 ON argo_profiles(h3_index_res5);
CREATE INDEX IF NOT EXISTS idx_profiles_float_cycle ON argo_profiles(float_id, cycle_number);
CREATE INDEX IF NOT EXISTS idx_profiles_lat_lon ON argo_profiles(latitude, longitude);

-- ============================================
-- ARGO Measurements Table
-- Stores individual depth measurements
-- ============================================
CREATE TABLE IF NOT EXISTS argo_measurements (
    measurement_id BIGSERIAL PRIMARY KEY,
    profile_id BIGINT REFERENCES argo_profiles(profile_id) ON DELETE CASCADE,
    pressure DECIMAL(8,2) NOT NULL,
    depth DECIMAL(8,2),
    temperature DECIMAL(6,3),
    temperature_qc INTEGER,
    salinity DECIMAL(7,4),
    salinity_qc INTEGER,
    temperature_adjusted DECIMAL(6,3),
    salinity_adjusted DECIMAL(7,4),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for argo_measurements
CREATE INDEX IF NOT EXISTS idx_measurements_profile_id ON argo_measurements(profile_id);
CREATE INDEX IF NOT EXISTS idx_measurements_profile_pressure ON argo_measurements(profile_id, pressure);
CREATE INDEX IF NOT EXISTS idx_measurements_temp_range ON argo_measurements(temperature) WHERE temperature IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_measurements_salinity_range ON argo_measurements(salinity) WHERE salinity IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_measurements_depth ON argo_measurements(depth) WHERE depth IS NOT NULL;

-- ============================================
-- ARGO Ocean Properties Table
-- Stores derived oceanographic properties
-- ============================================
CREATE TABLE IF NOT EXISTS argo_ocean_properties (
    property_id BIGSERIAL PRIMARY KEY,
    measurement_id BIGINT REFERENCES argo_measurements(measurement_id) ON DELETE CASCADE,
    profile_id BIGINT REFERENCES argo_profiles(profile_id) ON DELETE CASCADE,
    potential_temperature DECIMAL(6,3),
    potential_density DECIMAL(8,4),
    sigma_theta DECIMAL(8,4),
    buoyancy_frequency DECIMAL(12,8),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for argo_ocean_properties
CREATE INDEX IF NOT EXISTS idx_properties_measurement_id ON argo_ocean_properties(measurement_id);
CREATE INDEX IF NOT EXISTS idx_properties_profile_id ON argo_ocean_properties(profile_id);

-- ============================================
-- ARGO Profile Summaries Table
-- Stores aggregated profile statistics
-- ============================================
CREATE TABLE IF NOT EXISTS argo_summaries (
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
    profile_quality_score DECIMAL(3,2) CHECK (profile_quality_score BETWEEN 0 AND 1),
    measurement_count INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for argo_summaries
CREATE INDEX IF NOT EXISTS idx_summaries_profile_id ON argo_summaries(profile_id);
CREATE INDEX IF NOT EXISTS idx_summaries_surface_temp ON argo_summaries(surface_temperature);
CREATE INDEX IF NOT EXISTS idx_summaries_surface_sal ON argo_summaries(surface_salinity);

-- ============================================
-- Ocean Regions Table
-- Stores predefined ocean regions for spatial queries
-- ============================================
CREATE TABLE IF NOT EXISTS ocean_regions (
    region_id SERIAL PRIMARY KEY,
    region_name VARCHAR(100) UNIQUE NOT NULL,
    region_type VARCHAR(50),
    boundary GEOGRAPHY(POLYGON, 4326),
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for ocean_regions
CREATE INDEX IF NOT EXISTS idx_regions_name ON ocean_regions(region_name);
CREATE INDEX IF NOT EXISTS idx_regions_boundary ON ocean_regions USING GIST(boundary);

-- ============================================
-- Insert Predefined Ocean Regions
-- ============================================
INSERT INTO ocean_regions (region_name, region_type, boundary, description) VALUES
(
    'Indian Ocean',
    'Basin',
    ST_GeogFromText('POLYGON((20 -40, 20 30, 120 30, 120 -40, 20 -40))'),
    'Indian Ocean basin - primary area of interest'
),
(
    'Arabian Sea',
    'Sea',
    ST_GeogFromText('POLYGON((50 10, 50 25, 75 25, 75 10, 50 10))'),
    'Arabian Sea - northwestern Indian Ocean'
),
(
    'Bay of Bengal',
    'Sea',
    ST_GeogFromText('POLYGON((80 5, 80 22, 95 22, 95 5, 80 5))'),
    'Bay of Bengal - northeastern Indian Ocean'
),
(
    'Southern Indian Ocean',
    'Region',
    ST_GeogFromText('POLYGON((20 -40, 20 -20, 120 -20, 120 -40, 20 -40))'),
    'Southern Indian Ocean region'
)
ON CONFLICT (region_name) DO NOTHING;

-- ============================================
-- Materialized Views for Performance
-- ============================================

-- Float statistics view
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_float_statistics AS
SELECT 
    f.status,
    COUNT(DISTINCT f.float_id) as float_count,
    COUNT(DISTINCT p.profile_id) as total_profiles,
    MAX(p.profile_datetime) as latest_profile,
    MIN(p.profile_datetime) as earliest_profile,
    AVG(s.profile_quality_score) as avg_quality_score
FROM argo_floats f
LEFT JOIN argo_profiles p ON f.float_id = p.float_id
LEFT JOIN argo_summaries s ON p.profile_id = s.profile_id
GROUP BY f.status;

CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_float_stats_status ON mv_float_statistics(status);

-- Regional statistics view
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_regional_statistics AS
SELECT 
    r.region_name,
    COUNT(DISTINCT p.profile_id) as profile_count,
    COUNT(DISTINCT p.float_id) as float_count,
    AVG(s.surface_temperature) as avg_surface_temp,
    AVG(s.surface_salinity) as avg_surface_salinity,
    MIN(p.profile_datetime) as earliest_date,
    MAX(p.profile_datetime) as latest_date
FROM ocean_regions r
LEFT JOIN argo_profiles p ON ST_Contains(r.boundary, p.location)
LEFT JOIN argo_summaries s ON p.profile_id = s.profile_id
GROUP BY r.region_name;

CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_regional_stats_name ON mv_regional_statistics(region_name);

-- ============================================
-- Functions and Triggers
-- ============================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for updated_at
CREATE TRIGGER update_argo_floats_updated_at
    BEFORE UPDATE ON argo_floats
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_argo_profiles_updated_at
    BEFORE UPDATE ON argo_profiles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_argo_summaries_updated_at
    BEFORE UPDATE ON argo_summaries
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Function to automatically set location from lat/lon
CREATE OR REPLACE FUNCTION set_location_from_lat_lon()
RETURNS TRIGGER AS $$
BEGIN
    NEW.location = ST_SetSRID(ST_MakePoint(NEW.longitude, NEW.latitude), 4326)::geography;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to set location
CREATE TRIGGER set_profile_location
    BEFORE INSERT OR UPDATE ON argo_profiles
    FOR EACH ROW
    EXECUTE FUNCTION set_location_from_lat_lon();

-- ============================================
-- Grants and Permissions
-- ============================================
-- Grant permissions to floatchat_user (will be created separately)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO floatchat_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO floatchat_user;

-- ============================================
-- Comments for Documentation
-- ============================================
COMMENT ON TABLE argo_floats IS 'ARGO float metadata and deployment information';
COMMENT ON TABLE argo_profiles IS 'Individual ARGO profile measurements with location and time';
COMMENT ON TABLE argo_measurements IS 'Depth-resolved temperature and salinity measurements';
COMMENT ON TABLE argo_ocean_properties IS 'Derived oceanographic properties (TEOS-10)';
COMMENT ON TABLE argo_summaries IS 'Aggregated statistics for each profile';
COMMENT ON TABLE ocean_regions IS 'Predefined ocean regions for spatial queries';

-- ============================================
-- Schema Version Tracking
-- ============================================
CREATE TABLE IF NOT EXISTS schema_version (
    version VARCHAR(10) PRIMARY KEY,
    applied_at TIMESTAMP DEFAULT NOW(),
    description TEXT
);

INSERT INTO schema_version (version, description) VALUES
('1.0.0', 'Initial schema with ARGO floats, profiles, measurements, and regions')
ON CONFLICT (version) DO NOTHING;

-- ============================================
-- End of Schema
-- ============================================
