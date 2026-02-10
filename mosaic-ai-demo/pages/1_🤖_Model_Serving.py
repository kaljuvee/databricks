"""
Databricks Mosaic AI Demo - Model Serving Page
Interactive interface for Foundation Model APIs
"""

import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from model_serving import DatabricksModelServing

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(page_title="Model Serving", page_icon="🤖", layout="wide")

# Header
st.title("🤖 Foundation Model APIs")
st.markdown("Query state-of-the-art open models through OpenAI-compatible APIs")

st.markdown("---")

# Initialize session state
if 'model_client' not in st.session_state:
    try:
        st.session_state.model_client = DatabricksModelServing()
        st.session_state.initialized = True
    except Exception as e:
        st.session_state.initialized = False
        st.session_state.error = str(e)

# Check initialization
if not st.session_state.initialized:
    st.error(f"⚠️ **Configuration Error**: {st.session_state.error}")
    st.info("""
    **Setup Required:**
    1. Set `DATABRICKS_HOST` in your `.env` file
    2. Set `DATABRICKS_TOKEN` in your `.env` file
    3. Restart the Streamlit app
    """)
    st.stop()

st.success("✅ Connected to Databricks Model Serving")

# Sidebar configuration
st.sidebar.header("⚙️ Configuration")

# Model selection
model_options = {
    "Llama 3.1 8B (Fastest, Cheapest)": "databricks-llama-3-1-8b-instruct",
    "Llama 3.3 70B (Balanced)": "databricks-llama-3-3-70b-instruct",
    "Mixtral 8x7B": "databricks-mixtral-8x7b-instruct",
}

selected_model_name = st.sidebar.selectbox(
    "Select Model",
    options=list(model_options.keys()),
    index=0
)
selected_model = model_options[selected_model_name]

# Parameters
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
max_tokens = st.sidebar.slider("Max Tokens", 100, 1000, 500, 50)

# System message
use_system_message = st.sidebar.checkbox("Use System Message", value=False)
system_message = None
if use_system_message:
    system_message = st.sidebar.text_area(
        "System Message",
        value="You are a helpful AI assistant specializing in data engineering and Databricks.",
        height=100
    )

st.sidebar.markdown("---")
st.sidebar.markdown("### 💰 Pricing")
st.sidebar.markdown(f"""
**{selected_model_name}**
- Input: $0.15-2.00 per 1M tokens
- Output: $0.45-6.00 per 1M tokens
""")

# Main content tabs
tab1, tab2, tab3 = st.tabs(["💬 Query", "📊 Compare Models", "📝 Sample Queries"])

# Tab 1: Single Query
with tab1:
    st.markdown("### Ask a Question")
    
    user_query = st.text_area(
        "Your Question",
        placeholder="e.g., What is Retrieval-Augmented Generation (RAG)?",
        height=100,
        key="query_input"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        query_button = st.button("🚀 Submit Query", type="primary", use_container_width=True)
    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.rerun()
    
    if query_button and user_query:
        with st.spinner(f"Querying {selected_model_name}..."):
            result = st.session_state.model_client.query_model(
                prompt=user_query,
                model=selected_model,
                max_tokens=max_tokens,
                temperature=temperature,
                system_message=system_message
            )
        
        if result["success"]:
            st.markdown("### 🤖 Response")
            st.markdown(result["response"])
            
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Model", selected_model_name.split()[0])
            with col2:
                st.metric("Total Tokens", result["usage"]["total_tokens"])
            with col3:
                st.metric("Prompt Tokens", result["usage"]["prompt_tokens"])
            with col4:
                st.metric("Completion Tokens", result["usage"]["completion_tokens"])
            
            # Cost estimation
            input_cost = (result["usage"]["prompt_tokens"] / 1_000_000) * 0.15
            output_cost = (result["usage"]["completion_tokens"] / 1_000_000) * 0.45
            total_cost = input_cost + output_cost
            
            st.info(f"💰 **Estimated Cost**: ${total_cost:.6f} USD")
        else:
            st.error(f"❌ Error: {result['error']}")

# Tab 2: Model Comparison
with tab2:
    st.markdown("### Compare Multiple Models")
    st.markdown("Query multiple models simultaneously and compare their responses")
    
    comparison_query = st.text_area(
        "Your Question",
        placeholder="e.g., Explain Delta Lake in one sentence.",
        height=100,
        key="comparison_input"
    )
    
    models_to_compare = st.multiselect(
        "Select Models to Compare",
        options=list(model_options.keys()),
        default=[list(model_options.keys())[0]]
    )
    
    if st.button("🔍 Compare Models", type="primary") and comparison_query and models_to_compare:
        selected_models = [model_options[name] for name in models_to_compare]
        
        with st.spinner("Querying models..."):
            results = st.session_state.model_client.compare_models(
                prompt=comparison_query,
                models=selected_models,
                system_message=system_message
            )
        
        # Display results side by side
        cols = st.columns(len(results))
        
        for idx, (col, result) in enumerate(zip(cols, results)):
            with col:
                if result["success"]:
                    st.markdown(f"#### {models_to_compare[idx]}")
                    st.markdown(result["response"])
                    st.caption(f"Tokens: {result['usage']['total_tokens']}")
                else:
                    st.error(f"Error: {result['error']}")

# Tab 3: Sample Queries
with tab3:
    st.markdown("### 📝 Try These Sample Queries")
    
    sample_queries = {
        "RAG Explanation": "Explain what Retrieval-Augmented Generation (RAG) is in 2-3 sentences.",
        "Delta Lake Benefits": "What are the key benefits of using Delta Lake?",
        "Vector Search": "How does Vector Search work in Databricks?",
        "MLflow Overview": "What is MLflow and why is it useful?",
        "Lakeflow Pipelines": "Explain Lakeflow pipelines and their use in data processing.",
        "Cost Optimization": "What are best practices for optimizing costs when using Foundation Model APIs?"
    }
    
    for title, query in sample_queries.items():
        with st.expander(f"💡 {title}"):
            st.code(query, language=None)
            if st.button(f"Run: {title}", key=f"sample_{title}"):
                with st.spinner("Processing..."):
                    result = st.session_state.model_client.query_model(
                        prompt=query,
                        model=selected_model,
                        max_tokens=max_tokens,
                        temperature=temperature
                    )
                
                if result["success"]:
                    st.markdown("**Response:**")
                    st.markdown(result["response"])
                    st.caption(f"Tokens used: {result['usage']['total_tokens']}")
                else:
                    st.error(f"Error: {result['error']}")

# Information section
with st.expander("ℹ️ About Model Serving"):
    st.markdown("""
    ### Foundation Model APIs
    
    Databricks provides access to state-of-the-art open models through a unified, OpenAI-compatible API:
    
    **Available Models:**
    - **Llama 3.1 8B**: Fast and cost-effective for simple tasks
    - **Llama 3.3 70B**: Balanced performance for most use cases
    - **Llama 3.1 405B**: Most capable for complex reasoning
    - **Mixtral 8x7B**: Efficient mixture-of-experts architecture
    - **DBRX**: Databricks' own foundation model
    
    **Features:**
    - OpenAI-compatible API interface
    - Streaming responses
    - Pay-per-token pricing
    - Scale-to-zero endpoints
    - Enterprise security and governance
    
    **Use Cases:**
    - Question answering
    - Text summarization
    - Code generation
    - Content creation
    - RAG applications
    """)
