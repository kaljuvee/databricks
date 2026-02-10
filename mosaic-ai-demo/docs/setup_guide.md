# Databricks Mosaic AI Demo - Setup Guide

This guide provides detailed instructions for setting up and running the Databricks Mosaic AI demo project.

## Prerequisites

Before you begin, ensure you have the following:

### 1. Databricks Workspace

You need access to a Databricks workspace on one of the following cloud platforms:
- **AWS**: Amazon Web Services
- **Azure**: Microsoft Azure
- **GCP**: Google Cloud Platform

If you don't have a workspace, you can sign up for a free trial at [databricks.com](https://www.databricks.com/try-databricks).

### 2. Python Environment

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment tool (recommended: `venv` or `conda`)

### 3. Git

- Git installed on your local machine
- GitHub account (for cloning the repository)

## Step-by-Step Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/kaljuvee/databricks.git
cd databricks/mosaic-ai-demo
```

### Step 2: Create a Virtual Environment

It's recommended to use a virtual environment to isolate dependencies:

```bash
# Using venv
python -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

#### 4.1 Copy the Sample Environment File

```bash
cp .env.sample .env
```

#### 4.2 Generate a Databricks Personal Access Token

1. Log in to your Databricks workspace
2. Click on your username in the top-right corner
3. Select **User Settings**
4. Navigate to **Developer** → **Access Tokens**
5. Click **Generate New Token**
6. Set a comment (e.g., "Mosaic AI Demo")
7. Set an expiration date (or leave blank for no expiration)
8. Click **Generate**
9. **Important**: Copy the token immediately and save it securely

#### 4.3 Find Your Workspace URL

Your workspace URL depends on your cloud provider:

**AWS:**
```
https://<workspace-id>.cloud.databricks.com
```

**Azure:**
```
https://adb-<workspace-id>.<random-number>.azuredatabricks.net
```

**GCP:**
```
https://<workspace-id>.gcp.databricks.com
```

You can find your workspace URL in the browser address bar when logged into Databricks.

#### 4.4 Edit the .env File

Open the `.env` file in a text editor and fill in the required values:

```bash
# Required
DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
DATABRICKS_TOKEN=dapi1234567890abcdef

# Optional (use defaults or customize)
DATABRICKS_CATALOG=main
DATABRICKS_SCHEMA=default
DEFAULT_MODEL=databricks-llama-3-1-8b-instruct
```

### Step 5: Verify Your Setup

Run the utility script to verify your environment configuration:

```bash
python src/utils.py
```

This will check that all required environment variables are set correctly.

## Running the Examples

### Example 1: Model Serving

Test the Foundation Model APIs:

```bash
python src/model_serving.py
```

This will:
- Connect to Databricks Model Serving
- Query Llama 3.1 8B model
- Demonstrate streaming responses
- Show cost estimation

**Expected Output:**
```
================================================================================
Databricks Mosaic AI - Model Serving Demo
================================================================================

✓ Successfully connected to Databricks Model Serving

--------------------------------------------------------------------------------
Example 1: Simple Query with Llama 3.1 8B
--------------------------------------------------------------------------------
Model: databricks-llama-3-1-8b-instruct
Response: Retrieval-Augmented Generation (RAG) is...
Tokens used: 245
```

### Example 2: Vector Search

Explore Vector Search capabilities:

```bash
python src/vector_search.py
```

This will:
- List existing Vector Search endpoints
- Show examples of creating indexes
- Demonstrate query operations

**Note**: To fully use Vector Search, you need to:
1. Create a Vector Search endpoint in your workspace
2. Create a Delta table with your documents
3. Create a Vector Search index

### Example 3: RAG Pipeline

Run the complete RAG pipeline:

```bash
python src/rag_pipeline.py
```

This will:
- Demonstrate document chunking
- Show retrieval and generation
- Process batch queries
- Display best practices

### Example 4: AI Gateway

Test governance features:

```bash
python src/ai_gateway.py
```

This will:
- Detect and mask PII
- Apply rate limiting
- Check for toxic content
- Generate usage reports

## Advanced Configuration

### Setting Up Vector Search

To use Vector Search in your demos:

#### 1. Create a Vector Search Endpoint

In your Databricks workspace:
1. Go to **Compute** → **Vector Search**
2. Click **Create Endpoint**
3. Name it (e.g., `my_vector_search_endpoint`)
4. Select endpoint type (Standard or Provisioned)
5. Click **Create**

#### 2. Create a Delta Table with Documents

```sql
CREATE TABLE main.default.my_docs (
  id STRING,
  text STRING,
  source STRING,
  metadata MAP<STRING, STRING>
);

INSERT INTO main.default.my_docs VALUES
  ('doc1', 'Your document text here...', 'source1.pdf', map('page', '1')),
  ('doc2', 'Another document...', 'source2.pdf', map('page', '1'));
```

#### 3. Create a Vector Search Index

```python
from databricks.vector_search.client import VectorSearchClient

client = VectorSearchClient()

client.create_delta_sync_index(
    endpoint_name="my_vector_search_endpoint",
    index_name="main.default.my_docs_index",
    source_table_name="main.default.my_docs",
    pipeline_type="TRIGGERED",
    primary_key="id",
    embedding_source_column="text",
    embedding_model_endpoint_name="databricks-bge-large-en"
)
```

#### 4. Update Your .env File

```bash
VECTOR_SEARCH_ENDPOINT=my_vector_search_endpoint
VECTOR_INDEX_NAME=main.default.my_docs_index
```

### Using Different Models

The demo supports multiple models. Update your `.env` file to try different ones:

```bash
# Fastest and cheapest
DEFAULT_MODEL=databricks-llama-3-1-8b-instruct

# Balanced performance
DEFAULT_MODEL=databricks-llama-3-3-70b-instruct

# Most capable
DEFAULT_MODEL=databricks-llama-3-1-405b-instruct

# Alternative architectures
DEFAULT_MODEL=databricks-mixtral-8x7b-instruct
DEFAULT_MODEL=databricks-dbrx-instruct
```

### Integrating External Models

You can also use external models through the AI Gateway:

```python
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DATABRICKS_TOKEN"),
    base_url=f"{os.getenv('DATABRICKS_HOST')}/serving-endpoints"
)

# Use OpenAI GPT-4 through Databricks Gateway
response = client.chat.completions.create(
    model="openai-gpt-4",  # External model route
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Troubleshooting

### Authentication Errors

**Error**: `401 Unauthorized` or `Invalid token`

**Solutions**:
1. Verify your token is correct and not expired
2. Check that your `DATABRICKS_HOST` URL is correct
3. Ensure your token has the necessary permissions
4. Try generating a new token

### Model Not Found

**Error**: `404 Not Found` or `Model endpoint not found`

**Solutions**:
1. Check that Foundation Model APIs are enabled in your workspace
2. Verify the model name is correct
3. Ensure your workspace has access to the requested model
4. Try a different model (e.g., `databricks-llama-3-1-8b-instruct`)

### Vector Search Errors

**Error**: `Vector Search endpoint not found`

**Solutions**:
1. Create a Vector Search endpoint in your workspace
2. Update the `VECTOR_SEARCH_ENDPOINT` in your `.env` file
3. Ensure Vector Search is enabled for your workspace
4. Check that your token has SQL access permissions

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'openai'`

**Solutions**:
1. Ensure you've activated your virtual environment
2. Run `pip install -r requirements.txt`
3. Check that you're using Python 3.8 or higher

### Connection Timeouts

**Error**: `Connection timeout` or `Request timeout`

**Solutions**:
1. Check your internet connection
2. Verify your workspace URL is accessible
3. Try increasing timeout values in the code
4. Check if your workspace is in a hibernated state

## Cost Management

### Understanding Pricing

Databricks Foundation Model APIs use pay-per-token pricing:

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| Llama 3.1 8B | $0.15 | $0.45 |
| Llama 3.3 70B | $0.50 | $1.50 |
| Llama 3.1 405B | $2.00 | $6.00 |

### Cost Optimization Tips

1. **Start Small**: Use Llama 3.1 8B for development and testing
2. **Monitor Usage**: Track token consumption with the usage reports
3. **Set Budgets**: Configure spending alerts in your Databricks workspace
4. **Cache Results**: Cache frequent queries to avoid repeated API calls
5. **Scale to Zero**: Ensure endpoints scale to zero when not in use

### Estimating Costs

Use the utility function to estimate costs:

```python
from src.utils import calculate_cost

cost = calculate_cost(
    prompt_tokens=1000,
    completion_tokens=500,
    model="llama-3-1-8b"
)

print(f"Estimated cost: ${cost['total_cost']:.6f}")
```

## Best Practices

### Security

1. **Never commit `.env` files**: Always keep credentials out of version control
2. **Use short-lived tokens**: Set expiration dates on Personal Access Tokens
3. **Rotate tokens regularly**: Generate new tokens periodically
4. **Use Service Principals**: For production, use Service Principals instead of PATs
5. **Enable PII masking**: Always mask sensitive data in logs

### Performance

1. **Batch requests**: Process multiple queries together when possible
2. **Use appropriate models**: Don't use large models for simple tasks
3. **Implement caching**: Cache embeddings and frequent query results
4. **Monitor latency**: Track response times and optimize accordingly
5. **Use async operations**: Implement async/await for concurrent requests

### Development

1. **Use version control**: Track changes with Git
2. **Write tests**: Add unit tests for your RAG components
3. **Document changes**: Keep documentation up-to-date
4. **Log everything**: Use proper logging for debugging
5. **Monitor costs**: Track token usage and costs continuously

## Next Steps

### Extend the Demo

1. **Add more models**: Try different Foundation Models
2. **Build a UI**: Create a Streamlit or Gradio interface
3. **Add more documents**: Expand your Vector Search index
4. **Implement feedback**: Add user feedback loops
5. **Deploy to production**: Use Databricks Jobs for scheduling

### Learn More

- [Databricks Mosaic AI Documentation](https://docs.databricks.com/en/generative-ai/generative-ai.html)
- [Model Serving Guide](https://docs.databricks.com/en/machine-learning/model-serving/index.html)
- [Vector Search Guide](https://docs.databricks.com/en/generative-ai/vector-search.html)
- [RAG Tutorial](https://docs.databricks.com/en/generative-ai/tutorials/ai-cookbook/index.html)
- [AI Gateway Documentation](https://docs.databricks.com/en/generative-ai/ai-gateway.html)

## Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section above
2. Review the [Databricks Documentation](https://docs.databricks.com)
3. Open an issue on the [GitHub repository](https://github.com/kaljuvee/databricks/issues)
4. Contact Databricks Support through your workspace

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License. See the LICENSE file for details.
