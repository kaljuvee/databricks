# Databricks Mosaic AI Demo

A comprehensive demonstration of Databricks Mosaic AI capabilities including Model Serving, Vector Search, RAG (Retrieval-Augmented Generation), AI Gateway, Lakeflow Pipelines, and Agent Framework features.

## Features

This demo project illustrates the following Databricks Mosaic AI capabilities:

### 1. **Foundation Model APIs & Model Serving**
- Access to state-of-the-art open models (Llama 3.3, Mixtral, DBRX)
- External model integration (OpenAI, Anthropic, Google Gemini)
- OpenAI-compatible API interface
- Streaming responses and batch processing
- Cost estimation and optimization

### 2. **Mosaic AI Gateway**
- Rate limiting and usage tracking
- AI Guardrails (PII masking, toxicity filters)
- Unified governance layer for model calls
- Compliance and security features

### 3. **Vector Search**
- Serverless vector database
- Automatic synchronization with Delta Tables
- Real-time index updates
- Similarity search and filtering

### 4. **RAG (Retrieval-Augmented Generation)**
- Document chunking and embedding pipelines
- Integration with Delta Lake
- Context retrieval and answer generation
- Source citation and traceability

### 5. **Lakeflow Spark Declarative Pipelines**
- Automated document processing (chunking and embedding)
- Delta Live Tables (DLT) for declarative transformations
- Medallion architecture (Bronze → Silver → Gold)
- Data quality expectations and monitoring
- Automatic sync with Vector Search indexes

### 6. **Mosaic AI Agent Framework**
- Agent configuration and deployment
- End-to-end tracing with MLflow
- Performance monitoring and analysis
- Quality indicators and recommendations
- Production deployment patterns

### 7. **AI Playground**
- Browser-based chat interface
- Side-by-side model comparison

## Project Structure

```
mosaic-ai-demo/
├── src/
│   ├── model_serving.py          # Foundation Model API examples
│   ├── vector_search.py          # Vector Search implementation
│   ├── rag_pipeline.py           # RAG application logic
│   ├── ai_gateway.py             # AI Gateway with guardrails
│   ├── lakeflow_pipeline.py      # Lakeflow DLT pipeline examples
│   ├── agent_framework.py        # Agent Framework with MLflow tracing
│   └── utils.py                  # Helper functions
├── notebooks/
│   └── (Jupyter notebooks for interactive demos)
├── data/
│   └── sample_documents/         # Sample documents for RAG
├── docs/
│   └── setup_guide.md            # Detailed setup instructions
├── .env.sample                   # Environment variables template
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Prerequisites

- Databricks workspace (AWS, Azure, or GCP)
- Python 3.8+
- Personal Access Token (PAT) from Databricks

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/kaljuvee/databricks.git
cd databricks/mosaic-ai-demo
```

### 2. Set Up Environment Variables

Copy the `.env.sample` file to `.env` and fill in your credentials:

```bash
cp .env.sample .env
```

Edit `.env` with your Databricks credentials:
- `DATABRICKS_HOST`: Your workspace URL
- `DATABRICKS_TOKEN`: Your Personal Access Token

### 3. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Run Examples

```bash
# Test Model Serving
python src/model_serving.py

# Test Vector Search
python src/vector_search.py

# Run RAG Pipeline
python src/rag_pipeline.py

# Test AI Gateway
python src/ai_gateway.py

# Explore Lakeflow Pipelines
python src/lakeflow_pipeline.py

# Try Agent Framework
python src/agent_framework.py
```

## Configuration

### Generating a Databricks Personal Access Token

1. Log in to your Databricks workspace
2. Go to **User Settings** → **Developer** → **Access Tokens**
3. Click **Generate New Token**
4. Copy the token and save it in your `.env` file

### Finding Your Workspace URL

Your workspace URL follows this format:
- AWS: `https://<workspace-id>.cloud.databricks.com`
- Azure: `https://adb-<workspace-id>.<random>.azuredatabricks.net`
- GCP: `https://<workspace-id>.gcp.databricks.com`

## Cost Optimization Tips

1. **Use Smaller Models**: Start with Llama 3.1 8B (~$0.15 per 1M input tokens) for simple tasks
2. **Scale to Zero**: Configure endpoints to scale to zero when not in use
3. **Model Routing**: Use AI Gateway to route simple queries to cheaper models
4. **Pay-Per-Token**: Use Foundation Model APIs instead of provisioning dedicated GPU hardware

## Pricing Reference

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| Llama 3.1 8B | $0.15 | $0.45 |
| Llama 3.3 70B | $0.50 | $1.50 |
| Llama 3.1 405B | $2.00 | $6.00 |

## Documentation

- [Databricks Mosaic AI Documentation](https://docs.databricks.com/en/generative-ai/generative-ai.html)
- [Model Serving Guide](https://docs.databricks.com/en/machine-learning/model-serving/index.html)
- [Vector Search Guide](https://docs.databricks.com/en/generative-ai/vector-search.html)
- [RAG Tutorial](https://docs.databricks.com/en/generative-ai/tutorials/ai-cookbook/index.html)
- [Lakeflow Documentation](https://docs.databricks.com/en/delta-live-tables/index.html)
- [Agent Framework Guide](https://docs.databricks.com/en/generative-ai/agent-framework/index.html)

## Examples Included

### 1. Model Serving (`src/model_serving.py`)
- Connect to Foundation Model APIs
- Query different models (Llama, Mixtral, DBRX)
- Compare responses from multiple models
- Streaming responses
- Cost estimation

### 2. Vector Search (`src/vector_search.py`)
- Create and manage vector search indexes
- Embed documents and perform similarity search
- Sync with Delta Tables
- Query with filters

### 3. RAG Pipeline (`src/rag_pipeline.py`)
- Load and chunk documents
- Create embeddings and store in vector database
- Retrieve relevant context and generate answers
- Batch query processing
- Source citation

### 4. AI Gateway (`src/ai_gateway.py`)
- Configure rate limiting
- Apply PII masking
- Filter toxic content
- Track usage metrics
- Generate compliance reports

### 5. Lakeflow Pipeline (`src/lakeflow_pipeline.py`)
- Generate Delta Live Tables pipeline configuration
- Automated document chunking and embedding
- Medallion architecture (Bronze → Silver → Gold)
- Data quality expectations
- Integration with Vector Search

### 6. Agent Framework (`src/agent_framework.py`)
- Create agent configurations
- Trace retrieval and generation steps
- End-to-end pipeline tracing
- Performance analysis and recommendations
- MLflow integration for experiment tracking

## Troubleshooting

### Authentication Errors
- Verify your `DATABRICKS_TOKEN` is valid and not expired
- Check that your `DATABRICKS_HOST` URL is correct

### Model Serving Errors
- Ensure your workspace has access to Foundation Model APIs
- Check that the model endpoint is running

### Vector Search Errors
- Verify Vector Search is enabled in your workspace
- Check Delta Table permissions

### Lakeflow Pipeline Errors
- Ensure Delta Live Tables is enabled
- Check that source tables exist
- Verify pipeline configuration

## Advanced Setup

### Setting Up Lakeflow Pipelines

1. **Create Source Table**: Run the SQL from `lakeflow_pipeline.py` to create sample documents
2. **Create DLT Pipeline**: Upload the generated notebook to Databricks
3. **Configure Pipeline**: Use the generated configuration
4. **Start Pipeline**: Monitor execution in the DLT UI
5. **Create Vector Index**: Point to the output table with automatic sync

### Deploying Agents with MLflow

1. **Run Agent**: Execute `agent_framework.py` to generate traces
2. **Log to MLflow**: Use the generated MLflow code
3. **Analyze Performance**: Review metrics in MLflow UI
4. **Register Model**: Register the agent in Model Registry
5. **Deploy**: Deploy as a Model Serving endpoint

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Open an issue on GitHub
- Consult [Databricks Documentation](https://docs.databricks.com)
- Contact Databricks Support

## Acknowledgments

Built with Databricks Mosaic AI platform, showcasing the power of unified AI development on the lakehouse architecture. This demo covers all major RAG components:

- **Foundation Model APIs** for generation
- **Vector Search** for retrieval
- **Lakeflow Pipelines** for automated data processing
- **Agent Framework** for tracing and optimization
- **AI Gateway** for governance and compliance

Start building production-ready generative AI applications today! 🚀
