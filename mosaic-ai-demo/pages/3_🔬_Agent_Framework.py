"""
Databricks Mosaic AI Demo - Agent Framework Page
Interactive interface for agent tracing and monitoring
"""

import streamlit as st
import os
import sys
import json
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agent_framework import AgentFramework

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(page_title="Agent Framework", page_icon="🔬", layout="wide")

# Header
st.title("🔬 Mosaic AI Agent Framework")
st.markdown("Trace, monitor, and optimize your RAG applications with MLflow")

st.markdown("---")

# Initialize session state
if 'agent_framework' not in st.session_state:
    try:
        st.session_state.agent_framework = AgentFramework()
        st.session_state.initialized = True
        st.session_state.traces = []
    except Exception as e:
        st.session_state.initialized = False
        st.session_state.error = str(e)

# Check initialization
if not st.session_state.initialized:
    st.error(f"⚠️ **Configuration Error**: {st.session_state.error}")
    st.stop()

st.success("✅ Agent Framework initialized")

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Create Trace", "📊 Analyze Traces", "⚙️ Agent Config", "📈 MLflow Integration"])

# Tab 1: Create Trace
with tab1:
    st.markdown("### Simulate RAG Execution and Create Trace")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Query Configuration")
        query = st.text_input("User Query", value="What is Databricks Mosaic AI?")
        
        st.markdown("#### Retrieval Simulation")
        num_chunks = st.slider("Number of Chunks Retrieved", 1, 10, 3)
        retrieval_time = st.slider("Retrieval Time (ms)", 50, 500, 150)
        avg_score = st.slider("Average Relevance Score", 0.0, 1.0, 0.85, 0.05)
    
    with col2:
        st.markdown("#### Generation Simulation")
        answer_length = st.slider("Answer Length (chars)", 100, 1000, 300)
        generation_time = st.slider("Generation Time (ms)", 200, 1000, 450)
        prompt_tokens = st.slider("Prompt Tokens", 100, 1000, 350)
        completion_tokens = st.slider("Completion Tokens", 50, 500, 120)
    
    if st.button("🔬 Create Trace", type="primary"):
        # Simulate retrieval
        mock_chunks = [
            {
                "id": f"chunk_{i}",
                "score": avg_score + (0.1 - i * 0.02),
                "source": "docs.pdf",
                "text": f"Sample context chunk {i}..."
            }
            for i in range(num_chunks)
        ]
        
        retrieval_trace = st.session_state.agent_framework.trace_retrieval(
            query=query,
            retrieved_chunks=mock_chunks,
            retrieval_time_ms=retrieval_time
        )
        
        # Simulate generation
        answer = "Databricks Mosaic AI is a unified platform for building generative AI applications..."
        token_count = {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens
        }
        
        generation_trace = st.session_state.agent_framework.trace_generation(
            query=query,
            context="Sample context",
            generated_answer=answer,
            generation_time_ms=generation_time,
            token_count=token_count
        )
        
        # Create end-to-end trace
        total_time = retrieval_time + generation_time
        e2e_trace = st.session_state.agent_framework.trace_end_to_end(
            query=query,
            retrieval_trace=retrieval_trace,
            generation_trace=generation_trace,
            final_answer=answer,
            total_time_ms=total_time
        )
        
        st.session_state.traces.append(e2e_trace)
        
        st.success(f"✅ Trace created: {e2e_trace['trace_id']}")
        
        # Display trace
        with st.expander("View Trace Details"):
            st.json(e2e_trace)

# Tab 2: Analyze Traces
with tab2:
    st.markdown("### Trace Analysis and Recommendations")
    
    if len(st.session_state.traces) == 0:
        st.info("No traces available. Create some traces in the 'Create Trace' tab first.")
    else:
        st.success(f"📊 Analyzing {len(st.session_state.traces)} traces")
        
        # Run analysis
        analysis = st.session_state.agent_framework.analyze_traces(st.session_state.traces)
        
        # Summary metrics
        st.markdown("#### Performance Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Queries", analysis["summary"]["total_queries"])
        with col2:
            st.metric("Avg Latency (ms)", f"{analysis['summary']['avg_total_time_ms']:.1f}")
        with col3:
            st.metric("Avg Tokens", f"{analysis['summary']['avg_tokens_per_query']:.0f}")
        with col4:
            st.metric("Avg Retrieval Score", f"{analysis['summary']['avg_retrieval_score']:.3f}")
        
        st.markdown("---")
        
        # Detailed metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ⏱️ Latency Breakdown")
            st.metric("Retrieval Time", f"{analysis['summary']['avg_retrieval_time_ms']:.1f} ms")
            st.metric("Generation Time", f"{analysis['summary']['avg_generation_time_ms']:.1f} ms")
            
            # Latency chart
            import pandas as pd
            latency_data = pd.DataFrame({
                "Step": ["Retrieval", "Generation"],
                "Time (ms)": [
                    analysis['summary']['avg_retrieval_time_ms'],
                    analysis['summary']['avg_generation_time_ms']
                ]
            })
            st.bar_chart(latency_data.set_index("Step"))
        
        with col2:
            st.markdown("#### 🎯 Quality Indicators")
            st.metric("Slow Queries", analysis["issues"]["slow_queries_count"])
            st.metric("Low Quality Retrievals", analysis["issues"]["low_quality_retrievals_count"])
            
            if analysis["issues"]["slow_queries_count"] > 0:
                with st.expander("View Slow Queries"):
                    for sq in analysis["issues"]["slow_queries"]:
                        st.markdown(f"- **{sq['query']}** ({sq['time_ms']:.0f} ms)")
            
            if analysis["issues"]["low_quality_retrievals_count"] > 0:
                with st.expander("View Low Quality Retrievals"):
                    for lq in analysis["issues"]["low_quality_retrievals"]:
                        st.markdown(f"- **{lq['query']}** (score: {lq['score']:.3f})")
        
        # Recommendations
        if analysis["recommendations"]:
            st.markdown("---")
            st.markdown("#### 💡 Optimization Recommendations")
            for rec in analysis["recommendations"]:
                st.info(f"**Recommendation:** {rec}")
        else:
            st.success("✅ No issues detected! Your RAG pipeline is performing well.")
        
        # Clear traces button
        if st.button("🗑️ Clear All Traces"):
            st.session_state.traces = []
            st.rerun()

# Tab 3: Agent Configuration
with tab3:
    st.markdown("### Create Agent Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Basic Settings")
        agent_name = st.text_input("Agent Name", value="databricks_docs_assistant")
        vector_index = st.text_input("Vector Index", value="main.default.docs_index")
        llm_model = st.selectbox(
            "LLM Model",
            ["databricks-llama-3-1-8b-instruct", "databricks-llama-3-3-70b-instruct"]
        )
        num_chunks = st.slider("Context Chunks", 1, 10, 3)
    
    with col2:
        st.markdown("#### Generation Settings")
        temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.1)
        max_tokens = st.slider("Max Tokens", 100, 1000, 500, 50)
        
        st.markdown("#### Guardrails")
        pii_masking = st.checkbox("PII Masking", value=True)
        toxicity_filter = st.checkbox("Toxicity Filter", value=True)
        rate_limit = st.slider("Rate Limit (req/min)", 1, 100, 10)
    
    if st.button("⚙️ Generate Configuration", type="primary"):
        config = st.session_state.agent_framework.create_agent_config(
            agent_name=agent_name,
            vector_index=vector_index,
            llm_model=llm_model,
            num_context_chunks=num_chunks
        )
        
        # Update with user settings
        config["generator"]["temperature"] = temperature
        config["generator"]["max_tokens"] = max_tokens
        config["guardrails"]["pii_masking"] = pii_masking
        config["guardrails"]["toxicity_filter"] = toxicity_filter
        config["guardrails"]["rate_limit"] = rate_limit
        
        st.success("✅ Agent configuration generated")
        
        # Display configuration
        st.markdown("#### Configuration JSON")
        st.json(config)
        
        # Download button
        config_json = json.dumps(config, indent=2)
        st.download_button(
            label="📥 Download Configuration",
            data=config_json,
            file_name=f"{agent_name}_config.json",
            mime="application/json"
        )

# Tab 4: MLflow Integration
with tab4:
    st.markdown("### MLflow Integration")
    st.markdown("Generate code for logging your agent to MLflow")
    
    agent_name_mlflow = st.text_input("Agent Name", value="my_rag_agent", key="mlflow_agent")
    
    if st.button("📝 Generate MLflow Code", type="primary"):
        config = st.session_state.agent_framework.create_agent_config(
            agent_name=agent_name_mlflow,
            vector_index="main.default.docs_index",
            llm_model="databricks-llama-3-1-8b-instruct"
        )
        
        mlflow_code = st.session_state.agent_framework.generate_mlflow_code(config)
        
        st.success("✅ MLflow integration code generated")
        
        st.markdown("#### Python Code")
        st.code(mlflow_code, language="python")
        
        st.markdown("#### Instructions")
        st.markdown("""
        1. **Copy the code above** to your Python script
        2. **Replace `{{username}}`** with your Databricks username
        3. **Run the script** to log your agent to MLflow
        4. **View in MLflow UI**: Go to Experiments in your Databricks workspace
        5. **Compare runs**: Track different configurations and metrics
        6. **Register model**: Promote to Model Registry when ready
        """)
        
        # Download button
        st.download_button(
            label="📥 Download MLflow Code",
            data=mlflow_code,
            file_name="agent_mlflow_tracking.py",
            mime="text/x-python"
        )

# Information section
with st.expander("ℹ️ About Agent Framework"):
    st.markdown("""
    ### Mosaic AI Agent Framework
    
    The Agent Framework provides comprehensive tools for building, deploying, and monitoring RAG agents:
    
    **Key Features:**
    - **End-to-End Tracing**: Track every step of your RAG pipeline
    - **MLflow Integration**: Log experiments and track metrics
    - **Performance Analysis**: Identify bottlenecks and optimization opportunities
    - **Quality Monitoring**: Track retrieval scores and answer quality
    - **Production Deployment**: Deploy as Model Serving endpoints
    
    **What to Trace:**
    1. **Retrieval Metrics**: Chunks retrieved, scores, latency
    2. **Generation Metrics**: Tokens used, model, latency
    3. **Quality Indicators**: Relevance scores, answer length
    4. **Issues**: Slow queries, low-quality retrievals
    
    **Best Practices:**
    - Trace every query in production
    - Set up alerts for performance degradation
    - Analyze traces regularly to identify improvements
    - Use MLflow for experiment tracking
    - A/B test different configurations
    """)
