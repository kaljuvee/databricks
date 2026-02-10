"""
Databricks Mosaic AI - Utility Functions

Common utility functions for the demo project.
"""

import os
from typing import Dict, List, Optional
import json
from datetime import datetime


def load_config(config_path: str = ".env") -> Dict:
    """
    Load configuration from environment file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Dictionary with configuration values
    """
    config = {}
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    
    return config


def calculate_cost(
    prompt_tokens: int,
    completion_tokens: int,
    model: str = "llama-3-1-8b"
) -> Dict:
    """
    Calculate estimated cost for a model query.
    
    Args:
        prompt_tokens: Number of input tokens
        completion_tokens: Number of output tokens
        model: Model name
        
    Returns:
        Dictionary with cost breakdown
    """
    # Pricing per 1M tokens (as of documentation)
    pricing = {
        "llama-3-1-8b": {"input": 0.15, "output": 0.45},
        "llama-3-3-70b": {"input": 0.50, "output": 1.50},
        "llama-3-1-405b": {"input": 2.00, "output": 6.00},
        "mixtral-8x7b": {"input": 0.50, "output": 1.50},
        "dbrx": {"input": 0.75, "output": 2.25}
    }
    
    # Default to 8B pricing if model not found
    model_pricing = pricing.get(model, pricing["llama-3-1-8b"])
    
    input_cost = (prompt_tokens / 1_000_000) * model_pricing["input"]
    output_cost = (completion_tokens / 1_000_000) * model_pricing["output"]
    total_cost = input_cost + output_cost
    
    return {
        "model": model,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": prompt_tokens + completion_tokens,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost,
        "currency": "USD"
    }


def format_response(
    response: Dict,
    include_metadata: bool = True
) -> str:
    """
    Format a model response for display.
    
    Args:
        response: Response dictionary from model
        include_metadata: Whether to include metadata
        
    Returns:
        Formatted string
    """
    output = []
    
    if response.get("success"):
        output.append(f"Response: {response.get('response', '')}")
        
        if include_metadata:
            output.append("\nMetadata:")
            output.append(f"  Model: {response.get('model', 'N/A')}")
            
            if "usage" in response:
                usage = response["usage"]
                output.append(f"  Tokens: {usage.get('total_tokens', 0)}")
                
                # Calculate cost if possible
                if "prompt_tokens" in usage and "completion_tokens" in usage:
                    cost = calculate_cost(
                        usage["prompt_tokens"],
                        usage["completion_tokens"]
                    )
                    output.append(f"  Est. Cost: ${cost['total_cost']:.6f}")
    else:
        output.append(f"Error: {response.get('error', 'Unknown error')}")
    
    return "\n".join(output)


def save_results(
    results: List[Dict],
    output_path: str,
    format: str = "json"
) -> bool:
    """
    Save results to file.
    
    Args:
        results: List of result dictionaries
        output_path: Path to output file
        format: Output format (json, txt)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        if format == "json":
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=2, default=str)
        
        elif format == "txt":
            with open(output_path, 'w') as f:
                for i, result in enumerate(results):
                    f.write(f"Result {i+1}:\n")
                    f.write(format_response(result))
                    f.write("\n" + "="*80 + "\n\n")
        
        return True
    
    except Exception as e:
        print(f"Error saving results: {e}")
        return False


def validate_environment() -> Dict:
    """
    Validate that required environment variables are set.
    
    Returns:
        Dictionary with validation results
    """
    required_vars = [
        "DATABRICKS_TOKEN",
        "DATABRICKS_HOST"
    ]
    
    optional_vars = [
        "DATABRICKS_CATALOG",
        "DATABRICKS_SCHEMA",
        "DATABRICKS_GATEWAY_ROUTE"
    ]
    
    results = {
        "valid": True,
        "missing_required": [],
        "missing_optional": [],
        "present": []
    }
    
    for var in required_vars:
        if not os.getenv(var):
            results["valid"] = False
            results["missing_required"].append(var)
        else:
            results["present"].append(var)
    
    for var in optional_vars:
        if not os.getenv(var):
            results["missing_optional"].append(var)
        else:
            results["present"].append(var)
    
    return results


def print_banner(title: str, width: int = 80) -> None:
    """
    Print a formatted banner.
    
    Args:
        title: Banner title
        width: Banner width
    """
    print("=" * width)
    print(title.center(width))
    print("=" * width)


def print_section(title: str, width: int = 80) -> None:
    """
    Print a formatted section header.
    
    Args:
        title: Section title
        width: Section width
    """
    print("\n" + "-" * width)
    print(title)
    print("-" * width)


def get_timestamp() -> str:
    """
    Get current timestamp in ISO format.
    
    Returns:
        ISO formatted timestamp string
    """
    return datetime.now().isoformat()


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def parse_model_name(endpoint_name: str) -> str:
    """
    Parse model name from endpoint name.
    
    Args:
        endpoint_name: Full endpoint name
        
    Returns:
        Simplified model name
    """
    # Remove common prefixes
    name = endpoint_name.replace("databricks-", "")
    name = name.replace("-instruct", "")
    
    return name


if __name__ == "__main__":
    """
    Test utility functions.
    """
    print_banner("Databricks Mosaic AI - Utilities Test")
    
    # Test environment validation
    print_section("Environment Validation")
    validation = validate_environment()
    print(f"Valid: {validation['valid']}")
    print(f"Present: {validation['present']}")
    print(f"Missing Required: {validation['missing_required']}")
    print(f"Missing Optional: {validation['missing_optional']}")
    
    # Test cost calculation
    print_section("Cost Calculation")
    cost = calculate_cost(1000, 500, "llama-3-1-8b")
    print(f"Model: {cost['model']}")
    print(f"Total Tokens: {cost['total_tokens']}")
    print(f"Total Cost: ${cost['total_cost']:.6f}")
    
    # Test text truncation
    print_section("Text Truncation")
    long_text = "This is a very long text that needs to be truncated for display purposes."
    truncated = truncate_text(long_text, max_length=30)
    print(f"Original: {long_text}")
    print(f"Truncated: {truncated}")
    
    print("\n" + "=" * 80)
    print("All utility tests completed!")
