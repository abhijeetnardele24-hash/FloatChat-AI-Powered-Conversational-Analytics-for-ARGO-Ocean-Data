"""
RAG (Retrieval-Augmented Generation) Query Engine
Main engine that processes user questions and generates intelligent responses
Combines: ChromaDB retrieval + Ollama LLM + PostgreSQL queries
"""

import requests
import json
from loguru import logger
import sys
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.config import settings
from src.database.connection import get_db_engine
from src.ai.nl_to_sql import NLToSQLConverter
from src.ai.query_examples import OCEAN_REGIONS, METRICS


class RAGQueryEngine:
    """Main RAG engine for intelligent query processing"""
    
    def __init__(self):
        self.ollama_url = settings.ollama_base_url
        self.model = settings.ollama_model
        self.nl_to_sql = NLToSQLConverter()
        self.db_engine = get_db_engine()
        
    def process_question(self, question):
        """
        Main entry point: Process a natural language question
        Returns a complete response with data and natural language answer
        """
        logger.info(f"Processing question: {question}")
        
        try:
            # Step 1: Generate SQL query
            sql_result = self.nl_to_sql.generate_sql(question)
            
            if not sql_result["success"]:
                return {
                    "success": False,
                    "error": "Failed to generate SQL query",
                    "details": sql_result["error"]
                }
            
            sql_query = sql_result["sql"]
            
            # Step 2: Validate SQL
            if not self.nl_to_sql.validate_sql(sql_query):
                return {
                    "success": False,
                    "error": "Generated SQL query failed validation",
                    "sql": sql_query
                }
            
            # Step 3: Execute SQL query
            query_result = self._execute_query(sql_query)
            
            if not query_result["success"]:
                return {
                    "success": False,
                    "error": "Failed to execute SQL query",
                    "sql": sql_query,
                    "details": query_result["error"]
                }
            
            # Step 4: Generate natural language response
            nl_response = self._generate_response(
                question=question,
                sql=sql_query,
                data=query_result["data"]
            )
            
            # Step 5: Return complete result
            return {
                "success": True,
                "question": question,
                "sql": sql_query,
                "data": query_result["data"],
                "response": nl_response,
                "row_count": query_result["row_count"]
            }
            
        except Exception as e:
            logger.error(f"Error processing question: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _execute_query(self, sql):
        """Execute SQL query on PostgreSQL database"""
        try:
            logger.info("Executing SQL query...")
            
            # Execute query
            with self.db_engine.connect() as conn:
                result = conn.execute(text(sql))
                
                # Fetch results
                rows = result.fetchall()
                columns = result.keys()
                
                # Convert to list of dicts
                data = [dict(zip(columns, row)) for row in rows]
                
                logger.success(f"Query executed successfully: {len(data)} rows")
                
                return {
                    "success": True,
                    "data": data,
                    "row_count": len(data),
                    "columns": list(columns),
                    "error": None
                }
                
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            return {
                "success": False,
                "data": None,
                "row_count": 0,
                "error": str(e)
            }
    
    def _generate_response(self, question, sql, data):
        """Generate natural language response from query results"""
        try:
            logger.info("Generating natural language response...")
            
            # Format data summary
            data_summary = self._format_data_summary(data)
            
            # Create prompt for response generation
            prompt = f"""You are FloatChat, an AI assistant for ARGO ocean data.

User Question: {question}

SQL Query Executed: {sql}

Query Results Summary:
{data_summary}

Generate a clear, concise, and informative response to the user's question based on the query results.
Include specific numbers and insights from the data.
Be conversational and helpful.
If the results show interesting patterns or trends, mention them.

Response:"""
            
            # Call Ollama
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "temperature": 0.3,
                    "stream": False
                },
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            nl_response = result.get("response", "").strip()
            
            logger.success("Natural language response generated")
            
            return nl_response
            
        except Exception as e:
            logger.error(f"Failed to generate response: {e}")
            return f"I found {len(data)} results for your query, but couldn't generate a detailed response."
    
    def _format_data_summary(self, data):
        """Format query results into a readable summary"""
        if not data:
            return "No results found."
        
        summary = f"Found {len(data)} result(s).\n\n"
        
        # Show first few rows
        max_rows = min(5, len(data))
        for i, row in enumerate(data[:max_rows]):
            summary += f"Row {i+1}: {row}\n"
        
        if len(data) > max_rows:
            summary += f"\n... and {len(data) - max_rows} more rows"
        
        return summary
    
    def get_database_stats(self):
        """Get database statistics for context"""
        try:
            stats = {}
            
            with self.db_engine.connect() as conn:
                # Count floats
                result = conn.execute(text("SELECT COUNT(*) FROM argo_floats"))
                stats["float_count"] = result.scalar()
                
                # Count profiles
                result = conn.execute(text("SELECT COUNT(*) FROM argo_profiles"))
                stats["profile_count"] = result.scalar()
                
                # Count measurements
                result = conn.execute(text("SELECT COUNT(*) FROM argo_measurements"))
                stats["measurement_count"] = result.scalar()
                
                # Date range
                result = conn.execute(text("""
                    SELECT MIN(date), MAX(date) FROM argo_profiles
                """))
                min_date, max_date = result.fetchone()
                stats["date_range"] = f"{min_date} to {max_date}"
                
                # Regions
                result = conn.execute(text("""
                    SELECT ocean_region, COUNT(*) as count
                    FROM argo_profiles
                    GROUP BY ocean_region
                    ORDER BY count DESC
                """))
                stats["regions"] = dict(result.fetchall())
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get database stats: {e}")
            return {}
    
    def chat(self, message):
        """
        Simple chat interface
        Handles greetings, help requests, and questions
        """
        message_lower = message.lower().strip()
        
        # Handle greetings
        if any(word in message_lower for word in ["hi", "hello", "hey"]):
            stats = self.get_database_stats()
            return f"""Hello! I'm FloatChat, your AI assistant for ARGO ocean data.

I have access to:
- {stats.get('float_count', 'N/A'):,} ARGO floats
- {stats.get('profile_count', 'N/A'):,} ocean profiles
- {stats.get('measurement_count', 'N/A'):,} measurements
- Data from {stats.get('date_range', 'N/A')}
- Coverage: {', '.join(stats.get('regions', {}).keys())}

What would you like to know about ARGO ocean data?"""
        
        # Handle help requests
        if any(word in message_lower for word in ["help", "what can you do"]):
            return """I can help you explore ARGO ocean data! Here are some things you can ask:

📊 **Statistical Queries:**
- "What is the average temperature in the Pacific Ocean?"
- "Show me salinity statistics for the Indian Ocean"

🌍 **Regional Queries:**
- "Compare temperature between Atlantic and Pacific"
- "Show me all floats in the Southern Ocean"

📅 **Temporal Queries:**
- "What was the temperature in summer 2023?"
- "Show temperature trends from 2018 to 2024"

🔍 **Specific Queries:**
- "Find the warmest location in the database"
- "Show me profiles deeper than 1500 meters"

Just ask your question in natural language!"""
        
        # Process as data question
        return self.process_question(message)


def test_rag_engine():
    """Test the RAG engine"""
    engine = RAGQueryEngine()
    
    test_questions = [
        "Hi",
        "What is the average temperature in the Pacific Ocean?",
        "How many profiles were collected in 2023?",
        "Compare salinity between Atlantic and Indian Ocean"
    ]
    
    logger.info("Testing RAG Query Engine...")
    logger.info("="*70)
    
    for question in test_questions:
        logger.info(f"\nUser: {question}")
        result = engine.chat(question)
        
        if isinstance(result, str):
            logger.info(f"FloatChat: {result}")
        elif result.get("success"):
            logger.info(f"FloatChat: {result['response']}")
            logger.info(f"Data rows: {result['row_count']}")
        else:
            logger.error(f"Error: {result.get('error')}")
        
        logger.info("-"*70)


if __name__ == "__main__":
    test_rag_engine()
