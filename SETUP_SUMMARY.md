# Databricks Mosaic AI Demo - Setup Summary

## Project Successfully Created! 🎉

The Databricks Mosaic AI demo project has been successfully created and pushed to your repository at:
**https://github.com/kaljuvee/databricks**

## Project Location

The demo project is located in the `mosaic-ai-demo/` directory of your repository.

## What's Included

### 1. **Source Code** (`src/`)
- `model_serving.py` - Foundation Model API examples (Llama, Mixtral, DBRX)
- `vector_search.py` - Vector Search implementation for similarity search
- `rag_pipeline.py` - Complete RAG pipeline with retrieval and generation
- `ai_gateway.py` - AI Gateway with PII masking, rate limiting, and toxicity filtering
- `utils.py` - Utility functions for cost calculation, formatting, and validation

### 2. **Documentation** (`docs/`)
- `setup_guide.md` - Comprehensive setup and troubleshooting guide

### 3. **Sample Data** (`data/`)
- `sample_documents/databricks_intro.txt` - Sample document for RAG demonstrations

### 4. **Configuration Files**
- `.env.sample` - Template for environment variables (see below)
- `requirements.txt` - Python dependencies
- `README.md` - Project overview and quick start guide

## Required Environment Variables

To run the demo, you need to provide the following credentials in a `.env` file:

### **REQUIRED** (Minimum to get started)

```bash
# Your Databricks workspace URL
DATABRICKS_HOST=https://your-workspace.cloud.databricks.com

# Your Personal Access Token (PAT)
DATABRICKS_TOKEN=dapi1234567890abcdef
```

### How to Get These Values

#### 1. **DATABRICKS_HOST** (Your Workspace URL)

Your workspace URL depends on your cloud provider:

- **AWS**: `https://<workspace-id>.cloud.databricks.com`
- **Azure**: `https://adb-<workspace-id>.<random>.azuredatabricks.net`
- **GCP**: `https://<workspace-id>.gcp.databricks.com`

You can find this URL in your browser's address bar when logged into Databricks.

#### 2. **DATABRICKS_TOKEN** (Personal Access Token)

To generate a Personal Access Token:

1. Log in to your Databricks workspace
2. Click on your **username** in the top-right corner
3. Select **User Settings**
4. Navigate to **Developer** → **Access Tokens**
5. Click **Generate New Token**
6. Set a comment (e.g., "Mosaic AI Demo")
7. Set an expiration date (optional)
8. Click **Generate**
9. **Copy the token immediately** (you won't be able to see it again!)

**Token Permissions Needed:**
- Workspace access
- SQL access (for Vector Search)
- Serving access (for Model Serving)

### **OPTIONAL** Environment Variables

These are optional and have sensible defaults:

```bash
# Catalog and Schema (defaults: main, default)
DATABRICKS_CATALOG=main
DATABRICKS_SCHEMA=default

# Default model (defaults to cheapest option)
DEFAULT_MODEL=databricks-llama-3-1-8b-instruct

# Vector Search (only if using Vector Search features)
VECTOR_SEARCH_ENDPOINT=your_vector_search_endpoint
VECTOR_INDEX_NAME=main.default.docs_index
EMBEDDING_MODEL_ENDPOINT=databricks-bge-large-en

# AI Gateway settings
DATABRICKS_GATEWAY_ROUTE=default
RATE_LIMIT_PER_MINUTE=10
ENABLE_PII_MASKING=true
ENABLE_TOXICITY_FILTER=true

# RAG Pipeline settings
RAG_NUM_CONTEXT_CHUNKS=3
RAG_CHUNK_SIZE=500
RAG_CHUNK_OVERLAP=50
RAG_TEMPERATURE=0.3
```

## Quick Start Guide

### 1. Clone and Navigate to the Project

```bash
git clone https://github.com/kaljuvee/databricks.git
cd databricks/mosaic-ai-demo
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy the sample file
cp .env.sample .env

# Edit .env with your credentials
# Add your DATABRICKS_HOST and DATABRICKS_TOKEN
```

### 5. Run the Examples

```bash
# Test Model Serving
python src/model_serving.py

# Test Vector Search
python src/vector_search.py

# Test RAG Pipeline
python src/rag_pipeline.py

# Test AI Gateway
python src/ai_gateway.py
```

## Features Demonstrated

### 1. **Foundation Model APIs** (`model_serving.py`)
- Access to Llama 3.3, Mixtral, DBRX models
- OpenAI-compatible API interface
- Streaming responses
- Cost estimation
- Model comparison

### 2. **Vector Search** (`vector_search.py`)
- Serverless vector database
- Automatic Delta table synchronization
- Similarity search
- Index management

### 3. **RAG Pipeline** (`rag_pipeline.py`)
- Document chunking with overlap
- Context retrieval
- Answer generation with citations
- Batch query processing
- MLflow integration ready

### 4. **AI Gateway** (`ai_gateway.py`)
- PII detection and masking
- Rate limiting per user
- Toxicity filtering
- Usage tracking and reporting
- Governance compliance

## Pricing Information

The demo uses pay-per-token pricing:

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| **Llama 3.1 8B** (Recommended for testing) | $0.15 | $0.45 |
| Llama 3.3 70B | $0.50 | $1.50 |
| Llama 3.1 405B | $2.00 | $6.00 |

**Cost Optimization Tips:**
- Start with Llama 3.1 8B for development (cheapest)
- Use smaller models for simple tasks
- Configure endpoints to "scale to zero" when not in use
- Monitor token usage with the built-in utilities

## Next Steps

1. **Set up your `.env` file** with your Databricks credentials
2. **Run the examples** to verify everything works
3. **Explore the code** to understand how each feature works
4. **Read the setup guide** at `docs/setup_guide.md` for advanced configuration
5. **Customize the demos** for your specific use cases

## Troubleshooting

### Common Issues

**"401 Unauthorized"**
- Check that your `DATABRICKS_TOKEN` is correct and not expired
- Verify your token has the necessary permissions

**"Model endpoint not found"**
- Ensure Foundation Model APIs are enabled in your workspace
- Try using `databricks-llama-3-1-8b-instruct` (most widely available)

**"Vector Search endpoint not found"**
- Vector Search requires additional setup (see setup guide)
- You can skip Vector Search examples initially

**Import errors**
- Activate your virtual environment
- Run `pip install -r requirements.txt`

## Support and Documentation

- **Setup Guide**: `mosaic-ai-demo/docs/setup_guide.md`
- **Project README**: `mosaic-ai-demo/README.md`
- **Databricks Docs**: https://docs.databricks.com/en/generative-ai/generative-ai.html
- **GitHub Repository**: https://github.com/kaljuvee/databricks

## Summary of What You Need

To get started, you only need **TWO things**:

1. ✅ **DATABRICKS_HOST** - Your workspace URL
2. ✅ **DATABRICKS_TOKEN** - Your Personal Access Token

Everything else is optional and has defaults!

---

**Happy coding with Databricks Mosaic AI! 🚀**
