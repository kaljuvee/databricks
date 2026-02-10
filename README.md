# Databricks Demo Repository

A comprehensive collection of Databricks demonstrations and examples, showcasing the full capabilities of the Databricks platform for data engineering, machine learning, and generative AI.

## 📦 Projects

### Mosaic AI Demo

A complete demonstration of **Databricks Mosaic AI** capabilities, including Foundation Model APIs, Vector Search, RAG (Retrieval-Augmented Generation), AI Gateway, Lakeflow Pipelines, and Agent Framework.

**Location**: `mosaic-ai-demo/`

**Features**:
- 🤖 **Foundation Model APIs** - Access to Llama, Mixtral, DBRX models
- 🔍 **Vector Search** - Serverless vector database with Delta sync
- 📚 **RAG Pipeline** - Complete retrieval-augmented generation
- 🛡️ **AI Gateway** - Governance with PII masking and rate limiting
- 🔄 **Lakeflow Pipelines** - Automated document processing and embedding
- 🔬 **Agent Framework** - MLflow-based tracing and debugging

**Quick Start**:

**Option 1: Web Interface (Streamlit)**
```bash
cd mosaic-ai-demo
pip install -r requirements.txt
cp .env.sample .env
# Edit .env with your credentials
streamlit run Home.py
```
Open browser to `http://localhost:8501`

**Option 2: TUI (Terminal Interface)**
```bash
cd mosaic-ai-demo
cp .env.sample .env
# Edit .env with your credentials
./mosaic-ai.sh
```
Interactive bash-style commands: `query`, `rag`, `compare`, `trace`

**Option 3: Python Scripts**
```bash
cd mosaic-ai-demo
python src/model_serving.py
python src/rag_pipeline.py
```

**What You Need**:
- Databricks workspace (AWS, Azure, or GCP)
- Personal Access Token (PAT)
- Python 3.8+

See the [Mosaic AI Demo README](mosaic-ai-demo/README.md) for detailed instructions.

---

## 🚀 Getting Started

### Prerequisites

1. **Databricks Workspace**: Sign up at [databricks.com](https://www.databricks.com/try-databricks)
2. **Personal Access Token**: Generate in User Settings → Developer → Access Tokens
3. **Python 3.8+**: Download from [python.org](https://www.python.org/downloads/)

### Generate Your Databricks Token

1. Log in to your Databricks workspace
2. Click your **username** (top-right) → **User Settings**
3. Go to **Developer** → **Access Tokens**
4. Click **Generate New Token**
5. Set a comment (e.g., "Demo Projects")
6. Click **Generate** and copy the token immediately

### Environment Setup

Each project requires a `.env` file with your credentials:

```bash
DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
DATABRICKS_TOKEN=your_token_here
```

Your workspace URL format:
- **AWS**: `https://<workspace-id>.cloud.databricks.com`
- **Azure**: `https://adb-<workspace-id>.<random>.azuredatabricks.net`
- **GCP**: `https://<workspace-id>.gcp.databricks.com`

---

## 📚 Documentation

- [Databricks Documentation](https://docs.databricks.com)
- [Mosaic AI Documentation](https://docs.databricks.com/en/generative-ai/generative-ai.html)
- [Model Serving Guide](https://docs.databricks.com/en/machine-learning/model-serving/index.html)
- [Vector Search Guide](https://docs.databricks.com/en/generative-ai/vector-search.html)
- [Lakeflow Documentation](https://docs.databricks.com/en/delta-live-tables/index.html)

---

## 💰 Pricing

Databricks Mosaic AI uses pay-per-token pricing:

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| Llama 3.1 8B | $0.15 | $0.45 |
| Llama 3.3 70B | $0.50 | $1.50 |
| Llama 3.1 405B | $2.00 | $6.00 |

**Cost Optimization**:
- Start with Llama 3.1 8B for development
- Configure endpoints to scale to zero
- Use model routing for different query complexities
- Monitor usage with built-in tracking

---

## 🛠️ Technologies

- **Databricks Mosaic AI** - Unified generative AI platform
- **Delta Lake** - Open-source storage layer
- **MLflow** - ML lifecycle management
- **Apache Spark** - Distributed data processing
- **Unity Catalog** - Unified governance
- **Vector Search** - Serverless vector database
- **Lakeflow** - Declarative data pipelines

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Support

- **Issues**: Open an issue on [GitHub](https://github.com/kaljuvee/databricks/issues)
- **Documentation**: Check project-specific READMEs
- **Databricks Support**: Contact through your workspace

---

## 🌟 Acknowledgments

Built with Databricks Mosaic AI, showcasing the power of unified AI development on the lakehouse architecture.

---

**Ready to get started?** Navigate to the `mosaic-ai-demo/` directory and follow the README!
