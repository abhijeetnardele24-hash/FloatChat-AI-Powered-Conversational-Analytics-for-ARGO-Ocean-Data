"""
Query Examples for Few-Shot Learning
Provides example natural language queries and their SQL translations
Used to train the NL-to-SQL converter
"""

# Example queries for RAG few-shot learning
QUERY_EXAMPLES = [
    {
        "question": "What is the average temperature in the Pacific Ocean?",
        "intent": "statistical_query",
        "region": "Pacific Ocean",
        "metric": "temperature",
        "aggregation": "average",
        "sql": """
            SELECT AVG(m.temperature) as avg_temp
            FROM argo_profiles p
            JOIN argo_measurements m ON p.profile_id = m.profile_id
            WHERE p.ocean_region = 'Pacific Ocean'
              AND m.temperature IS NOT NULL
              AND m.temperature_qc = '1';
        """,
        "explanation": "Calculate average temperature from all measurements in Pacific Ocean with good quality control"
    },
    {
        "question": "Show me all floats in the Indian Ocean",
        "intent": "data_retrieval",
        "region": "Indian Ocean",
        "sql": """
            SELECT DISTINCT f.float_id, COUNT(p.profile_id) as profile_count
            FROM argo_floats f
            JOIN argo_profiles p ON f.float_id = p.float_id
            WHERE p.ocean_region = 'Indian Ocean'
            GROUP BY f.float_id
            ORDER BY profile_count DESC;
        """,
        "explanation": "List all unique floats that have profiles in the Indian Ocean"
    },
    {
        "question": "What was the temperature in summer 2023?",
        "intent": "temporal_query",
        "time_period": "summer 2023",
        "metric": "temperature",
        "sql": """
            SELECT AVG(m.temperature) as avg_temp,
                   MIN(m.temperature) as min_temp,
                   MAX(m.temperature) as max_temp,
                   COUNT(*) as measurement_count
            FROM argo_profiles p
            JOIN argo_measurements m ON p.profile_id = m.profile_id
            WHERE EXTRACT(YEAR FROM p.date) = 2023
              AND EXTRACT(MONTH FROM p.date) IN (6, 7, 8)
              AND m.temperature IS NOT NULL
              AND m.temperature_qc = '1';
        """,
        "explanation": "Calculate temperature statistics for summer months (June, July, August) in 2023"
    },
    {
        "question": "Compare salinity between Atlantic and Pacific",
        "intent": "comparison_query",
        "regions": ["Atlantic Ocean", "Pacific Ocean"],
        "metric": "salinity",
        "sql": """
            SELECT 
                p.ocean_region,
                AVG(m.salinity) as avg_salinity,
                STDDEV(m.salinity) as std_salinity,
                COUNT(*) as measurement_count
            FROM argo_profiles p
            JOIN argo_measurements m ON p.profile_id = m.profile_id
            WHERE p.ocean_region IN ('Atlantic Ocean', 'Pacific Ocean')
              AND m.salinity IS NOT NULL
              AND m.salinity_qc = '1'
            GROUP BY p.ocean_region;
        """,
        "explanation": "Compare average salinity and standard deviation between Atlantic and Pacific oceans"
    },
    {
        "question": "Show temperature at 1000m depth",
        "intent": "depth_query",
        "depth": 1000,
        "metric": "temperature",
        "sql": """
            SELECT 
                p.ocean_region,
                AVG(m.temperature) as avg_temp,
                COUNT(*) as measurement_count
            FROM argo_profiles p
            JOIN argo_measurements m ON p.profile_id = m.profile_id
            WHERE m.pressure BETWEEN 950 AND 1050
              AND m.temperature IS NOT NULL
              AND m.temperature_qc = '1'
            GROUP BY p.ocean_region
            ORDER BY avg_temp DESC;
        """,
        "explanation": "Find average temperature at approximately 1000m depth (950-1050 dbar pressure) by ocean region"
    },
    {
        "question": "How many profiles were collected in 2023?",
        "intent": "count_query",
        "time_period": "2023",
        "sql": """
            SELECT 
                COUNT(*) as total_profiles,
                COUNT(DISTINCT float_id) as unique_floats,
                ocean_region
            FROM argo_profiles
            WHERE EXTRACT(YEAR FROM date) = 2023
            GROUP BY ocean_region
            ORDER BY total_profiles DESC;
        """,
        "explanation": "Count total profiles and unique floats collected in 2023, grouped by ocean region"
    },
    {
        "question": "Find the warmest location in the database",
        "intent": "extrema_query",
        "metric": "temperature",
        "extrema": "max",
        "sql": """
            SELECT 
                p.profile_id,
                p.latitude,
                p.longitude,
                p.date,
                p.ocean_region,
                m.temperature,
                m.pressure
            FROM argo_profiles p
            JOIN argo_measurements m ON p.profile_id = m.profile_id
            WHERE m.temperature_qc = '1'
            ORDER BY m.temperature DESC
            LIMIT 1;
        """,
        "explanation": "Find the single warmest temperature measurement with its location and depth"
    },
    {
        "question": "Show temperature trends from 2018 to 2024",
        "intent": "trend_query",
        "time_range": "2018-2024",
        "metric": "temperature",
        "sql": """
            SELECT 
                EXTRACT(YEAR FROM p.date) as year,
                AVG(m.temperature) as avg_temp,
                COUNT(*) as measurement_count
            FROM argo_profiles p
            JOIN argo_measurements m ON p.profile_id = m.profile_id
            WHERE m.temperature IS NOT NULL
              AND m.temperature_qc = '1'
            GROUP BY EXTRACT(YEAR FROM p.date)
            ORDER BY year;
        """,
        "explanation": "Calculate yearly average temperature from 2018 to 2024 to show trends"
    },
    {
        "question": "What's the salinity range in the Arctic Ocean?",
        "intent": "range_query",
        "region": "Arctic Ocean",
        "metric": "salinity",
        "sql": """
            SELECT 
                MIN(m.salinity) as min_salinity,
                MAX(m.salinity) as max_salinity,
                AVG(m.salinity) as avg_salinity,
                STDDEV(m.salinity) as std_salinity,
                COUNT(*) as measurement_count
            FROM argo_profiles p
            JOIN argo_measurements m ON p.profile_id = m.profile_id
            WHERE p.ocean_region = 'Arctic Ocean'
              AND m.salinity IS NOT NULL
              AND m.salinity_qc = '1';
        """,
        "explanation": "Calculate salinity statistics (min, max, average, standard deviation) for Arctic Ocean"
    },
    {
        "question": "Show me profiles deeper than 1500 meters",
        "intent": "depth_filter",
        "depth_threshold": 1500,
        "sql": """
            SELECT 
                p.profile_id,
                p.float_id,
                p.latitude,
                p.longitude,
                p.date,
                p.ocean_region,
                MAX(m.pressure) as max_depth
            FROM argo_profiles p
            JOIN argo_measurements m ON p.profile_id = m.profile_id
            GROUP BY p.profile_id, p.float_id, p.latitude, p.longitude, p.date, p.ocean_region
            HAVING MAX(m.pressure) > 1500
            ORDER BY max_depth DESC
            LIMIT 100;
        """,
        "explanation": "Find profiles that reach deeper than 1500 dbar (approximately 1500m)"
    }
]

# Ocean region definitions
OCEAN_REGIONS = {
    "Pacific Ocean": {
        "description": "Largest ocean, between Asia/Australia and Americas",
        "bounds": "120°E to 70°W, 60°S to 60°N",
        "characteristics": "Deepest ocean, contains Mariana Trench"
    },
    "Atlantic Ocean": {
        "description": "Second largest ocean, between Americas and Europe/Africa",
        "bounds": "70°W to 20°E, 60°S to 60°N",
        "characteristics": "Important for global ocean circulation"
    },
    "Indian Ocean": {
        "description": "Third largest ocean, south of Asia",
        "bounds": "20°E to 120°E, 40°S to 30°N",
        "characteristics": "Warmest ocean, monsoon influence"
    },
    "Southern Ocean": {
        "description": "Ocean surrounding Antarctica",
        "bounds": "All longitudes, south of 60°S",
        "characteristics": "Coldest ocean, Antarctic Circumpolar Current"
    },
    "Arctic Ocean": {
        "description": "Smallest ocean, around North Pole",
        "bounds": "All longitudes, north of 60°N",
        "characteristics": "Ice-covered, coldest temperatures"
    }
}

# Common query patterns
QUERY_PATTERNS = {
    "average": ["average", "mean", "avg"],
    "maximum": ["maximum", "max", "highest", "warmest", "hottest"],
    "minimum": ["minimum", "min", "lowest", "coldest"],
    "count": ["how many", "count", "number of"],
    "compare": ["compare", "difference", "versus", "vs", "between"],
    "trend": ["trend", "change", "over time", "from", "to"],
    "range": ["range", "between", "from", "to"],
    "location": ["where", "location", "region", "area"],
    "time": ["when", "date", "year", "month", "season"]
}

# Metric mappings
METRICS = {
    "temperature": {
        "column": "temperature",
        "unit": "°C",
        "table": "argo_measurements",
        "qc_column": "temperature_qc"
    },
    "salinity": {
        "column": "salinity",
        "unit": "PSU",
        "table": "argo_measurements",
        "qc_column": "salinity_qc"
    },
    "pressure": {
        "column": "pressure",
        "unit": "dbar",
        "table": "argo_measurements",
        "qc_column": "pressure_qc",
        "note": "Pressure in decibars, approximately equal to depth in meters"
    }
}

# Time period mappings
TIME_PERIODS = {
    "summer": [6, 7, 8],
    "winter": [12, 1, 2],
    "spring": [3, 4, 5],
    "fall": [9, 10, 11],
    "autumn": [9, 10, 11]
}


def get_example_by_intent(intent):
    """Get example queries by intent type"""
    return [ex for ex in QUERY_EXAMPLES if ex["intent"] == intent]


def get_all_intents():
    """Get list of all intent types"""
    return list(set(ex["intent"] for ex in QUERY_EXAMPLES))


def format_examples_for_prompt():
    """Format examples for few-shot learning prompt"""
    formatted = []
    for ex in QUERY_EXAMPLES[:5]:  # Use first 5 examples
        formatted.append(f"""
Question: {ex['question']}
SQL: {ex['sql'].strip()}
""")
    return "\n".join(formatted)
