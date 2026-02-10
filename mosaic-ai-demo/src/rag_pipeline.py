"""
Databricks Mosaic AI - RAG Pipeline Demo

This module demonstrates a complete RAG (Retrieval-Augmented Generation)
pipeline using Databricks Vector Search and Foundation Model APIs.
"""

import os
from typing import List, Dict, Optional
from dotenv import load_dotenv
from openai import OpenAI
import json

# Load environment variables
load_dotenv()


class RAGPipeline:
    """
    Complete RAG pipeline implementation using Databricks Mosaic AI.
    Combines Vector Search for retrieval and Foundation Models for generation.
    """
    
    def __init__(self):
        """Initialize the RAG pipeline with necessary clients."""
        self.databricks_token = os.getenv("DATABRICKS_TOKEN")
        self.databricks_host = os.getenv("DATABRICKS_HOST")
        
        if not self.databricks_token or not self.databricks_host:
            raise ValueError(
                "DATABRICKS_TOKEN and DATABRICKS_HOST must be set in environment variables"
            )
        
        # Initialize OpenAI client for LLM
        self.llm_client = OpenAI(
            api_key=self.databricks_token,
            base_url=f"{self.databricks_host}/serving-endpoints"
        )
        
        # Vector Search client would be initialized here
        # (using the DatabricksVectorSearch class from vector_search.py)
    
    def chunk_document(
        self,
        text: str,
        chunk_size: int = 500,
        overlap: int = 50
    ) -> List[Dict]:
        """
        Split a document into overlapping chunks for embedding.
        
        Args:
            text: The document text to chunk
            chunk_size: Size of each chunk in characters
            overlap: Number of overlapping characters between chunks
            
        Returns:
            List of chunk dictionaries with text and metadata
        """
        chunks = []
        start = 0
        chunk_id = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]
            
            chunks.append({
                "chunk_id": chunk_id,
                "text": chunk_text,
                "start_pos": start,
                "end_pos": end,
                "length": len(chunk_text)
            })
            
            start += chunk_size - overlap
            chunk_id += 1
        
        return chunks
    
    def retrieve_context(
        self,
        query: str,
        index_name: str,
        num_results: int = 3
    ) -> List[Dict]:
        """
        Retrieve relevant context from Vector Search index.
        
        Args:
            query: User query
            index_name: Name of the vector search index
            num_results: Number of relevant chunks to retrieve
            
        Returns:
            List of retrieved document chunks with scores
        """
        # In a real implementation, this would call the Vector Search API
        # For demo purposes, we'll return mock data
        
        mock_results = [
            {
                "text": "Databricks Mosaic AI provides a unified platform for building RAG applications. "
                        "It includes Vector Search for retrieval and Foundation Model APIs for generation.",
                "score": 0.92,
                "source": "databricks_docs.pdf",
                "page": 5
            },
            {
                "text": "Vector Search in Databricks automatically syncs with Delta tables, ensuring your "
                        "search index is always up-to-date with the latest data in your lakehouse.",
                "score": 0.87,
                "source": "databricks_docs.pdf",
                "page": 12
            },
            {
                "text": "The AI Gateway provides governance features like rate limiting, PII masking, "
                        "and toxicity filtering for all model calls in your organization.",
                "score": 0.81,
                "source": "databricks_docs.pdf",
                "page": 18
            }
        ]
        
        return mock_results[:num_results]
    
    def generate_answer(
        self,
        query: str,
        context_chunks: List[Dict],
        model: str = "databricks-llama-3-1-8b-instruct",
        temperature: float = 0.3
    ) -> Dict:
        """
        Generate an answer using retrieved context and LLM.
        
        Args:
            query: User query
            context_chunks: Retrieved context chunks
            model: Model endpoint name
            temperature: Sampling temperature
            
        Returns:
            Dictionary with answer and metadata
        """
        # Build context from retrieved chunks
        context_text = "\n\n".join([
            f"[Source: {chunk['source']}, Page: {chunk['page']}, Score: {chunk['score']:.2f}]\n{chunk['text']}"
            for chunk in context_chunks
        ])
        
        # Create prompt with context
        system_message = (
            "You are a helpful AI assistant. Answer the user's question based on the provided context. "
            "If the context doesn't contain enough information, say so. "
            "Always cite the sources you use in your answer."
        )
        
        user_message = f"""Context:
{context_text}

Question: {query}

Please provide a detailed answer based on the context above."""
        
        try:
            response = self.llm_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=temperature,
                max_tokens=500
            )
            
            return {
                "success": True,
                "query": query,
                "answer": response.choices[0].message.content,
                "model": model,
                "context_used": len(context_chunks),
                "sources": [
                    {"source": chunk["source"], "page": chunk["page"], "score": chunk["score"]}
                    for chunk in context_chunks
                ],
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
        
        except Exception as e:
            return {
                "success": False,
                "query": query,
                "error": str(e)
            }
    
    def query(
        self,
        question: str,
        index_name: str = "main.default.docs_index",
        num_context_chunks: int = 3,
        model: str = "databricks-llama-3-1-8b-instruct"
    ) -> Dict:
        """
        Complete RAG query: retrieve context and generate answer.
        
        Args:
            question: User question
            index_name: Vector search index name
            num_context_chunks: Number of context chunks to retrieve
            model: Model endpoint name
            
        Returns:
            Dictionary with answer, sources, and metadata
        """
        # Step 1: Retrieve relevant context
        context_chunks = self.retrieve_context(
            query=question,
            index_name=index_name,
            num_results=num_context_chunks
        )
        
        # Step 2: Generate answer with context
        result = self.generate_answer(
            query=question,
            context_chunks=context_chunks,
            model=model
        )
        
        return result
    
    def batch_query(
        self,
        questions: List[str],
        index_name: str = "main.default.docs_index"
    ) -> List[Dict]:
        """
        Process multiple questions in batch.
        
        Args:
            questions: List of user questions
            index_name: Vector search index name
            
        Returns:
            List of answer dictionaries
        """
        results = []
        
        for question in questions:
            print(f"Processing: {question}")
            result = self.query(question=question, index_name=index_name)
            results.append(result)
        
        return results


def main():
    """
    Main function demonstrating RAG pipeline capabilities.
    """
    print("=" * 80)
    print("Databricks Mosaic AI - RAG Pipeline Demo")
    print("=" * 80)
    print()
    
    # Initialize pipeline
    try:
        rag = RAGPipeline()
        print("✓ Successfully initialized RAG pipeline")
        print()
    except Exception as e:
        print(f"✗ Failed to initialize pipeline: {e}")
        return
    
    # Example 1: Document chunking
    print("-" * 80)
    print("Example 1: Document Chunking")
    print("-" * 80)
    
    sample_doc = """
    Databricks Mosaic AI is a comprehensive platform for building generative AI applications.
    It provides integrated tools for RAG, including Vector Search for retrieval and Foundation
    Model APIs for generation. The platform automatically syncs vector indexes with Delta tables,
    ensuring your search is always up-to-date. The AI Gateway adds governance features like
    rate limiting, PII masking, and content filtering.
    """
    
    chunks = rag.chunk_document(sample_doc, chunk_size=100, overlap=20)
    print(f"Split document into {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks[:3]):  # Show first 3
        print(f"\nChunk {i}:")
        print(f"  Text: {chunk['text'][:80]}...")
        print(f"  Length: {chunk['length']} characters")
    print()
    
    # Example 2: Single RAG query
    print("-" * 80)
    print("Example 2: RAG Query")
    print("-" * 80)
    
    question = "What is Databricks Mosaic AI and what features does it provide?"
    print(f"Question: {question}\n")
    
    result = rag.query(question=question)
    
    if result["success"]:
        print(f"Answer: {result['answer']}\n")
        print(f"Model used: {result['model']}")
        print(f"Context chunks used: {result['context_used']}")
        print(f"Total tokens: {result['usage']['total_tokens']}")
        print("\nSources:")
        for source in result['sources']:
            print(f"  - {source['source']} (Page {source['page']}, Score: {source['score']:.2f})")
    else:
        print(f"Error: {result['error']}")
    
    print()
    
    # Example 3: Batch queries
    print("-" * 80)
    print("Example 3: Batch RAG Queries")
    print("-" * 80)
    
    questions = [
        "How does Vector Search work in Databricks?",
        "What is the AI Gateway used for?",
        "What are the benefits of using Delta Lake with RAG?"
    ]
    
    print(f"Processing {len(questions)} questions...\n")
    results = rag.batch_query(questions)
    
    for i, result in enumerate(results):
        if result["success"]:
            print(f"\nQ{i+1}: {result['query']}")
            print(f"A{i+1}: {result['answer'][:150]}...")
            print(f"Tokens: {result['usage']['total_tokens']}")
    
    print()
    
    # RAG Pipeline Architecture
    print("-" * 80)
    print("RAG Pipeline Architecture")
    print("-" * 80)
    print()
    print("1. **Document Ingestion**")
    print("   - Load documents (PDFs, text files, web pages)")
    print("   - Chunk documents into manageable pieces")
    print("   - Store in Delta tables")
    print()
    print("2. **Embedding & Indexing**")
    print("   - Generate embeddings using embedding models")
    print("   - Create Vector Search index")
    print("   - Automatic sync with Delta tables")
    print()
    print("3. **Retrieval**")
    print("   - Convert user query to embedding")
    print("   - Search vector index for similar chunks")
    print("   - Rank and filter results")
    print()
    print("4. **Generation**")
    print("   - Combine query with retrieved context")
    print("   - Send to Foundation Model API")
    print("   - Generate contextual answer")
    print()
    print("5. **Governance (AI Gateway)**")
    print("   - Apply rate limiting")
    print("   - Mask PII in responses")
    print("   - Filter toxic content")
    print("   - Track usage and costs")
    print()
    
    # Best practices
    print("-" * 80)
    print("Best Practices for RAG")
    print("-" * 80)
    print()
    print("1. **Chunking Strategy**")
    print("   - Use 300-500 character chunks for most use cases")
    print("   - Add 50-100 character overlap to preserve context")
    print("   - Experiment with different sizes for your data")
    print()
    print("2. **Retrieval Optimization**")
    print("   - Start with 3-5 context chunks")
    print("   - Use hybrid search (keyword + vector) when available")
    print("   - Apply metadata filters to narrow search scope")
    print()
    print("3. **Prompt Engineering**")
    print("   - Clearly instruct the model to use provided context")
    print("   - Ask model to cite sources")
    print("   - Handle cases where context is insufficient")
    print()
    print("4. **Monitoring & Evaluation**")
    print("   - Use MLflow to track RAG pipeline performance")
    print("   - Monitor retrieval quality (relevance scores)")
    print("   - Evaluate answer quality with human feedback")
    print()
    print("5. **Cost Optimization**")
    print("   - Use smaller models (8B) for simple queries")
    print("   - Cache frequent queries")
    print("   - Implement query routing based on complexity")
    print()
    
    print("=" * 80)
    print("Demo completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    main()
