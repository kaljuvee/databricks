"""
Databricks Mosaic AI - Model Serving Demo

This module demonstrates how to use Databricks Foundation Model APIs
with OpenAI-compatible interface for various LLM models.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict, Optional

# Load environment variables
load_dotenv()


class DatabricksModelServing:
    """
    Client for interacting with Databricks Foundation Model APIs.
    Supports Llama, Mixtral, DBRX, and external models via AI Gateway.
    """
    
    def __init__(self):
        """Initialize the Databricks Model Serving client."""
        self.databricks_token = os.getenv("DATABRICKS_TOKEN")
        self.databricks_host = os.getenv("DATABRICKS_HOST")
        
        if not self.databricks_token or not self.databricks_host:
            raise ValueError(
                "DATABRICKS_TOKEN and DATABRICKS_HOST must be set in environment variables"
            )
        
        # Initialize OpenAI client with Databricks endpoint
        self.client = OpenAI(
            api_key=self.databricks_token,
            base_url=f"{self.databricks_host}/serving-endpoints"
        )
    
    def query_model(
        self,
        prompt: str,
        model: str = "databricks-llama-3-1-8b-instruct",
        max_tokens: int = 500,
        temperature: float = 0.7,
        system_message: Optional[str] = None
    ) -> Dict:
        """
        Query a Databricks Foundation Model.
        
        Args:
            prompt: The user prompt/question
            model: Model endpoint name (e.g., 'databricks-llama-3-1-8b-instruct')
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0.0 to 1.0)
            system_message: Optional system message for context
            
        Returns:
            Dictionary with response and metadata
        """
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return {
                "success": True,
                "model": model,
                "response": response.choices[0].message.content,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                "finish_reason": response.choices[0].finish_reason
            }
        
        except Exception as e:
            return {
                "success": False,
                "model": model,
                "error": str(e)
            }
    
    def compare_models(
        self,
        prompt: str,
        models: List[str],
        system_message: Optional[str] = None
    ) -> List[Dict]:
        """
        Compare responses from multiple models for the same prompt.
        
        Args:
            prompt: The user prompt/question
            models: List of model endpoint names
            system_message: Optional system message for context
            
        Returns:
            List of response dictionaries from each model
        """
        results = []
        
        for model in models:
            print(f"Querying {model}...")
            result = self.query_model(
                prompt=prompt,
                model=model,
                system_message=system_message
            )
            results.append(result)
        
        return results
    
    def streaming_query(
        self,
        prompt: str,
        model: str = "databricks-llama-3-1-8b-instruct",
        system_message: Optional[str] = None
    ):
        """
        Query a model with streaming response.
        
        Args:
            prompt: The user prompt/question
            model: Model endpoint name
            system_message: Optional system message for context
            
        Yields:
            Response chunks as they arrive
        """
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            stream = self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        
        except Exception as e:
            yield f"Error: {str(e)}"


def main():
    """
    Main function demonstrating Model Serving capabilities.
    """
    print("=" * 80)
    print("Databricks Mosaic AI - Model Serving Demo")
    print("=" * 80)
    print()
    
    # Initialize client
    try:
        client = DatabricksModelServing()
        print("✓ Successfully connected to Databricks Model Serving")
        print()
    except Exception as e:
        print(f"✗ Failed to initialize client: {e}")
        return
    
    # Example 1: Simple query
    print("-" * 80)
    print("Example 1: Simple Query with Llama 3.1 8B")
    print("-" * 80)
    
    prompt = "Explain what Retrieval-Augmented Generation (RAG) is in 2-3 sentences."
    result = client.query_model(prompt=prompt)
    
    if result["success"]:
        print(f"Model: {result['model']}")
        print(f"Response: {result['response']}")
        print(f"Tokens used: {result['usage']['total_tokens']}")
        print()
    else:
        print(f"Error: {result['error']}")
        print()
    
    # Example 2: Query with system message
    print("-" * 80)
    print("Example 2: Query with System Message")
    print("-" * 80)
    
    system_msg = "You are a helpful data engineering assistant specializing in Databricks."
    prompt = "What are the benefits of using Delta Lake?"
    
    result = client.query_model(
        prompt=prompt,
        system_message=system_msg,
        temperature=0.5
    )
    
    if result["success"]:
        print(f"Response: {result['response']}")
        print()
    else:
        print(f"Error: {result['error']}")
        print()
    
    # Example 3: Compare multiple models (if available)
    print("-" * 80)
    print("Example 3: Model Comparison")
    print("-" * 80)
    
    models_to_compare = [
        "databricks-llama-3-1-8b-instruct",
        # Uncomment if you have access to these models:
        # "databricks-llama-3-3-70b-instruct",
        # "databricks-mixtral-8x7b-instruct",
    ]
    
    prompt = "What is the capital of France?"
    results = client.compare_models(prompt=prompt, models=models_to_compare)
    
    for result in results:
        if result["success"]:
            print(f"\nModel: {result['model']}")
            print(f"Response: {result['response']}")
            print(f"Tokens: {result['usage']['total_tokens']}")
        else:
            print(f"\nModel: {result['model']}")
            print(f"Error: {result['error']}")
    
    print()
    
    # Example 4: Streaming response
    print("-" * 80)
    print("Example 4: Streaming Response")
    print("-" * 80)
    
    prompt = "Write a haiku about data lakes."
    print("Streaming response: ", end="", flush=True)
    
    for chunk in client.streaming_query(prompt=prompt):
        print(chunk, end="", flush=True)
    
    print("\n")
    
    # Cost estimation
    print("-" * 80)
    print("Cost Estimation Example")
    print("-" * 80)
    print("Based on Llama 3.1 8B pricing:")
    print("  Input:  $0.15 per 1M tokens")
    print("  Output: $0.45 per 1M tokens")
    print()
    
    if result["success"]:
        usage = result["usage"]
        input_cost = (usage["prompt_tokens"] / 1_000_000) * 0.15
        output_cost = (usage["completion_tokens"] / 1_000_000) * 0.45
        total_cost = input_cost + output_cost
        
        print(f"Last query used {usage['total_tokens']} tokens")
        print(f"Estimated cost: ${total_cost:.6f}")
    
    print()
    print("=" * 80)
    print("Demo completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    main()
