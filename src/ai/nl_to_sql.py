"""
Natural Language to SQL Converter
Uses Ollama + Mistral to convert natural language questions to SQL queries
Implements few-shot learning with example queries
"""

import requests
import json
from loguru import logger
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.config import settings
from src.ai.query_examples import QUERY_EXAMPLES, format_examples_for_prompt, OCEAN_REGIONS, METRICS


class NLToSQLConverter:
    """Convert natural language questions to SQL queries using Ollama"""
    
    def __init__(self):
        self.ollama_url = settings.ollama_base_url
        self.model = settings.ollama_model
        self.temperature = settings.ollama_temperature
        
    def _create_prompt(self, question):
        """Create few-shot learning prompt for SQL generation"""
        
        system_prompt = """You are an expert SQL query generator for an ARGO ocean database.

DATABASE SCHEMA:
- argo_floats: float_id, platform_type, status
- argo_profiles: profile_id, float_id, latitude, longitude, location (PostGIS), date, ocean_region, n_levels
- argo_measurements: profile_id, level, pressure, temperature, salinity, temperature_qc, salinity_qc, pressure_qc

OCEAN REGIONS:
- Pacific Ocean
- Atlantic Ocean
- Indian Ocean
- Southern Ocean
- Arctic Ocean

QUALITY CONTROL:
- QC flag '1' = good data
- Always filter by QC flags for accurate results

IMPORTANT RULES:
1. Always JOIN argo_profiles and argo_measurements when querying measurements
2. Always filter by QC flags (temperature_qc = '1', salinity_qc = '1')
3. Use ocean_region column for region filtering
4. Pressure in dbar ≈ depth in meters
5. Return only the SQL query, no explanations

EXAMPLE QUERIES:
"""
        
        # Add few-shot examples
        examples = format_examples_for_prompt()
        
        user_prompt = f"""
{system_prompt}
{examples}

Now generate SQL for this question:
Question: {question}
SQL:"""
        
        return user_prompt
    
    def generate_sql(self, question):
        """Generate SQL query from natural language question"""
        try:
            logger.info(f"Generating SQL for: {question}")
            
            # Create prompt
            prompt = self._create_prompt(question)
            
            # Call Ollama API
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "temperature": self.temperature,
                    "stream": False
                },
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extract SQL from response
            sql = result.get("response", "").strip()
            
            # Clean up SQL
            sql = self._clean_sql(sql)
            
            logger.success(f"Generated SQL: {sql[:100]}...")
            
            return {
                "success": True,
                "sql": sql,
                "question": question,
                "error": None
            }
            
        except Exception as e:
            logger.error(f"Failed to generate SQL: {e}")
            return {
                "success": False,
                "sql": None,
                "question": question,
                "error": str(e)
            }
    
    def _clean_sql(self, sql):
        """Clean and validate SQL query"""
        # Remove markdown code blocks if present
        if "```sql" in sql:
            sql = sql.split("```sql")[1].split("```")[0]
        elif "```" in sql:
            sql = sql.split("```")[1].split("```")[0]
        
        # Remove extra whitespace
        sql = " ".join(sql.split())
        
        # Ensure it ends with semicolon
        if not sql.endswith(";"):
            sql += ";"
        
        return sql.strip()
    
    def validate_sql(self, sql):
        """Basic SQL validation"""
        # Check for dangerous operations
        dangerous_keywords = ["DROP", "DELETE", "TRUNCATE", "UPDATE", "INSERT", "ALTER"]
        sql_upper = sql.upper()
        
        for keyword in dangerous_keywords:
            if keyword in sql_upper:
                logger.warning(f"Dangerous SQL keyword detected: {keyword}")
                return False
        
        # Check for required SELECT
        if not sql_upper.startswith("SELECT"):
            logger.warning("SQL must start with SELECT")
            return False
        
        return True
    
    def explain_query(self, question, sql):
        """Generate natural language explanation of SQL query"""
        try:
            prompt = f"""Explain this SQL query in simple terms:

Question: {question}
SQL: {sql}

Provide a brief, user-friendly explanation of what this query does."""
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "temperature": 0.3,
                    "stream": False
                },
                timeout=20
            )
            
            response.raise_for_status()
            result = response.json()
            explanation = result.get("response", "").strip()
            
            return explanation
            
        except Exception as e:
            logger.error(f"Failed to generate explanation: {e}")
            return "Query explanation unavailable"


def test_converter():
    """Test the NL to SQL converter"""
    converter = NLToSQLConverter()
    
    test_questions = [
        "What is the average temperature in the Pacific Ocean?",
        "Show me all floats in the Indian Ocean",
        "Compare salinity between Atlantic and Pacific",
        "What was the temperature in summer 2023?",
        "How many profiles were collected in 2022?"
    ]
    
    logger.info("Testing NL to SQL Converter...")
    logger.info("="*60)
    
    for question in test_questions:
        logger.info(f"\nQuestion: {question}")
        result = converter.generate_sql(question)
        
        if result["success"]:
            logger.success(f"SQL: {result['sql']}")
            
            # Validate
            is_valid = converter.validate_sql(result['sql'])
            logger.info(f"Valid: {is_valid}")
            
            # Explain
            explanation = converter.explain_query(question, result['sql'])
            logger.info(f"Explanation: {explanation}")
        else:
            logger.error(f"Error: {result['error']}")
        
        logger.info("-"*60)


if __name__ == "__main__":
    test_converter()
