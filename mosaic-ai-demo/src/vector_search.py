"""
Databricks Mosaic AI - Vector Search Demo

This module demonstrates how to use Databricks Vector Search for
similarity search and retrieval operations.
"""

import os
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()


class DatabricksVectorSearch:
    """
    Client for interacting with Databricks Vector Search.
    Provides methods for creating indexes, adding documents, and searching.
    """
    
    def __init__(self):
        """Initialize the Databricks Vector Search client."""
        self.databricks_token = os.getenv("DATABRICKS_TOKEN")
        self.databricks_host = os.getenv("DATABRICKS_HOST")
        self.catalog = os.getenv("DATABRICKS_CATALOG", "main")
        self.schema = os.getenv("DATABRICKS_SCHEMA", "default")
        
        if not self.databricks_token or not self.databricks_host:
            raise ValueError(
                "DATABRICKS_TOKEN and DATABRICKS_HOST must be set in environment variables"
            )
        
        self.headers = {
            "Authorization": f"Bearer {self.databricks_token}",
            "Content-Type": "application/json"
        }
        
        # Clean up host URL
        self.base_url = self.databricks_host.rstrip('/')
    
    def create_vector_search_endpoint(
        self,
        endpoint_name: str,
        endpoint_type: str = "STANDARD"
    ) -> Dict:
        """
        Create a Vector Search endpoint.
        
        Args:
            endpoint_name: Name for the endpoint
            endpoint_type: Type of endpoint (STANDARD or PROVISIONED)
            
        Returns:
            Response dictionary with endpoint details
        """
        url = f"{self.base_url}/api/2.0/vector-search/endpoints"
        
        payload = {
            "name": endpoint_name,
            "endpoint_type": endpoint_type
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return {
                "success": True,
                "endpoint": response.json()
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "details": response.text if response else None
            }
    
    def list_vector_search_endpoints(self) -> Dict:
        """
        List all Vector Search endpoints.
        
        Returns:
            Response dictionary with list of endpoints
        """
        url = f"{self.base_url}/api/2.0/vector-search/endpoints"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return {
                "success": True,
                "endpoints": response.json()
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "details": response.text if response else None
            }
    
    def create_vector_index(
        self,
        endpoint_name: str,
        index_name: str,
        source_table: str,
        primary_key: str,
        embedding_source_column: str,
        embedding_model_endpoint: Optional[str] = None
    ) -> Dict:
        """
        Create a Vector Search index.
        
        Args:
            endpoint_name: Name of the Vector Search endpoint
            index_name: Name for the index (format: catalog.schema.index)
            source_table: Delta table to sync from (format: catalog.schema.table)
            primary_key: Primary key column name
            embedding_source_column: Column containing text to embed
            embedding_model_endpoint: Optional embedding model endpoint
            
        Returns:
            Response dictionary with index details
        """
        url = f"{self.base_url}/api/2.0/vector-search/indexes"
        
        payload = {
            "name": index_name,
            "endpoint_name": endpoint_name,
            "primary_key": primary_key,
            "index_type": "DELTA_SYNC",
            "delta_sync_index_spec": {
                "source_table": source_table,
                "embedding_source_columns": [
                    {
                        "name": embedding_source_column,
                        "embedding_model_endpoint_name": embedding_model_endpoint
                    }
                ] if embedding_model_endpoint else None
            }
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return {
                "success": True,
                "index": response.json()
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "details": response.text if response else None
            }
    
    def query_vector_index(
        self,
        index_name: str,
        query_text: str,
        num_results: int = 5,
        filters: Optional[Dict] = None
    ) -> Dict:
        """
        Query a Vector Search index for similar documents.
        
        Args:
            index_name: Name of the index to query
            query_text: Text query to find similar documents
            num_results: Number of results to return
            filters: Optional filters to apply
            
        Returns:
            Response dictionary with search results
        """
        url = f"{self.base_url}/api/2.0/vector-search/indexes/{index_name}/query"
        
        payload = {
            "query_text": query_text,
            "num_results": num_results
        }
        
        if filters:
            payload["filters"] = filters
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return {
                "success": True,
                "results": response.json()
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "details": response.text if response else None
            }
    
    def get_index_status(self, index_name: str) -> Dict:
        """
        Get the status of a Vector Search index.
        
        Args:
            index_name: Name of the index
            
        Returns:
            Response dictionary with index status
        """
        url = f"{self.base_url}/api/2.0/vector-search/indexes/{index_name}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return {
                "success": True,
                "status": response.json()
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "details": response.text if response else None
            }
    
    def delete_index(self, index_name: str) -> Dict:
        """
        Delete a Vector Search index.
        
        Args:
            index_name: Name of the index to delete
            
        Returns:
            Response dictionary with deletion status
        """
        url = f"{self.base_url}/api/2.0/vector-search/indexes/{index_name}"
        
        try:
            response = requests.delete(url, headers=self.headers)
            response.raise_for_status()
            return {
                "success": True,
                "message": "Index deleted successfully"
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "details": response.text if response else None
            }


def main():
    """
    Main function demonstrating Vector Search capabilities.
    """
    print("=" * 80)
    print("Databricks Mosaic AI - Vector Search Demo")
    print("=" * 80)
    print()
    
    # Initialize client
    try:
        client = DatabricksVectorSearch()
        print("✓ Successfully connected to Databricks Vector Search API")
        print()
    except Exception as e:
        print(f"✗ Failed to initialize client: {e}")
        return
    
    # Example 1: List existing endpoints
    print("-" * 80)
    print("Example 1: List Vector Search Endpoints")
    print("-" * 80)
    
    result = client.list_vector_search_endpoints()
    
    if result["success"]:
        endpoints = result.get("endpoints", {}).get("endpoints", [])
        if endpoints:
            print(f"Found {len(endpoints)} endpoint(s):")
            for ep in endpoints:
                print(f"  - {ep.get('name')} (Status: {ep.get('endpoint_status', {}).get('state')})")
        else:
            print("No endpoints found. You may need to create one first.")
        print()
    else:
        print(f"Error: {result['error']}")
        if result.get('details'):
            print(f"Details: {result['details']}")
        print()
    
    # Example 2: Create a Vector Search endpoint (commented out to avoid accidental creation)
    print("-" * 80)
    print("Example 2: Create Vector Search Endpoint (Example)")
    print("-" * 80)
    print("To create an endpoint, uncomment the following code:")
    print()
    print("  endpoint_name = 'my_vector_search_endpoint'")
    print("  result = client.create_vector_search_endpoint(endpoint_name)")
    print()
    
    # Example 3: Vector Index operations
    print("-" * 80)
    print("Example 3: Vector Index Operations (Example)")
    print("-" * 80)
    print("To create a vector index, you need:")
    print("  1. A Delta table with your documents")
    print("  2. A Vector Search endpoint")
    print("  3. An embedding model endpoint (optional)")
    print()
    print("Example code:")
    print()
    print("  result = client.create_vector_index(")
    print("      endpoint_name='my_endpoint',")
    print("      index_name='main.default.my_docs_index',")
    print("      source_table='main.default.my_docs',")
    print("      primary_key='id',")
    print("      embedding_source_column='text',")
    print("      embedding_model_endpoint='databricks-bge-large-en'")
    print("  )")
    print()
    
    # Example 4: Query a vector index
    print("-" * 80)
    print("Example 4: Query Vector Index (Example)")
    print("-" * 80)
    print("To query an existing index:")
    print()
    print("  result = client.query_vector_index(")
    print("      index_name='main.default.my_docs_index',")
    print("      query_text='What is machine learning?',")
    print("      num_results=5")
    print("  )")
    print()
    print("  if result['success']:")
    print("      for doc in result['results']['data_array']:")
    print("          print(f\"Score: {doc['score']}, Text: {doc['text']}\")")
    print()
    
    # Best practices
    print("-" * 80)
    print("Best Practices for Vector Search")
    print("-" * 80)
    print()
    print("1. **Delta Sync**: Vector Search automatically syncs with Delta tables")
    print("   - Changes to source table automatically update the index")
    print("   - No manual refresh needed")
    print()
    print("2. **Embedding Models**: Choose the right embedding model")
    print("   - BGE-large-en: Good for English text")
    print("   - E5-large: Multilingual support")
    print("   - Custom models: Use your own fine-tuned embeddings")
    print()
    print("3. **Index Types**:")
    print("   - DELTA_SYNC: Automatic sync with Delta tables")
    print("   - DIRECT_ACCESS: Manual embedding management")
    print()
    print("4. **Performance**:")
    print("   - Use filters to narrow search scope")
    print("   - Adjust num_results based on your needs")
    print("   - Monitor index sync status")
    print()
    
    print("=" * 80)
    print("Demo completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    main()
