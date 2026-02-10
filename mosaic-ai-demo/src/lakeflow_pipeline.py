"""
Databricks Mosaic AI - Lakeflow Pipeline Demo

This module demonstrates how to use Lakeflow (Delta Live Tables) for
automated document processing, chunking, and embedding pipelines.
"""

import os
from typing import Dict, List, Optional
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()


class LakeflowPipeline:
    """
    Lakeflow pipeline for automated document processing and embedding.
    Uses Delta Live Tables for declarative data transformations.
    """
    
    def __init__(self):
        """Initialize the Lakeflow pipeline."""
        self.databricks_token = os.getenv("DATABRICKS_TOKEN")
        self.databricks_host = os.getenv("DATABRICKS_HOST")
        self.catalog = os.getenv("DATABRICKS_CATALOG", "main")
        self.schema = os.getenv("DATABRICKS_SCHEMA", "default")
        
        if not self.databricks_token or not self.databricks_host:
            raise ValueError(
                "DATABRICKS_TOKEN and DATABRICKS_HOST must be set in environment variables"
            )
    
    def generate_dlt_pipeline_config(
        self,
        pipeline_name: str,
        source_table: str,
        target_table: str,
        embedding_model: str = "databricks-bge-large-en"
    ) -> Dict:
        """
        Generate a Delta Live Tables pipeline configuration for document processing.
        
        Args:
            pipeline_name: Name of the DLT pipeline
            source_table: Source table with raw documents
            target_table: Target table for processed chunks
            embedding_model: Embedding model endpoint name
            
        Returns:
            Pipeline configuration dictionary
        """
        config = {
            "name": pipeline_name,
            "storage": f"/pipelines/{pipeline_name}",
            "configuration": {
                "source_table": f"{self.catalog}.{self.schema}.{source_table}",
                "target_table": f"{self.catalog}.{self.schema}.{target_table}",
                "embedding_model": embedding_model,
                "chunk_size": "500",
                "chunk_overlap": "50"
            },
            "clusters": [
                {
                    "label": "default",
                    "autoscale": {
                        "min_workers": 1,
                        "max_workers": 5,
                        "mode": "ENHANCED"
                    }
                }
            ],
            "libraries": [
                {"pypi": {"package": "openai"}},
                {"pypi": {"package": "tiktoken"}}
            ],
            "target": f"{self.catalog}.{self.schema}",
            "continuous": False,
            "development": True
        }
        
        return config
    
    def generate_dlt_notebook_code(self) -> str:
        """
        Generate DLT notebook code for document processing pipeline.
        
        Returns:
            Python code for DLT notebook
        """
        code = '''
import dlt
from pyspark.sql import functions as F
from pyspark.sql.types import StringType, ArrayType, StructType, StructField, IntegerType
import os

# Configuration
SOURCE_TABLE = spark.conf.get("source_table")
EMBEDDING_MODEL = spark.conf.get("embedding_model", "databricks-bge-large-en")
CHUNK_SIZE = int(spark.conf.get("chunk_size", "500"))
CHUNK_OVERLAP = int(spark.conf.get("chunk_overlap", "50"))


@dlt.table(
    name="raw_documents",
    comment="Raw documents from source",
    table_properties={
        "quality": "bronze"
    }
)
def raw_documents():
    """
    Bronze layer: Ingest raw documents from source table.
    """
    return spark.read.table(SOURCE_TABLE)


def chunk_text(text: str, chunk_size: int, overlap: int) -> list:
    """
    Split text into overlapping chunks.
    """
    if not text:
        return []
    
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append({
            "text": chunk,
            "start_pos": start,
            "end_pos": min(end, text_length),
            "length": len(chunk)
        })
        start += chunk_size - overlap
    
    return chunks


# Register UDF for chunking
chunk_text_udf = F.udf(
    lambda text: chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP),
    ArrayType(StructType([
        StructField("text", StringType()),
        StructField("start_pos", IntegerType()),
        StructField("end_pos", IntegerType()),
        StructField("length", IntegerType())
    ]))
)


@dlt.table(
    name="chunked_documents",
    comment="Documents split into chunks with overlap",
    table_properties={
        "quality": "silver"
    }
)
def chunked_documents():
    """
    Silver layer: Chunk documents into smaller pieces.
    """
    return (
        dlt.read("raw_documents")
        .withColumn("chunks", chunk_text_udf(F.col("text")))
        .withColumn("chunk", F.explode(F.col("chunks")))
        .select(
            F.col("id").alias("document_id"),
            F.col("source"),
            F.col("metadata"),
            F.col("chunk.text").alias("chunk_text"),
            F.col("chunk.start_pos").alias("start_position"),
            F.col("chunk.end_pos").alias("end_position"),
            F.col("chunk.length").alias("chunk_length"),
            F.monotonically_increasing_id().alias("chunk_id")
        )
    )


@dlt.table(
    name="embedded_chunks",
    comment="Chunks with embeddings ready for Vector Search",
    table_properties={
        "quality": "gold",
        "delta.enableChangeDataFeed": "true"
    }
)
def embedded_chunks():
    """
    Gold layer: Prepare chunks for embedding.
    Note: Actual embedding generation happens in Vector Search index creation.
    """
    return (
        dlt.read("chunked_documents")
        .select(
            F.concat(
                F.col("document_id"),
                F.lit("_"),
                F.col("chunk_id")
            ).alias("id"),
            F.col("document_id"),
            F.col("chunk_text").alias("text"),
            F.col("source"),
            F.col("metadata"),
            F.col("start_position"),
            F.col("end_position"),
            F.col("chunk_length"),
            F.current_timestamp().alias("processed_at")
        )
    )


@dlt.table(
    name="pipeline_metrics",
    comment="Pipeline execution metrics"
)
def pipeline_metrics():
    """
    Track pipeline metrics for monitoring.
    """
    return (
        dlt.read("embedded_chunks")
        .groupBy("document_id", "source")
        .agg(
            F.count("*").alias("chunk_count"),
            F.avg("chunk_length").alias("avg_chunk_length"),
            F.sum("chunk_length").alias("total_characters"),
            F.max("processed_at").alias("last_processed")
        )
    )


# Data quality expectations
@dlt.expect_or_drop("valid_chunk_text", "chunk_text IS NOT NULL AND length(chunk_text) > 0")
@dlt.expect_or_drop("valid_chunk_length", "chunk_length > 0 AND chunk_length <= 1000")
@dlt.expect("reasonable_chunk_count", "chunk_count > 0 AND chunk_count < 10000")
'''
        return code
    
    def create_sample_documents_table(self) -> str:
        """
        Generate SQL to create a sample documents table.
        
        Returns:
            SQL code to create the table
        """
        sql = f"""
-- Create sample documents table for Lakeflow pipeline
CREATE TABLE IF NOT EXISTS {self.catalog}.{self.schema}.sample_documents (
  id STRING NOT NULL,
  text STRING NOT NULL,
  source STRING,
  metadata MAP<STRING, STRING>,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
) USING DELTA;

-- Insert sample documents
INSERT INTO {self.catalog}.{self.schema}.sample_documents (id, text, source, metadata) VALUES
  (
    'doc_001',
    'Databricks Mosaic AI provides a unified platform for building RAG applications. It includes Vector Search for retrieval and Foundation Model APIs for generation. The platform automatically syncs vector indexes with Delta tables.',
    'databricks_intro.txt',
    map('category', 'documentation', 'topic', 'mosaic_ai')
  ),
  (
    'doc_002',
    'Lakeflow pipelines use Delta Live Tables to automate document processing. You can define declarative transformations for chunking and embedding documents. The pipeline ensures data quality with expectations and constraints.',
    'lakeflow_guide.txt',
    map('category', 'documentation', 'topic', 'lakeflow')
  ),
  (
    'doc_003',
    'The AI Gateway provides governance features like rate limiting, PII masking, and toxicity filtering. It acts as a central layer for all model interactions in your organization. Usage tracking helps manage costs and compliance.',
    'ai_gateway_overview.txt',
    map('category', 'documentation', 'topic', 'ai_gateway')
  );

-- Verify the data
SELECT id, source, length(text) as text_length, metadata
FROM {self.catalog}.{self.schema}.sample_documents;
"""
        return sql


def main():
    """
    Main function demonstrating Lakeflow pipeline capabilities.
    """
    print("=" * 80)
    print("Databricks Mosaic AI - Lakeflow Pipeline Demo")
    print("=" * 80)
    print()
    
    # Initialize pipeline
    try:
        pipeline = LakeflowPipeline()
        print("✓ Successfully initialized Lakeflow pipeline")
        print()
    except Exception as e:
        print(f"✗ Failed to initialize pipeline: {e}")
        return
    
    # Example 1: Generate DLT pipeline configuration
    print("-" * 80)
    print("Example 1: Delta Live Tables Pipeline Configuration")
    print("-" * 80)
    
    config = pipeline.generate_dlt_pipeline_config(
        pipeline_name="document_processing_pipeline",
        source_table="sample_documents",
        target_table="embedded_chunks"
    )
    
    print("Pipeline Configuration:")
    print(json.dumps(config, indent=2))
    print()
    
    # Example 2: Generate DLT notebook code
    print("-" * 80)
    print("Example 2: Delta Live Tables Notebook Code")
    print("-" * 80)
    
    dlt_code = pipeline.generate_dlt_notebook_code()
    print("Generated DLT notebook code (first 500 characters):")
    print(dlt_code[:500] + "...")
    print()
    print("Full code saved to: lakeflow_dlt_notebook.py")
    
    # Save the full code
    with open("lakeflow_dlt_notebook.py", "w") as f:
        f.write(dlt_code)
    
    # Example 3: Sample documents table SQL
    print("-" * 80)
    print("Example 3: Create Sample Documents Table")
    print("-" * 80)
    
    sql = pipeline.create_sample_documents_table()
    print("SQL to create and populate sample documents table:")
    print(sql)
    print()
    
    # Lakeflow Architecture
    print("-" * 80)
    print("Lakeflow Pipeline Architecture")
    print("-" * 80)
    print()
    print("Medallion Architecture:")
    print()
    print("1. **Bronze Layer (raw_documents)**")
    print("   - Ingest raw documents from source")
    print("   - No transformations, preserve original data")
    print("   - Enable schema evolution")
    print()
    print("2. **Silver Layer (chunked_documents)**")
    print("   - Split documents into chunks")
    print("   - Apply data quality rules")
    print("   - Add metadata and positions")
    print()
    print("3. **Gold Layer (embedded_chunks)**")
    print("   - Prepare for Vector Search")
    print("   - Enable Change Data Feed")
    print("   - Ready for downstream consumption")
    print()
    print("4. **Metrics Layer (pipeline_metrics)**")
    print("   - Track processing statistics")
    print("   - Monitor data quality")
    print("   - Enable observability")
    print()
    
    # Best practices
    print("-" * 80)
    print("Lakeflow Best Practices")
    print("-" * 80)
    print()
    print("1. **Declarative Transformations**")
    print("   - Define what you want, not how to get it")
    print("   - Let Databricks optimize execution")
    print("   - Use @dlt.table decorators")
    print()
    print("2. **Data Quality Expectations**")
    print("   - Use @dlt.expect for quality checks")
    print("   - Drop invalid records with @dlt.expect_or_drop")
    print("   - Track violations with @dlt.expect_or_fail")
    print()
    print("3. **Incremental Processing**")
    print("   - Use dlt.read_stream for streaming")
    print("   - Enable Change Data Feed on gold tables")
    print("   - Process only new/changed data")
    print()
    print("4. **Pipeline Monitoring**")
    print("   - Create metrics tables")
    print("   - Use pipeline event logs")
    print("   - Set up alerts for failures")
    print()
    print("5. **Integration with Vector Search**")
    print("   - Enable CDC on final table")
    print("   - Use consistent ID columns")
    print("   - Auto-sync with vector indexes")
    print()
    
    # Setup instructions
    print("-" * 80)
    print("How to Deploy This Pipeline")
    print("-" * 80)
    print()
    print("1. Create a DLT pipeline in Databricks:")
    print("   - Go to Workflows → Delta Live Tables")
    print("   - Click 'Create Pipeline'")
    print("   - Upload the generated notebook")
    print("   - Configure with the generated config")
    print()
    print("2. Create the source table:")
    print("   - Run the SQL from Example 3 in a notebook")
    print("   - Or use your own documents table")
    print()
    print("3. Start the pipeline:")
    print("   - Click 'Start' in the DLT UI")
    print("   - Monitor execution in the graph view")
    print("   - Check data quality metrics")
    print()
    print("4. Create Vector Search index:")
    print("   - Point to the 'embedded_chunks' table")
    print("   - Enable automatic sync")
    print("   - Specify embedding model")
    print()
    
    print("=" * 80)
    print("Demo completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    main()
