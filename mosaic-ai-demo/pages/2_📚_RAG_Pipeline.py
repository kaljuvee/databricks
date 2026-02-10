"""
Databricks Mosaic AI Demo - RAG Pipeline Page
Interactive interface for Retrieval-Augmented Generation
"""

import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from rag_pipeline import RAGPipeline

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(page_title="RAG Pipeline", page_icon="📚", layout="wide")

# Header
st.title("📚 RAG Pipeline")
st.markdown("Complete Retrieval-Augmented Generation with context and citations")

st.markdown("---")

# Initialize session state
if 'rag_pipeline' not in st.session_state:
    try:
        st.session_state.rag_pipeline = RAGPipeline()
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

st.success("✅ RAG Pipeline initialized successfully")

# Sidebar configuration
st.sidebar.header("⚙️ RAG Configuration")

# Chunking parameters
st.sidebar.subheader("Document Chunking")
chunk_size = st.sidebar.slider("Chunk Size (characters)", 200, 1000, 500, 50)
chunk_overlap = st.sidebar.slider("Chunk Overlap (characters)", 0, 200, 50, 10)

# Retrieval parameters
st.sidebar.subheader("Retrieval")
num_context_chunks = st.sidebar.slider("Number of Context Chunks", 1, 10, 3, 1)

# Generation parameters
st.sidebar.subheader("Generation")
model_options = {
    "Llama 3.1 8B": "databricks-llama-3-1-8b-instruct",
    "Llama 3.3 70B": "databricks-llama-3-3-70b-instruct",
}
selected_model_name = st.sidebar.selectbox("Model", options=list(model_options.keys()))
selected_model = model_options[selected_model_name]

temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.3, 0.1)

# Main content tabs
tab1, tab2, tab3 = st.tabs(["🔍 RAG Query", "📄 Document Chunking", "📊 Batch Queries"])

# Tab 1: RAG Query
with tab1:
    st.markdown("### Ask Questions with Context")
    st.markdown("The RAG pipeline retrieves relevant context and generates answers with citations")
    
    user_question = st.text_area(
        "Your Question",
        placeholder="e.g., What is Databricks Mosaic AI and what features does it provide?",
        height=100
    )
    
    if st.button("🚀 Query with RAG", type="primary"):
        if user_question:
            with st.spinner("Retrieving context and generating answer..."):
                result = st.session_state.rag_pipeline.query(
                    question=user_question,
                    num_context_chunks=num_context_chunks,
                    model=selected_model
                )
            
            if result["success"]:
                # Display answer
                st.markdown("### 🤖 Answer")
                st.markdown(result["answer"])
                
                st.markdown("---")
                
                # Display sources
                st.markdown("### 📚 Sources Used")
                for idx, source in enumerate(result["sources"], 1):
                    with st.expander(f"Source {idx}: {source['source']} (Page {source['page']})"):
                        st.markdown(f"**Relevance Score**: {source['score']:.2f}")
                        st.caption("This source was used to generate the answer above")
                
                # Metrics
                st.markdown("---")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Context Chunks", result["context_used"])
                with col2:
                    st.metric("Total Tokens", result["usage"]["total_tokens"])
                with col3:
                    st.metric("Model", selected_model_name)
                with col4:
                    input_cost = (result["usage"]["prompt_tokens"] / 1_000_000) * 0.15
                    output_cost = (result["usage"]["completion_tokens"] / 1_000_000) * 0.45
                    total_cost = input_cost + output_cost
                    st.metric("Est. Cost", f"${total_cost:.6f}")
            else:
                st.error(f"❌ Error: {result['error']}")
        else:
            st.warning("Please enter a question")

# Tab 2: Document Chunking
with tab2:
    st.markdown("### Document Chunking Demo")
    st.markdown("See how documents are split into overlapping chunks for embedding")
    
    sample_doc = st.text_area(
        "Document Text",
        value="""Databricks Mosaic AI is a comprehensive platform for building generative AI applications. It provides integrated tools for RAG, including Vector Search for retrieval and Foundation Model APIs for generation. The platform automatically syncs vector indexes with Delta tables, ensuring your search is always up-to-date. The AI Gateway adds governance features like rate limiting, PII masking, and content filtering.""",
        height=150
    )
    
    if st.button("✂️ Chunk Document"):
        chunks = st.session_state.rag_pipeline.chunk_document(
            text=sample_doc,
            chunk_size=chunk_size,
            overlap=chunk_overlap
        )
        
        st.success(f"✅ Document split into {len(chunks)} chunks")
        
        # Display chunks
        for idx, chunk in enumerate(chunks):
            with st.expander(f"Chunk {idx + 1} (Length: {chunk['length']} chars)"):
                st.markdown(f"**Position**: {chunk['start_pos']} - {chunk['end_pos']}")
                st.text(chunk['text'])
        
        # Visualization
        st.markdown("### 📊 Chunking Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Chunks", len(chunks))
        with col2:
            avg_length = sum(c['length'] for c in chunks) / len(chunks)
            st.metric("Avg Chunk Length", f"{avg_length:.0f}")
        with col3:
            st.metric("Overlap", f"{chunk_overlap} chars")

# Tab 3: Batch Queries
with tab3:
    st.markdown("### Batch Query Processing")
    st.markdown("Process multiple questions at once")
    
    # Predefined questions
    default_questions = [
        "How does Vector Search work in Databricks?",
        "What is the AI Gateway used for?",
        "What are the benefits of using Delta Lake with RAG?"
    ]
    
    st.markdown("**Questions to Process:**")
    questions = []
    for i in range(3):
        q = st.text_input(f"Question {i+1}", value=default_questions[i] if i < len(default_questions) else "", key=f"batch_q_{i}")
        if q:
            questions.append(q)
    
    if st.button("🔄 Process Batch", type="primary"):
        if questions:
            with st.spinner(f"Processing {len(questions)} questions..."):
                results = st.session_state.rag_pipeline.batch_query(
                    questions=questions,
                    index_name="main.default.docs_index"
                )
            
            st.success(f"✅ Processed {len(results)} questions")
            
            # Display results
            for idx, result in enumerate(results, 1):
                with st.expander(f"Q{idx}: {result['query'][:50]}..."):
                    if result["success"]:
                        st.markdown("**Answer:**")
                        st.markdown(result["answer"])
                        st.caption(f"Tokens: {result['usage']['total_tokens']} | Sources: {len(result['sources'])}")
                    else:
                        st.error(f"Error: {result.get('error', 'Unknown error')}")
        else:
            st.warning("Please enter at least one question")

# Sample queries section
st.markdown("---")
st.markdown("### 💡 Sample RAG Queries")

sample_queries = {
    "Platform Overview": "What is Databricks Mosaic AI and what features does it provide?",
    "Vector Search": "How does Vector Search integrate with Delta tables?",
    "AI Gateway": "What governance features does the AI Gateway provide?",
    "Lakeflow": "How do Lakeflow pipelines automate document processing?",
    "Agent Framework": "What is the Mosaic AI Agent Framework used for?",
}

cols = st.columns(3)
for idx, (title, query) in enumerate(sample_queries.items()):
    with cols[idx % 3]:
        if st.button(f"📝 {title}", key=f"sample_{title}", use_container_width=True):
            st.session_state.sample_query = query
            st.rerun()

# Process sample query if selected
if 'sample_query' in st.session_state:
    st.markdown("---")
    st.markdown(f"**Running Sample Query:** {st.session_state.sample_query}")
    
    with st.spinner("Processing..."):
        result = st.session_state.rag_pipeline.query(
            question=st.session_state.sample_query,
            num_context_chunks=num_context_chunks,
            model=selected_model
        )
    
    if result["success"]:
        st.markdown("### Answer")
        st.markdown(result["answer"])
        st.caption(f"Tokens: {result['usage']['total_tokens']} | Sources: {len(result['sources'])}")
    
    # Clear sample query
    del st.session_state.sample_query

# Information section
with st.expander("ℹ️ About RAG Pipeline"):
    st.markdown("""
    ### Retrieval-Augmented Generation (RAG)
    
    RAG combines retrieval and generation to provide accurate, contextual answers:
    
    **Pipeline Steps:**
    1. **Document Chunking**: Split documents into manageable pieces with overlap
    2. **Embedding**: Convert chunks to vector representations
    3. **Retrieval**: Find most relevant chunks for a query
    4. **Generation**: Use retrieved context to generate accurate answers
    
    **Key Benefits:**
    - **Accuracy**: Grounds answers in your actual data
    - **Citations**: Provides source references
    - **Up-to-date**: Uses latest data from Delta tables
    - **Scalable**: Handles large document collections
    
    **Best Practices:**
    - Use 300-500 character chunks for most use cases
    - Add 50-100 character overlap to preserve context
    - Retrieve 3-5 context chunks per query
    - Use lower temperature (0.3) for factual answers
    - Monitor retrieval scores to ensure quality
    """)
