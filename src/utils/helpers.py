"""
Helper utility functions for FloatChat Ultra
"""

from typing import Any, Dict, List, Optional
import hashlib
import json
from datetime import datetime


def generate_hash(data: str) -> str:
    """
    Generate SHA256 hash of string data
    
    Args:
        data: String to hash
    
    Returns:
        Hexadecimal hash string
    """
    return hashlib.sha256(data.encode()).hexdigest()


def sanitize_sql(sql: str) -> str:
    """
    Basic SQL sanitization to prevent injection
    
    Args:
        sql: SQL query string
    
    Returns:
        Sanitized SQL string
    
    Raises:
        ValueError: If dangerous SQL keywords detected
    """
    # List of forbidden keywords
    forbidden = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'TRUNCATE', 'EXEC', 'EXECUTE']
    
    sql_upper = sql.upper()
    for keyword in forbidden:
        if keyword in sql_upper:
            raise ValueError(f"Forbidden SQL keyword detected: {keyword}")
    
    return sql.strip()


def format_timestamp(dt: datetime) -> str:
    """
    Format datetime to ISO string
    
    Args:
        dt: Datetime object
    
    Returns:
        ISO formatted string
    """
    return dt.isoformat()


def parse_timestamp(timestamp_str: str) -> datetime:
    """
    Parse ISO timestamp string to datetime
    
    Args:
        timestamp_str: ISO formatted timestamp string
    
    Returns:
        Datetime object
    """
    return datetime.fromisoformat(timestamp_str)


def dict_to_json(data: Dict[str, Any]) -> str:
    """
    Convert dictionary to JSON string
    
    Args:
        data: Dictionary to convert
    
    Returns:
        JSON string
    """
    return json.dumps(data, indent=2, default=str)


def json_to_dict(json_str: str) -> Dict[str, Any]:
    """
    Convert JSON string to dictionary
    
    Args:
        json_str: JSON string
    
    Returns:
        Dictionary
    """
    return json.loads(json_str)


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
    
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def validate_lat_lon(latitude: float, longitude: float) -> bool:
    """
    Validate latitude and longitude values
    
    Args:
        latitude: Latitude value
        longitude: Longitude value
    
    Returns:
        True if valid, False otherwise
    """
    return -90 <= latitude <= 90 and -180 <= longitude <= 180


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate great circle distance between two points (Haversine formula)
    
    Args:
        lat1, lon1: First point coordinates
        lat2, lon2: Second point coordinates
    
    Returns:
        Distance in kilometers
    """
    from math import radians, sin, cos, sqrt, atan2
    
    R = 6371  # Earth's radius in kilometers
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    return R * c
