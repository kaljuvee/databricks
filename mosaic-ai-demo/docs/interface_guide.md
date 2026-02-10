# Interface Guide

This guide covers all three ways to interact with the Databricks Mosaic AI Demo.

---

## 🌐 Web Interface (Streamlit)

### Overview

The Streamlit web interface provides a visual, browser-based way to explore all Mosaic AI features with interactive forms, charts, and real-time feedback.

### Launch

```bash
cd mosaic-ai-demo
pip install -r requirements.txt
cp .env.sample .env
# Edit .env with your credentials
streamlit run Home.py
```

Open browser to: **http://localhost:8501**

### Features

#### Home Page
- Overview of all components
- Quick stats and pricing information
- Configuration status check
- Links to documentation

#### 🤖 Model Serving Page
- **Query Tab**: Ask questions to foundation models
- **Compare Models Tab**: Side-by-side model comparison
- **Sample Queries Tab**: Pre-built example queries
- Real-time token usage and cost estimation
- Model selection and parameter tuning

#### 📚 RAG Pipeline Page
- **RAG Query Tab**: Ask questions with context retrieval
- **Document Chunking Tab**: Visualize document splitting
- **Batch Queries Tab**: Process multiple questions at once
- Source citations with relevance scores
- Context visualization

#### 🔬 Agent Framework Page
- **Create Trace Tab**: Simulate RAG execution and create traces
- **Analyze Traces Tab**: Performance analysis and recommendations
- **Agent Config Tab**: Generate agent configurations
- **MLflow Integration Tab**: Generate MLflow tracking code
- Visual metrics and charts

### Tips

- Use the **sidebar** to adjust parameters
- Click **expanders** for additional information
- Download generated configurations and code
- Monitor token usage and costs in real-time

---

## 💻 TUI (Text User Interface)

### Overview

The TUI provides a bash-style interactive terminal interface with rich formatting, perfect for command-line enthusiasts and automation.

### Launch

```bash
cd mosaic-ai-demo
cp .env.sample .env
# Edit .env with your credentials
./mosaic-ai.sh
```

Or directly with Python:

```bash
python3 cli.py
```

### Command Reference

#### Basic Commands

```bash
help                    # Show all available commands
menu                    # Display interactive menu
status                  # Show current configuration
samples                 # Display sample queries
clear                   # Clear screen
exit                    # Exit the application
```

#### Query Commands

```bash
query <text>            # Query foundation model
# Example: query What is Databricks Mosaic AI?

rag <question>          # Ask question using RAG pipeline
# Example: rag How does Vector Search work?

compare <text>          # Compare multiple models
# Example: compare Explain Delta Lake benefits

trace                   # Create and analyze agent trace
```

#### Configuration Commands

```bash
model <name>            # Switch model
# Options: llama8b, llama70b, mixtral
# Example: model llama70b

model                   # Show current model (no argument)
```

#### Menu Options

Type a number to select from the menu:

```
1 - Foundation Model APIs
2 - RAG Pipeline
3 - Agent Framework
4 - Compare Models
5 - Sample Queries
6 - Configuration
7 - Help
0 - Exit
```

### Features

- **Rich Formatting**: Colored output with panels and tables
- **Command History**: Use up/down arrows to navigate history
- **Auto-completion**: Tab completion for commands
- **Real-time Metrics**: Token usage and cost estimation
- **Source Citations**: View sources used in RAG responses
- **Trace Analysis**: Performance metrics and recommendations

### Example Session

```bash
mosaic-ai> help
# Shows all commands

mosaic-ai> status
# Shows current configuration

mosaic-ai> query What is Databricks Mosaic AI?
# Queries the default model

mosaic-ai> model llama70b
# Switches to Llama 70B model

mosaic-ai> rag How does Vector Search integrate with Delta tables?
# Uses RAG pipeline for contextual answer

mosaic-ai> compare Explain the benefits of using Lakeflow
# Compares responses from multiple models

mosaic-ai> trace
# Creates a sample trace and shows analysis

mosaic-ai> exit
# Exits the application
```

### Tips

- Use **Tab** for command completion
- Use **Up/Down arrows** for command history
- Type **menu** for a visual menu interface
- Type **samples** to see example queries
- Press **Ctrl+C** to cancel (won't exit)
- Type **exit** or **quit** to leave

---

## 🐍 Python Scripts

### Overview

Run individual components directly as Python scripts for maximum flexibility and integration with your own code.

### Usage

```bash
cd mosaic-ai-demo

# Foundation Model APIs
python src/model_serving.py

# Vector Search
python src/vector_search.py

# RAG Pipeline
python src/rag_pipeline.py

# AI Gateway
python src/ai_gateway.py

# Lakeflow Pipelines
python src/lakeflow_pipeline.py

# Agent Framework
python src/agent_framework.py
```

### Integration

Import modules in your own code:

```python
from src.model_serving import DatabricksModelServing
from src.rag_pipeline import RAGPipeline
from src.agent_framework import AgentFramework

# Initialize
model_client = DatabricksModelServing()
rag = RAGPipeline()
agent = AgentFramework()

# Use
result = model_client.query_model("Your question here")
rag_result = rag.query("Your question here")
trace = agent.trace_end_to_end(...)
```

---

## Comparison

| Feature | Web (Streamlit) | TUI (Terminal) | Python Scripts |
|---------|----------------|----------------|----------------|
| **Visual Interface** | ✅ Rich UI | ⚠️ Text-based | ❌ Code only |
| **Interactive** | ✅ Forms & buttons | ✅ Commands | ❌ Manual |
| **Charts & Graphs** | ✅ Yes | ❌ Tables only | ❌ No |
| **Automation** | ❌ Manual | ⚠️ Commands | ✅ Full |
| **Batch Processing** | ✅ Yes | ⚠️ Manual | ✅ Yes |
| **Learning Curve** | Easy | Medium | Advanced |
| **Best For** | Exploration | Quick queries | Integration |
| **Remote Access** | ✅ Yes (port forward) | ✅ SSH | ✅ Yes |

---

## Choosing the Right Interface

### Use **Web Interface (Streamlit)** when:
- You want visual feedback and charts
- You're exploring features for the first time
- You need to compare models side-by-side
- You want to adjust parameters with sliders
- You're demonstrating to others

### Use **TUI (Terminal)** when:
- You prefer command-line interfaces
- You're working over SSH
- You want quick queries without opening a browser
- You're comfortable with bash-style commands
- You want a lightweight interface

### Use **Python Scripts** when:
- You're integrating with your own code
- You need automation and batch processing
- You want to customize the behavior
- You're building a production application
- You need programmatic access

---

## Troubleshooting

### Web Interface Issues

**Port already in use:**
```bash
streamlit run Home.py --server.port 8502
```

**Can't access from remote:**
```bash
streamlit run Home.py --server.address 0.0.0.0
```

### TUI Issues

**Script not executable:**
```bash
chmod +x mosaic-ai.sh
```

**Virtual environment issues:**
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### General Issues

**Environment variables not loaded:**
```bash
# Make sure .env file exists
cp .env.sample .env
# Edit .env with your credentials
```

**Import errors:**
```bash
# Install dependencies
pip install -r requirements.txt
```

**Authentication errors:**
```bash
# Verify credentials in .env
cat .env
# Check that DATABRICKS_HOST and DATABRICKS_TOKEN are set correctly
```

---

## Next Steps

1. **Try all three interfaces** to find your preferred workflow
2. **Explore sample queries** to understand capabilities
3. **Experiment with parameters** to see how they affect results
4. **Read the component documentation** for advanced features
5. **Build your own applications** using the Python modules

---

For more information, see:
- [Main README](../README.md)
- [Setup Guide](setup_guide.md)
- [Component Summary](../COMPONENT_SUMMARY.md)
