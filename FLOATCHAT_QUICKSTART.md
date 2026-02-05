# FloatChat Ultra - Quick Start Guide

## 🚀 Quick Start (3 Steps)

### 1. Start Ollama Server

```bash
# In a separate terminal
ollama serve
```

### 2. Wait for Data Download to Complete

The global ARGO dataset download is currently running in the background:
- **Size**: 20-25 GB
- **Time**: 4-6 hours
- **Profiles**: ~800,000
- **Coverage**: All ocean regions (Pacific, Atlantic, Indian, Southern, Arctic)

**Check progress**: Look at the terminal where download is running

### 3. Launch FloatChat (After Download Completes)

```bash
# Activate virtual environment
.\venv\Scripts\activate

# Launch FloatChat
python run_floatchat.py
```

This will open FloatChat in your browser at `http://localhost:8501`

---

## 💬 Using FloatChat

### Example Questions:

**Statistical Queries:**
- "What is the average temperature in the Pacific Ocean?"
- "Show me salinity statistics for the Indian Ocean"

**Regional Comparisons:**
- "Compare temperature between Atlantic and Pacific"
- "Show me all floats in the Southern Ocean"

**Temporal Analysis:**
- "What was the temperature in summer 2023?"
- "Show temperature trends from 2018 to 2024"

**Specific Queries:**
- "Find the warmest location in the database"
- "Show me profiles deeper than 1500 meters"
- "How many profiles were collected in 2022?"

---

## 🔧 Manual Pipeline Execution

If you want to run the data pipeline manually:

### Step 1: Download Index
```bash
python src/data/download_index.py
```

### Step 2: Download NetCDF Files (4-6 hours)
```bash
python src/data/download_netcdf.py
```

### Step 3: Parse NetCDF Files
```bash
python src/data/parse_netcdf.py
```

### Step 4: Load into Database
```bash
python src/data/load_database.py
```

---

## 🧪 Test AI Components

### Test NL-to-SQL Converter:
```bash
python src/ai/nl_to_sql.py
```

### Test RAG Engine:
```bash
python src/ai/rag_engine.py
```

---

## 📊 Current Status

✅ **Phase 1**: Requirements & Planning - COMPLETE  
✅ **Phase 2**: Infrastructure Setup - COMPLETE  
🔄 **Phase 3**: Data Acquisition - IN PROGRESS  
- ✅ Scripts created
- ✅ Global coverage configured
- 🔄 Downloading 20-25 GB dataset (4-6 hours)
- ⏳ Parse and load (pending download completion)

✅ **Phase 4**: AI Integration - COMPLETE  
- ✅ Query examples created
- ✅ NL-to-SQL converter built
- ✅ RAG engine implemented
- ✅ Streamlit chat interface ready

⏳ **Phase 5**: Testing & Validation - PENDING  
⏳ **Phase 6**: Documentation & Polish - PENDING

---

## 🎯 What FloatChat Can Do

### Natural Language Understanding
Ask questions in plain English - FloatChat converts them to SQL automatically!

### Intelligent Responses
Get natural language answers with specific data insights

### Data Visualization
View results in interactive tables

### SQL Transparency
See the generated SQL queries to understand what's happening

### Multi-Region Support
Query data from any ocean region worldwide

### Temporal Analysis
Analyze trends over time (2018-2024)

---

## 🐛 Troubleshooting

### "Ollama connection failed"
**Solution**: Start Ollama server
```bash
ollama serve
```

### "Database connection failed"
**Solution**: Check PostgreSQL is running on port 5433
```bash
& "C:\Program Files\PostgreSQL\18\bin\pg_ctl.exe" status -D "C:\Program Files\PostgreSQL\18\data"
```

### "No data found"
**Solution**: Wait for data download to complete, then run:
```bash
python src/data/parse_netcdf.py
python src/data/load_database.py
```

---

## 📈 Expected Dataset Stats

After download completes:

| Metric | Value |
|--------|-------|
| **Floats** | ~1,000-1,500 |
| **Profiles** | ~800,000 |
| **Measurements** | ~80-100 million |
| **Date Range** | 2018-2024 |
| **Regions** | All 5 oceans |
| **Raw Data Size** | 20-25 GB |
| **Database Size** | ~2-3 GB |

---

## 🌟 Features

- 🤖 **AI-Powered**: Uses Ollama + Mistral 7B for natural language understanding
- 🗄️ **PostgreSQL + PostGIS**: Spatial queries and efficient data storage
- 🧠 **RAG Pipeline**: Retrieval-Augmented Generation for intelligent responses
- 🌊 **Real ARGO Data**: Authentic oceanographic measurements
- 🌍 **Global Coverage**: All ocean regions worldwide
- 📊 **Interactive UI**: Beautiful Streamlit dashboard
- 🔍 **SQL Transparency**: See generated queries
- 📈 **Data Visualization**: Interactive tables and charts

---

**Built with ❤️ for the oceanographic community** 🌊

*Last Updated: February 5, 2026*
