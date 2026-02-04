"""
SQLAlchemy ORM models for FloatChat database
Maps Python classes to PostgreSQL tables
"""

from sqlalchemy import (
    Column, Integer, String, DECIMAL, TIMESTAMP, ForeignKey,
    CheckConstraint, JSON, BigInteger, Text
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from geoalchemy2 import Geography
from datetime import datetime

Base = declarative_base()


class ArgoFloat(Base):
    """ARGO float metadata"""
    __tablename__ = 'argo_floats'
    
    float_id = Column(Integer, primary_key=True)
    platform_number = Column(String(20), unique=True, nullable=False)
    wmo_number = Column(String(20))
    platform_type = Column(String(50))
    manufacturer = Column(String(100))
    deployment_date = Column(TIMESTAMP)
    deployment_location = Column(Geography('POINT', srid=4326))
    status = Column(
        String(20),
        CheckConstraint("status IN ('ACTIVE', 'INACTIVE', 'LOST', 'UNKNOWN')")
    )
    last_update = Column(TIMESTAMP, default=datetime.now)
    metadata_json = Column(JSON)
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    profiles = relationship(
        "ArgoProfile",
        back_populates="float",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<ArgoFloat(platform_number='{self.platform_number}', status='{self.status}')>"


class ArgoProfile(Base):
    """Individual ARGO profile measurement"""
    __tablename__ = 'argo_profiles'
    
    profile_id = Column(BigInteger, primary_key=True)
    float_id = Column(Integer, ForeignKey('argo_floats.float_id', ondelete='CASCADE'))
    cycle_number = Column(Integer, nullable=False)
    profile_datetime = Column(TIMESTAMP, nullable=False)
    latitude = Column(DECIMAL(10, 7), nullable=False)
    longitude = Column(DECIMAL(10, 7), nullable=False)
    location = Column(Geography('POINT', srid=4326))
    position_qc = Column(Integer)
    vertical_sampling_scheme = Column(String(20))
    profile_type = Column(String(20))
    h3_index_res7 = Column(String(20))
    h3_index_res5 = Column(String(20))
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    float = relationship("ArgoFloat", back_populates="profiles")
    measurements = relationship(
        "ArgoMeasurement",
        back_populates="profile",
        cascade="all, delete-orphan"
    )
    summary = relationship(
        "ArgoSummary",
        back_populates="profile",
        uselist=False,
        cascade="all, delete-orphan"
    )
    ocean_properties = relationship(
        "ArgoOceanProperty",
        back_populates="profile",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<ArgoProfile(profile_id={self.profile_id}, float={self.float_id}, cycle={self.cycle_number})>"


class ArgoMeasurement(Base):
    """Depth-resolved temperature and salinity measurements"""
    __tablename__ = 'argo_measurements'
    
    measurement_id = Column(BigInteger, primary_key=True)
    profile_id = Column(
        BigInteger,
        ForeignKey('argo_profiles.profile_id', ondelete='CASCADE')
    )
    pressure = Column(DECIMAL(8, 2), nullable=False)
    depth = Column(DECIMAL(8, 2))
    temperature = Column(DECIMAL(6, 3))
    temperature_qc = Column(Integer)
    salinity = Column(DECIMAL(7, 4))
    salinity_qc = Column(Integer)
    temperature_adjusted = Column(DECIMAL(6, 3))
    salinity_adjusted = Column(DECIMAL(7, 4))
    created_at = Column(TIMESTAMP, default=datetime.now)
    
    # Relationships
    profile = relationship("ArgoProfile", back_populates="measurements")
    ocean_property = relationship(
        "ArgoOceanProperty",
        back_populates="measurement",
        uselist=False
    )
    
    def __repr__(self):
        return f"<ArgoMeasurement(id={self.measurement_id}, depth={self.depth}m, temp={self.temperature}°C)>"


class ArgoOceanProperty(Base):
    """Derived oceanographic properties (TEOS-10)"""
    __tablename__ = 'argo_ocean_properties'
    
    property_id = Column(BigInteger, primary_key=True)
    measurement_id = Column(
        BigInteger,
        ForeignKey('argo_measurements.measurement_id', ondelete='CASCADE')
    )
    profile_id = Column(
        BigInteger,
        ForeignKey('argo_profiles.profile_id', ondelete='CASCADE')
    )
    potential_temperature = Column(DECIMAL(6, 3))
    potential_density = Column(DECIMAL(8, 4))
    sigma_theta = Column(DECIMAL(8, 4))
    buoyancy_frequency = Column(DECIMAL(12, 8))
    created_at = Column(TIMESTAMP, default=datetime.now)
    
    # Relationships
    measurement = relationship("ArgoMeasurement", back_populates="ocean_property")
    profile = relationship("ArgoProfile", back_populates="ocean_properties")
    
    def __repr__(self):
        return f"<ArgoOceanProperty(id={self.property_id}, sigma_theta={self.sigma_theta})>"


class ArgoSummary(Base):
    """Aggregated profile statistics"""
    __tablename__ = 'argo_summaries'
    
    summary_id = Column(Integer, primary_key=True)
    profile_id = Column(
        BigInteger,
        ForeignKey('argo_profiles.profile_id', ondelete='CASCADE'),
        unique=True
    )
    mixed_layer_depth = Column(DECIMAL(7, 2))
    thermocline_depth = Column(DECIMAL(7, 2))
    max_depth = Column(DECIMAL(8, 2))
    surface_temperature = Column(DECIMAL(6, 3))
    surface_salinity = Column(DECIMAL(7, 4))
    mean_temperature = Column(DECIMAL(6, 3))
    mean_salinity = Column(DECIMAL(7, 4))
    temperature_range = Column(DECIMAL(6, 3))
    salinity_range = Column(DECIMAL(7, 4))
    profile_quality_score = Column(
        DECIMAL(3, 2),
        CheckConstraint("profile_quality_score BETWEEN 0 AND 1")
    )
    measurement_count = Column(Integer)
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    profile = relationship("ArgoProfile", back_populates="summary")
    
    def __repr__(self):
        return f"<ArgoSummary(profile_id={self.profile_id}, surface_temp={self.surface_temperature}°C)>"


class OceanRegion(Base):
    """Predefined ocean regions for spatial queries"""
    __tablename__ = 'ocean_regions'
    
    region_id = Column(Integer, primary_key=True)
    region_name = Column(String(100), unique=True, nullable=False)
    region_type = Column(String(50))
    boundary = Column(Geography('POLYGON', srid=4326))
    description = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.now)
    
    def __repr__(self):
        return f"<OceanRegion(name='{self.region_name}', type='{self.region_type}')>"


class SchemaVersion(Base):
    """Track database schema versions"""
    __tablename__ = 'schema_version'
    
    version = Column(String(10), primary_key=True)
    applied_at = Column(TIMESTAMP, default=datetime.now)
    description = Column(Text)
    
    def __repr__(self):
        return f"<SchemaVersion(version='{self.version}')>"
