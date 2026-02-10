"""
Databricks Mosaic AI Demo - Streamlit Application
Main entry point for the web interface
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Databricks Mosaic AI Demo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #FF3621;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #FF3621;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stButton>button {
        background-color: #FF3621;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Check environment configuration
def check_config():
    """Check if required environment variables are set."""
    host = os.getenv("DATABRICKS_HOST")
    token = os.getenv("DATABRICKS_TOKEN")
    
    if not host or not token:
        st.error("⚠️ **Configuration Required**")
        st.warning("""
        Please set up your environment variables:
        1. Copy `.env.sample` to `.env`
        2. Add your `DATABRICKS_HOST` and `DATABRICKS_TOKEN`
        3. Restart the Streamlit app
        """)
        return False
    return True

# Main page content
def main():
    # Header
    st.markdown('<div class="main-header">🤖 Databricks Mosaic AI Demo</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Explore the Power of Unified Generative AI</div>', unsafe_allow_html=True)
    
    # Configuration check
    config_ok = check_config()
    
    if config_ok:
        st.success("✅ Configuration loaded successfully!")
    
    st.markdown("---")
    
    # Introduction
    st.markdown("""
    ## Welcome to the Databricks Mosaic AI Demo
    
    This interactive application demonstrates the complete suite of Databricks Mosaic AI capabilities 
    for building production-ready RAG (Retrieval-Augmented Generation) applications.
    
    ### 🚀 What You Can Explore
    """)
    
    # Feature cards in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h3>🤖 Foundation Models</h3>
            <p>Access Llama, Mixtral, and DBRX models through OpenAI-compatible APIs</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h3>🔍 Vector Search</h3>
            <p>Serverless vector database with automatic Delta table synchronization</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h3>📚 RAG Pipeline</h3>
            <p>Complete retrieval-augmented generation with context and citations</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h3>🛡️ AI Gateway</h3>
            <p>Governance with PII masking, rate limiting, and toxicity filtering</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-box">
            <h3>🔄 Lakeflow Pipelines</h3>
            <p>Automated document processing with Delta Live Tables</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h3>🔬 Agent Framework</h3>
            <p>MLflow-based tracing and performance monitoring</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick stats
    st.markdown("### 📊 Platform Highlights")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h2>6</h2>
            <p>Core Components</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h2>$0.15</h2>
            <p>Per 1M Tokens (Llama 8B)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h2>100%</h2>
            <p>RAG Coverage</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h2>∞</h2>
            <p>Scale to Zero</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Getting started
    st.markdown("### 🎯 Getting Started")
    
    st.markdown("""
    **Choose a feature from the sidebar** to explore:
    
    1. **Model Serving** - Query foundation models and compare responses
    2. **Vector Search** - Create indexes and perform similarity search
    3. **RAG Pipeline** - Build complete retrieval-augmented generation
    4. **AI Gateway** - Apply governance and security features
    5. **Lakeflow** - Automate document processing pipelines
    6. **Agent Framework** - Trace and optimize your RAG applications
    
    Each page includes interactive demos, sample queries, and real-time results!
    """)
    
    # Pricing information
    with st.expander("💰 Pricing Information"):
        st.markdown("""
        | Model | Input (per 1M tokens) | Output (per 1M tokens) |
        |-------|----------------------|------------------------|
        | Llama 3.1 8B | $0.15 | $0.45 |
        | Llama 3.3 70B | $0.50 | $1.50 |
        | Llama 3.1 405B | $2.00 | $6.00 |
        
        **Cost Optimization Tips:**
        - Start with Llama 3.1 8B for development
        - Use model routing for different query complexities
        - Enable scale-to-zero for endpoints
        - Monitor usage with built-in tracking
        """)
    
    # Documentation links
    with st.expander("📚 Documentation & Resources"):
        st.markdown("""
        - [Databricks Mosaic AI Documentation](https://docs.databricks.com/en/generative-ai/generative-ai.html)
        - [Model Serving Guide](https://docs.databricks.com/en/machine-learning/model-serving/index.html)
        - [Vector Search Guide](https://docs.databricks.com/en/generative-ai/vector-search.html)
        - [RAG Tutorial](https://docs.databricks.com/en/generative-ai/tutorials/ai-cookbook/index.html)
        - [GitHub Repository](https://github.com/kaljuvee/databricks)
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        Built with Databricks Mosaic AI | <a href="https://github.com/kaljuvee/databricks" target="_blank">View on GitHub</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
