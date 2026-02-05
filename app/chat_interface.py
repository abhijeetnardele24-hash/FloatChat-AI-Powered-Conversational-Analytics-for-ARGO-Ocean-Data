"""
FloatChat - Streamlit Chat Interface
AI-powered chatbot for ARGO ocean data exploration
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))
from src.ai.rag_engine import RAGQueryEngine
from src.utils.logger import setup_logger

# Setup logging
setup_logger()

# Page config
st.set_page_config(
    page_title="FloatChat - ARGO Ocean Data AI",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
    }
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #E3F2FD;
        border-left: 4px solid #1E88E5;
    }
    .assistant-message {
        background-color: #F5F5F5;
        border-left: 4px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# Initialize RAG engine
@st.cache_resource
def get_rag_engine():
    """Initialize and cache the RAG engine"""
    return RAGQueryEngine()


def display_stats(engine):
    """Display database statistics in sidebar"""
    st.sidebar.markdown("### 📊 Database Statistics")
    
    try:
        stats = engine.get_database_stats()
        
        st.sidebar.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{stats.get('float_count', 0):,}</div>
            <div class="stat-label">ARGO Floats</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.sidebar.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{stats.get('profile_count', 0):,}</div>
            <div class="stat-label">Ocean Profiles</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.sidebar.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{stats.get('measurement_count', 0):,}</div>
            <div class="stat-label">Measurements</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.sidebar.markdown(f"**Date Range:** {stats.get('date_range', 'N/A')}")
        
        if stats.get('regions'):
            st.sidebar.markdown("**Ocean Regions:**")
            for region, count in stats.get('regions', {}).items():
                st.sidebar.markdown(f"- {region}: {count:,} profiles")
                
    except Exception as e:
        st.sidebar.error(f"Failed to load stats: {e}")


def display_example_questions():
    """Display example questions in sidebar"""
    st.sidebar.markdown("### 💡 Example Questions")
    
    examples = [
        "What is the average temperature in the Pacific Ocean?",
        "Compare salinity between Atlantic and Indian Ocean",
        "Show me temperature trends from 2018 to 2024",
        "How many profiles were collected in 2023?",
        "Find the warmest location in the database",
        "Show me profiles deeper than 1500 meters"
    ]
    
    for example in examples:
        if st.sidebar.button(example, key=example):
            st.session_state.messages.append({"role": "user", "content": example})
            st.rerun()


def main():
    """Main Streamlit app"""
    
    # Header
    st.markdown('<div class="main-header">🌊 FloatChat Ultra</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered ARGO Ocean Data Explorer</div>', unsafe_allow_html=True)
    
    # Initialize RAG engine
    try:
        engine = get_rag_engine()
    except Exception as e:
        st.error(f"Failed to initialize AI engine: {e}")
        st.info("Make sure Ollama is running and PostgreSQL database is accessible.")
        return
    
    # Sidebar
    display_stats(engine)
    st.sidebar.markdown("---")
    display_example_questions()
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ About")
    st.sidebar.info("""
    FloatChat uses AI to help you explore ARGO ocean data.
    
    **Powered by:**
    - 🤖 Ollama (Mistral 7B)
    - 🗄️ PostgreSQL + PostGIS
    - 🧠 RAG Pipeline
    - 🌊 Real ARGO Data
    """)
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Display data table if available
            if message.get("data"):
                st.dataframe(pd.DataFrame(message["data"]), use_container_width=True)
            
            # Display SQL if available
            if message.get("sql"):
                with st.expander("View SQL Query"):
                    st.code(message["sql"], language="sql")
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about ARGO ocean data..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = engine.chat(prompt)
                
                if isinstance(result, str):
                    # Simple text response (greeting, help, etc.)
                    st.markdown(result)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result
                    })
                    
                elif result.get("success"):
                    # Data query response
                    response = result["response"]
                    st.markdown(response)
                    
                    # Show data table
                    if result.get("data") and len(result["data"]) > 0:
                        st.markdown(f"**Found {result['row_count']} result(s):**")
                        st.dataframe(pd.DataFrame(result["data"]), use_container_width=True)
                    
                    # Show SQL
                    with st.expander("View SQL Query"):
                        st.code(result["sql"], language="sql")
                    
                    # Save to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response,
                        "data": result.get("data"),
                        "sql": result.get("sql")
                    })
                    
                else:
                    # Error response
                    error_msg = f"❌ Sorry, I encountered an error: {result.get('error')}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
    
    # Clear chat button
    if st.sidebar.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()


if __name__ == "__main__":
    main()
