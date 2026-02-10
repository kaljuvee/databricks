"""
Databricks Mosaic AI - Agent Framework Demo

This module demonstrates how to use the Mosaic AI Agent Framework
for building, deploying, and tracing RAG agents with MLflow.
"""

import os
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
from datetime import datetime
import json

# Load environment variables
load_dotenv()


class AgentFramework:
    """
    Mosaic AI Agent Framework for building and tracing RAG agents.
    Integrates with MLflow for experiment tracking and model registry.
    """
    
    def __init__(self):
        """Initialize the Agent Framework."""
        self.databricks_token = os.getenv("DATABRICKS_TOKEN")
        self.databricks_host = os.getenv("DATABRICKS_HOST")
        
        if not self.databricks_token or not self.databricks_host:
            raise ValueError(
                "DATABRICKS_TOKEN and DATABRICKS_HOST must be set in environment variables"
            )
        
        # Trace storage
        self.traces = []
    
    def create_agent_config(
        self,
        agent_name: str,
        vector_index: str,
        llm_model: str = "databricks-llama-3-1-8b-instruct",
        num_context_chunks: int = 3
    ) -> Dict:
        """
        Create an agent configuration.
        
        Args:
            agent_name: Name of the agent
            vector_index: Vector Search index name
            llm_model: LLM model endpoint
            num_context_chunks: Number of context chunks to retrieve
            
        Returns:
            Agent configuration dictionary
        """
        config = {
            "agent_name": agent_name,
            "version": "1.0.0",
            "retriever": {
                "type": "vector_search",
                "index_name": vector_index,
                "num_results": num_context_chunks,
                "similarity_threshold": 0.7
            },
            "generator": {
                "type": "foundation_model",
                "model": llm_model,
                "temperature": 0.3,
                "max_tokens": 500
            },
            "prompt_template": {
                "system": "You are a helpful AI assistant. Answer questions based on the provided context.",
                "user": "Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
            },
            "guardrails": {
                "pii_masking": True,
                "toxicity_filter": True,
                "rate_limit": 10
            },
            "tracing": {
                "enabled": True,
                "log_inputs": True,
                "log_outputs": True,
                "log_retrieval": True
            }
        }
        
        return config
    
    def trace_retrieval(
        self,
        query: str,
        retrieved_chunks: List[Dict],
        retrieval_time_ms: float
    ) -> Dict:
        """
        Trace the retrieval step of RAG.
        
        Args:
            query: User query
            retrieved_chunks: Retrieved document chunks
            retrieval_time_ms: Retrieval latency in milliseconds
            
        Returns:
            Retrieval trace dictionary
        """
        trace = {
            "step": "retrieval",
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "num_chunks_retrieved": len(retrieved_chunks),
            "chunks": [
                {
                    "chunk_id": chunk.get("id", "unknown"),
                    "score": chunk.get("score", 0.0),
                    "source": chunk.get("source", "unknown"),
                    "text_preview": chunk.get("text", "")[:100] + "..."
                }
                for chunk in retrieved_chunks
            ],
            "metrics": {
                "retrieval_time_ms": retrieval_time_ms,
                "avg_score": sum(c.get("score", 0) for c in retrieved_chunks) / len(retrieved_chunks) if retrieved_chunks else 0,
                "min_score": min((c.get("score", 0) for c in retrieved_chunks), default=0),
                "max_score": max((c.get("score", 0) for c in retrieved_chunks), default=0)
            }
        }
        
        return trace
    
    def trace_generation(
        self,
        query: str,
        context: str,
        generated_answer: str,
        generation_time_ms: float,
        token_count: Dict
    ) -> Dict:
        """
        Trace the generation step of RAG.
        
        Args:
            query: User query
            context: Retrieved context
            generated_answer: Generated answer
            generation_time_ms: Generation latency in milliseconds
            token_count: Token usage statistics
            
        Returns:
            Generation trace dictionary
        """
        trace = {
            "step": "generation",
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "context_length": len(context),
            "answer": generated_answer,
            "answer_length": len(generated_answer),
            "metrics": {
                "generation_time_ms": generation_time_ms,
                "prompt_tokens": token_count.get("prompt_tokens", 0),
                "completion_tokens": token_count.get("completion_tokens", 0),
                "total_tokens": token_count.get("total_tokens", 0),
                "tokens_per_second": token_count.get("completion_tokens", 0) / (generation_time_ms / 1000) if generation_time_ms > 0 else 0
            }
        }
        
        return trace
    
    def trace_end_to_end(
        self,
        query: str,
        retrieval_trace: Dict,
        generation_trace: Dict,
        final_answer: str,
        total_time_ms: float
    ) -> Dict:
        """
        Create an end-to-end trace for the complete RAG pipeline.
        
        Args:
            query: User query
            retrieval_trace: Retrieval step trace
            generation_trace: Generation step trace
            final_answer: Final answer
            total_time_ms: Total pipeline latency
            
        Returns:
            Complete trace dictionary
        """
        trace = {
            "trace_id": f"trace_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "answer": final_answer,
            "steps": [
                retrieval_trace,
                generation_trace
            ],
            "metrics": {
                "total_time_ms": total_time_ms,
                "retrieval_time_ms": retrieval_trace["metrics"]["retrieval_time_ms"],
                "generation_time_ms": generation_trace["metrics"]["generation_time_ms"],
                "num_chunks_used": retrieval_trace["num_chunks_retrieved"],
                "total_tokens": generation_trace["metrics"]["total_tokens"]
            },
            "quality_indicators": {
                "avg_retrieval_score": retrieval_trace["metrics"]["avg_score"],
                "context_relevance": "high" if retrieval_trace["metrics"]["avg_score"] > 0.8 else "medium" if retrieval_trace["metrics"]["avg_score"] > 0.6 else "low",
                "answer_length": len(final_answer),
                "latency_category": "fast" if total_time_ms < 1000 else "medium" if total_time_ms < 3000 else "slow"
            }
        }
        
        self.traces.append(trace)
        return trace
    
    def analyze_traces(self, traces: Optional[List[Dict]] = None) -> Dict:
        """
        Analyze traces to identify issues and optimization opportunities.
        
        Args:
            traces: List of traces to analyze (uses stored traces if None)
            
        Returns:
            Analysis results dictionary
        """
        if traces is None:
            traces = self.traces
        
        if not traces:
            return {"error": "No traces available for analysis"}
        
        # Calculate aggregate metrics
        total_queries = len(traces)
        avg_total_time = sum(t["metrics"]["total_time_ms"] for t in traces) / total_queries
        avg_retrieval_time = sum(t["metrics"]["retrieval_time_ms"] for t in traces) / total_queries
        avg_generation_time = sum(t["metrics"]["generation_time_ms"] for t in traces) / total_queries
        avg_tokens = sum(t["metrics"]["total_tokens"] for t in traces) / total_queries
        avg_retrieval_score = sum(t["quality_indicators"]["avg_retrieval_score"] for t in traces) / total_queries
        
        # Identify slow queries
        slow_queries = [
            t for t in traces
            if t["metrics"]["total_time_ms"] > avg_total_time * 1.5
        ]
        
        # Identify low-quality retrievals
        low_quality_retrievals = [
            t for t in traces
            if t["quality_indicators"]["avg_retrieval_score"] < 0.6
        ]
        
        analysis = {
            "summary": {
                "total_queries": total_queries,
                "avg_total_time_ms": round(avg_total_time, 2),
                "avg_retrieval_time_ms": round(avg_retrieval_time, 2),
                "avg_generation_time_ms": round(avg_generation_time, 2),
                "avg_tokens_per_query": round(avg_tokens, 2),
                "avg_retrieval_score": round(avg_retrieval_score, 3)
            },
            "issues": {
                "slow_queries_count": len(slow_queries),
                "slow_queries": [
                    {
                        "query": t["query"][:50] + "...",
                        "time_ms": t["metrics"]["total_time_ms"]
                    }
                    for t in slow_queries[:5]  # Top 5
                ],
                "low_quality_retrievals_count": len(low_quality_retrievals),
                "low_quality_retrievals": [
                    {
                        "query": t["query"][:50] + "...",
                        "score": t["quality_indicators"]["avg_retrieval_score"]
                    }
                    for t in low_quality_retrievals[:5]  # Top 5
                ]
            },
            "recommendations": []
        }
        
        # Generate recommendations
        if avg_retrieval_time > avg_generation_time * 2:
            analysis["recommendations"].append(
                "Retrieval is slower than generation. Consider optimizing vector index or reducing num_results."
            )
        
        if avg_retrieval_score < 0.7:
            analysis["recommendations"].append(
                "Average retrieval score is low. Consider improving document chunking or using a better embedding model."
            )
        
        if avg_tokens > 2000:
            analysis["recommendations"].append(
                "High token usage detected. Consider reducing context size or using a smaller model for simple queries."
            )
        
        if len(slow_queries) > total_queries * 0.2:
            analysis["recommendations"].append(
                "More than 20% of queries are slow. Consider caching frequent queries or optimizing the pipeline."
            )
        
        return analysis
    
    def generate_mlflow_code(self, agent_config: Dict) -> str:
        """
        Generate MLflow code for logging and tracking the agent.
        
        Args:
            agent_config: Agent configuration
            
        Returns:
            Python code for MLflow integration
        """
        code = f'''
import mlflow
from mlflow.models import infer_signature
import pandas as pd

# Set MLflow tracking URI (uses workspace default if not set)
mlflow.set_tracking_uri("databricks")

# Create or get experiment
experiment_name = "/Users/{{{{username}}}}/rag-agent-experiments"
mlflow.set_experiment(experiment_name)

# Start MLflow run
with mlflow.start_run(run_name="{agent_config['agent_name']}") as run:
    
    # Log parameters
    mlflow.log_param("agent_name", "{agent_config['agent_name']}")
    mlflow.log_param("vector_index", "{agent_config['retriever']['index_name']}")
    mlflow.log_param("llm_model", "{agent_config['generator']['model']}")
    mlflow.log_param("num_context_chunks", {agent_config['retriever']['num_results']})
    mlflow.log_param("temperature", {agent_config['generator']['temperature']})
    
    # Log the full agent configuration
    mlflow.log_dict(agent_config, "agent_config.json")
    
    # Example: Log metrics from traces
    # (In production, these would come from actual agent execution)
    mlflow.log_metric("avg_retrieval_time_ms", 150.5)
    mlflow.log_metric("avg_generation_time_ms", 450.2)
    mlflow.log_metric("avg_total_time_ms", 600.7)
    mlflow.log_metric("avg_retrieval_score", 0.85)
    mlflow.log_metric("avg_tokens_per_query", 450)
    
    # Log tags for organization
    mlflow.set_tag("agent_type", "rag")
    mlflow.set_tag("version", "{agent_config['version']}")
    mlflow.set_tag("environment", "development")
    
    # Example: Log a sample trace as artifact
    sample_trace = {{
        "query": "What is Databricks Mosaic AI?",
        "retrieval": {{"num_chunks": 3, "avg_score": 0.85}},
        "generation": {{"tokens": 450, "time_ms": 450}},
        "answer": "Databricks Mosaic AI is..."
    }}
    mlflow.log_dict(sample_trace, "sample_trace.json")
    
    print(f"MLflow run ID: {{run.info.run_id}}")
    print(f"Experiment ID: {{run.info.experiment_id}}")
    print(f"Artifact URI: {{run.info.artifact_uri}}")

# Register the agent as a model (optional)
# model_name = "{agent_config['agent_name']}"
# mlflow.register_model(f"runs:/{{run.info.run_id}}/model", model_name)
'''
        return code


def main():
    """
    Main function demonstrating Agent Framework capabilities.
    """
    print("=" * 80)
    print("Databricks Mosaic AI - Agent Framework Demo")
    print("=" * 80)
    print()
    
    # Initialize framework
    try:
        framework = AgentFramework()
        print("✓ Successfully initialized Agent Framework")
        print()
    except Exception as e:
        print(f"✗ Failed to initialize framework: {e}")
        return
    
    # Example 1: Create agent configuration
    print("-" * 80)
    print("Example 1: Agent Configuration")
    print("-" * 80)
    
    agent_config = framework.create_agent_config(
        agent_name="databricks_docs_assistant",
        vector_index="main.default.docs_index",
        llm_model="databricks-llama-3-1-8b-instruct",
        num_context_chunks=3
    )
    
    print("Agent Configuration:")
    print(json.dumps(agent_config, indent=2))
    print()
    
    # Example 2: Trace retrieval step
    print("-" * 80)
    print("Example 2: Trace Retrieval Step")
    print("-" * 80)
    
    query = "What is Databricks Mosaic AI?"
    mock_chunks = [
        {"id": "chunk_1", "score": 0.92, "source": "docs.pdf", "text": "Databricks Mosaic AI provides..."},
        {"id": "chunk_2", "score": 0.87, "source": "docs.pdf", "text": "Vector Search integrates..."},
        {"id": "chunk_3", "score": 0.81, "source": "docs.pdf", "text": "The AI Gateway provides..."}
    ]
    
    retrieval_trace = framework.trace_retrieval(query, mock_chunks, 145.3)
    print("Retrieval Trace:")
    print(json.dumps(retrieval_trace, indent=2))
    print()
    
    # Example 3: Trace generation step
    print("-" * 80)
    print("Example 3: Trace Generation Step")
    print("-" * 80)
    
    context = "\n\n".join([c["text"] for c in mock_chunks])
    answer = "Databricks Mosaic AI is a unified platform for building generative AI applications..."
    token_count = {"prompt_tokens": 350, "completion_tokens": 120, "total_tokens": 470}
    
    generation_trace = framework.trace_generation(query, context, answer, 425.7, token_count)
    print("Generation Trace:")
    print(json.dumps(generation_trace, indent=2))
    print()
    
    # Example 4: End-to-end trace
    print("-" * 80)
    print("Example 4: End-to-End Trace")
    print("-" * 80)
    
    e2e_trace = framework.trace_end_to_end(
        query, retrieval_trace, generation_trace, answer, 571.0
    )
    
    print("End-to-End Trace:")
    print(json.dumps(e2e_trace, indent=2))
    print()
    
    # Example 5: Simulate multiple queries and analyze
    print("-" * 80)
    print("Example 5: Trace Analysis")
    print("-" * 80)
    
    # Simulate a few more traces
    for i in range(4):
        mock_query = f"Sample query {i+1}"
        mock_retrieval = framework.trace_retrieval(mock_query, mock_chunks, 150 + i*20)
        mock_generation = framework.trace_generation(mock_query, context, answer, 400 + i*50, token_count)
        framework.trace_end_to_end(mock_query, mock_retrieval, mock_generation, answer, 550 + i*70)
    
    analysis = framework.analyze_traces()
    print("Trace Analysis:")
    print(json.dumps(analysis, indent=2))
    print()
    
    # Example 6: MLflow integration
    print("-" * 80)
    print("Example 6: MLflow Integration Code")
    print("-" * 80)
    
    mlflow_code = framework.generate_mlflow_code(agent_config)
    print("Generated MLflow code (first 500 characters):")
    print(mlflow_code[:500] + "...")
    print()
    print("Full code saved to: agent_mlflow_tracking.py")
    
    with open("agent_mlflow_tracking.py", "w") as f:
        f.write(mlflow_code)
    
    # Agent Framework Architecture
    print("-" * 80)
    print("Agent Framework Architecture")
    print("-" * 80)
    print()
    print("Components:")
    print()
    print("1. **Agent Configuration**")
    print("   - Define retriever and generator settings")
    print("   - Configure guardrails and policies")
    print("   - Set prompt templates")
    print()
    print("2. **Tracing System**")
    print("   - Trace each step of RAG pipeline")
    print("   - Capture inputs, outputs, and metrics")
    print("   - Enable debugging and optimization")
    print()
    print("3. **MLflow Integration**")
    print("   - Log experiments and parameters")
    print("   - Track metrics over time")
    print("   - Register and version agents")
    print()
    print("4. **Analysis Engine**")
    print("   - Analyze traces for issues")
    print("   - Generate recommendations")
    print("   - Identify optimization opportunities")
    print()
    print("5. **Deployment**")
    print("   - Deploy agents as Model Serving endpoints")
    print("   - Enable A/B testing")
    print("   - Monitor production performance")
    print()
    
    # Best practices
    print("-" * 80)
    print("Agent Framework Best Practices")
    print("-" * 80)
    print()
    print("1. **Comprehensive Tracing**")
    print("   - Trace every step of the pipeline")
    print("   - Log inputs, outputs, and intermediate results")
    print("   - Include timing and token metrics")
    print()
    print("2. **Quality Monitoring**")
    print("   - Track retrieval scores")
    print("   - Monitor answer quality")
    print("   - Set up alerts for degradation")
    print()
    print("3. **Experiment Tracking**")
    print("   - Use MLflow for all experiments")
    print("   - Compare different configurations")
    print("   - Version control agent definitions")
    print()
    print("4. **Performance Optimization**")
    print("   - Analyze slow queries")
    print("   - Optimize retrieval parameters")
    print("   - Cache frequent queries")
    print()
    print("5. **Production Deployment**")
    print("   - Use Model Serving for deployment")
    print("   - Enable auto-scaling")
    print("   - Implement fallback strategies")
    print()
    
    print("=" * 80)
    print("Demo completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    main()
