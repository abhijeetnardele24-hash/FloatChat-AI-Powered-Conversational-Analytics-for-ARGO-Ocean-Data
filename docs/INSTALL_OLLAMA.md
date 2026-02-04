# Ollama Installation Guide for Windows

## What is Ollama?

Ollama allows you to run Large Language Models (LLMs) locally on your computer. FloatChat uses Ollama to power the AI chatbot that understands natural language queries about ocean data.

## Quick Install Steps

### 1. Download Ollama

Visit: **https://ollama.com/download**

- Click **Download for Windows**
- File size: ~500 MB
- Installer: `OllamaSetup.exe`

### 2. Install Ollama

1. **Run** the downloaded installer
2. Follow the installation wizard
3. Ollama will install to: `C:\Users\<YourName>\AppData\Local\Programs\Ollama`
4. Installation completes in ~2 minutes

### 3. Verify Installation

Open **Command Prompt** or **PowerShell**:

```bash
# Check Ollama version
ollama --version

# Should show: ollama version 0.x.x
```

### 4. Pull Mistral Model

**Mistral 7B** is our recommended model (4.1 GB download):

```bash
# Pull the model
ollama pull mistral:7b-instruct

# This will download ~4.1 GB
# Takes 5-15 minutes depending on internet speed
```

**Progress will show**:
```
pulling manifest
pulling 8eeb52dfb3bb... 100% ▕████████████▏ 4.1 GB
pulling 73b313b5552d... 100% ▕████████████▏ 1.4 KB
pulling 0ba8f0e314b4... 100% ▕████████████▏  12 KB
pulling 56bb8bd477a5... 100% ▕████████████▏  96 B
pulling 1a4c3c319823... 100% ▕████████████▏ 485 B
verifying sha256 digest
writing manifest
success
```

### 5. Test the Model

```bash
# Run Mistral interactively
ollama run mistral:7b-instruct

# Try a test query:
>>> What is oceanography?

# You should get a detailed response about oceanography

# Exit with Ctrl+D or type: /bye
```

### 6. Start Ollama Server

Ollama usually auto-starts, but if needed:

```bash
# Start Ollama server
ollama serve

# Server runs on: http://localhost:11434
```

### 7. Verify API Access

```bash
# Test API endpoint
curl http://localhost:11434/api/tags

# Should return JSON with available models
```

## Alternative Models

### Smaller Model (Faster, Less Accurate)
```bash
# Mistral 7B (no instruct) - 3.8 GB
ollama pull mistral:7b
```

### Larger Model (Better Quality, Requires More RAM)
```bash
# Mixtral 8x7B - Requires 24GB+ RAM
ollama pull mixtral:8x7b-instruct

# Llama 3.1 70B - Requires 48GB+ RAM
ollama pull llama3.1:70b
```

### Recommended for FloatChat:
- **Development**: `mistral:7b-instruct` (4.1 GB, 8GB RAM)
- **Production**: `mixtral:8x7b-instruct` (26 GB, 24GB RAM)

## Useful Ollama Commands

```bash
# List installed models
ollama list

# Remove a model
ollama rm mistral:7b-instruct

# Show model information
ollama show mistral:7b-instruct

# Update a model
ollama pull mistral:7b-instruct

# Run model with custom parameters
ollama run mistral:7b-instruct --temperature 0.1
```

## Troubleshooting

### Issue: "ollama: command not found"

**Solution**: Restart terminal after installation

### Issue: "connection refused"

**Solution**: Start Ollama server
```bash
ollama serve
```

### Issue: Model download fails

**Solutions**:
1. Check internet connection
2. Try again: `ollama pull mistral:7b-instruct`
3. Use different mirror (if available)

### Issue: Out of memory

**Solution**: Use smaller model
```bash
ollama pull mistral:7b  # Instead of mixtral
```

## Performance Tips

### 1. GPU Acceleration
- Ollama automatically uses NVIDIA GPU if available
- Check GPU usage: Task Manager → Performance → GPU

### 2. Memory Management
- Close other applications when running large models
- Monitor RAM usage in Task Manager

### 3. Model Selection
| Model | Size | RAM Required | Speed | Quality |
|-------|------|--------------|-------|---------|
| mistral:7b | 3.8 GB | 8 GB | Fast | Good |
| mistral:7b-instruct | 4.1 GB | 8 GB | Fast | Better |
| mixtral:8x7b-instruct | 26 GB | 24 GB | Slow | Best |

## Integration with FloatChat

After installation, update `.env`:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral:7b-instruct
OLLAMA_TEMPERATURE=0.1
OLLAMA_NUM_CTX=8192
```

## Testing Integration

```python
# test_ollama.py
import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "mistral:7b-instruct",
        "prompt": "What is ARGO ocean data?",
        "stream": False
    }
)

print(response.json()['response'])
```

Run:
```bash
python test_ollama.py
```

## Next Steps

1. ✅ Install Ollama
2. ✅ Pull mistral:7b-instruct model
3. ✅ Verify server is running
4. ✅ Update .env configuration
5. 🔄 Test with FloatChat

---

**Installation Time**: ~20 minutes (including download)  
**Disk Space**: ~5 GB (for Mistral 7B)  
**RAM Required**: 8 GB minimum, 16 GB recommended

## Resources

- **Official Docs**: https://github.com/ollama/ollama
- **Model Library**: https://ollama.com/library
- **Discord Community**: https://discord.gg/ollama
