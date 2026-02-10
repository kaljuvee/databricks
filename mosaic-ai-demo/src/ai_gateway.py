"""
Databricks Mosaic AI - AI Gateway Demo

This module demonstrates how to use Databricks AI Gateway for
governance, rate limiting, PII masking, and content filtering.
"""

import os
import re
from typing import Dict, List, Optional
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

# Load environment variables
load_dotenv()


class AIGateway:
    """
    AI Gateway implementation with governance features.
    Provides rate limiting, PII detection/masking, and content filtering.
    """
    
    def __init__(self):
        """Initialize the AI Gateway."""
        self.databricks_token = os.getenv("DATABRICKS_TOKEN")
        self.databricks_host = os.getenv("DATABRICKS_HOST")
        self.gateway_route = os.getenv("DATABRICKS_GATEWAY_ROUTE", "default")
        
        if not self.databricks_token or not self.databricks_host:
            raise ValueError(
                "DATABRICKS_TOKEN and DATABRICKS_HOST must be set in environment variables"
            )
        
        # Initialize OpenAI client with Gateway route
        self.client = OpenAI(
            api_key=self.databricks_token,
            base_url=f"{self.databricks_host}/serving-endpoints"
        )
        
        # Usage tracking
        self.usage_log = []
        
        # PII patterns for detection
        self.pii_patterns = {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
            "credit_card": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
            "ip_address": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
        }
        
        # Toxic content keywords (simplified example)
        self.toxic_keywords = [
            "offensive_word_1",
            "offensive_word_2",
            # Add actual toxic keywords as needed
        ]
    
    def detect_pii(self, text: str) -> Dict:
        """
        Detect PII (Personally Identifiable Information) in text.
        
        Args:
            text: Text to scan for PII
            
        Returns:
            Dictionary with detected PII types and locations
        """
        detected_pii = {}
        
        for pii_type, pattern in self.pii_patterns.items():
            matches = re.finditer(pattern, text)
            findings = [match.group() for match in matches]
            
            if findings:
                detected_pii[pii_type] = findings
        
        return {
            "has_pii": len(detected_pii) > 0,
            "pii_types": list(detected_pii.keys()),
            "details": detected_pii
        }
    
    def mask_pii(self, text: str) -> Dict:
        """
        Mask PII in text with placeholders.
        
        Args:
            text: Text containing PII
            
        Returns:
            Dictionary with masked text and mask mapping
        """
        masked_text = text
        mask_mapping = {}
        
        for pii_type, pattern in self.pii_patterns.items():
            matches = list(re.finditer(pattern, masked_text))
            
            for i, match in enumerate(matches):
                original = match.group()
                placeholder = f"[{pii_type.upper()}_{i+1}]"
                masked_text = masked_text.replace(original, placeholder, 1)
                mask_mapping[placeholder] = original
        
        return {
            "original_text": text,
            "masked_text": masked_text,
            "mask_mapping": mask_mapping,
            "pii_count": len(mask_mapping)
        }
    
    def check_toxicity(self, text: str) -> Dict:
        """
        Check text for toxic content.
        
        Args:
            text: Text to check
            
        Returns:
            Dictionary with toxicity assessment
        """
        text_lower = text.lower()
        found_toxic = []
        
        for keyword in self.toxic_keywords:
            if keyword.lower() in text_lower:
                found_toxic.append(keyword)
        
        return {
            "is_toxic": len(found_toxic) > 0,
            "toxic_keywords_found": found_toxic,
            "severity": "high" if len(found_toxic) > 2 else "medium" if len(found_toxic) > 0 else "low"
        }
    
    def apply_rate_limit(
        self,
        user_id: str,
        requests_per_minute: int = 10
    ) -> Dict:
        """
        Apply rate limiting for a user.
        
        Args:
            user_id: User identifier
            requests_per_minute: Maximum requests allowed per minute
            
        Returns:
            Dictionary with rate limit status
        """
        # In a real implementation, this would check against a database or cache
        # For demo purposes, we'll return a mock response
        
        current_time = datetime.now()
        
        # Count recent requests for this user
        recent_requests = [
            log for log in self.usage_log
            if log.get("user_id") == user_id
            and (current_time - log.get("timestamp")).seconds < 60
        ]
        
        is_allowed = len(recent_requests) < requests_per_minute
        
        return {
            "allowed": is_allowed,
            "user_id": user_id,
            "requests_in_last_minute": len(recent_requests),
            "limit": requests_per_minute,
            "remaining": max(0, requests_per_minute - len(recent_requests))
        }
    
    def query_with_governance(
        self,
        prompt: str,
        user_id: str,
        model: str = "databricks-llama-3-1-8b-instruct",
        apply_pii_masking: bool = True,
        check_toxicity_filter: bool = True,
        rate_limit: int = 10
    ) -> Dict:
        """
        Query LLM with full governance features applied.
        
        Args:
            prompt: User prompt
            user_id: User identifier
            model: Model endpoint name
            apply_pii_masking: Whether to mask PII
            check_toxicity_filter: Whether to check for toxic content
            rate_limit: Requests per minute limit
            
        Returns:
            Dictionary with response and governance metadata
        """
        governance_log = {
            "timestamp": datetime.now(),
            "user_id": user_id,
            "model": model
        }
        
        # Step 1: Rate limiting
        rate_check = self.apply_rate_limit(user_id, rate_limit)
        governance_log["rate_limit"] = rate_check
        
        if not rate_check["allowed"]:
            return {
                "success": False,
                "error": "Rate limit exceeded",
                "governance": governance_log
            }
        
        # Step 2: PII detection and masking
        if apply_pii_masking:
            pii_check = self.detect_pii(prompt)
            governance_log["pii_detection"] = pii_check
            
            if pii_check["has_pii"]:
                mask_result = self.mask_pii(prompt)
                prompt = mask_result["masked_text"]
                governance_log["pii_masking"] = {
                    "applied": True,
                    "pii_count": mask_result["pii_count"]
                }
        
        # Step 3: Toxicity check
        if check_toxicity_filter:
            toxicity_check = self.check_toxicity(prompt)
            governance_log["toxicity_check"] = toxicity_check
            
            if toxicity_check["is_toxic"]:
                return {
                    "success": False,
                    "error": "Content filtered due to toxicity",
                    "governance": governance_log
                }
        
        # Step 4: Query the model
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )
            
            answer = response.choices[0].message.content
            
            # Step 5: Check response for toxicity
            if check_toxicity_filter:
                response_toxicity = self.check_toxicity(answer)
                governance_log["response_toxicity_check"] = response_toxicity
                
                if response_toxicity["is_toxic"]:
                    return {
                        "success": False,
                        "error": "Response filtered due to toxicity",
                        "governance": governance_log
                    }
            
            # Log usage
            governance_log["usage"] = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
            
            self.usage_log.append(governance_log)
            
            return {
                "success": True,
                "response": answer,
                "model": model,
                "governance": governance_log
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "governance": governance_log
            }
    
    def get_usage_report(self, user_id: Optional[str] = None) -> Dict:
        """
        Get usage report for all users or specific user.
        
        Args:
            user_id: Optional user identifier to filter by
            
        Returns:
            Dictionary with usage statistics
        """
        logs = self.usage_log
        
        if user_id:
            logs = [log for log in logs if log.get("user_id") == user_id]
        
        total_requests = len(logs)
        total_tokens = sum(
            log.get("usage", {}).get("total_tokens", 0)
            for log in logs
        )
        
        pii_detections = sum(
            1 for log in logs
            if log.get("pii_detection", {}).get("has_pii", False)
        )
        
        toxicity_blocks = sum(
            1 for log in logs
            if log.get("toxicity_check", {}).get("is_toxic", False)
        )
        
        return {
            "user_id": user_id or "all",
            "total_requests": total_requests,
            "total_tokens": total_tokens,
            "pii_detections": pii_detections,
            "toxicity_blocks": toxicity_blocks,
            "average_tokens_per_request": total_tokens / total_requests if total_requests > 0 else 0
        }


def main():
    """
    Main function demonstrating AI Gateway capabilities.
    """
    print("=" * 80)
    print("Databricks Mosaic AI - AI Gateway Demo")
    print("=" * 80)
    print()
    
    # Initialize gateway
    try:
        gateway = AIGateway()
        print("✓ Successfully initialized AI Gateway")
        print()
    except Exception as e:
        print(f"✗ Failed to initialize gateway: {e}")
        return
    
    # Example 1: PII Detection
    print("-" * 80)
    print("Example 1: PII Detection")
    print("-" * 80)
    
    text_with_pii = "My email is john.doe@example.com and my phone is 555-123-4567."
    pii_result = gateway.detect_pii(text_with_pii)
    
    print(f"Text: {text_with_pii}")
    print(f"Has PII: {pii_result['has_pii']}")
    print(f"PII Types: {pii_result['pii_types']}")
    print(f"Details: {pii_result['details']}")
    print()
    
    # Example 2: PII Masking
    print("-" * 80)
    print("Example 2: PII Masking")
    print("-" * 80)
    
    mask_result = gateway.mask_pii(text_with_pii)
    print(f"Original: {mask_result['original_text']}")
    print(f"Masked: {mask_result['masked_text']}")
    print(f"PII Count: {mask_result['pii_count']}")
    print()
    
    # Example 3: Rate Limiting
    print("-" * 80)
    print("Example 3: Rate Limiting")
    print("-" * 80)
    
    user_id = "user_123"
    rate_result = gateway.apply_rate_limit(user_id, requests_per_minute=10)
    
    print(f"User: {rate_result['user_id']}")
    print(f"Allowed: {rate_result['allowed']}")
    print(f"Requests in last minute: {rate_result['requests_in_last_minute']}")
    print(f"Remaining: {rate_result['remaining']}/{rate_result['limit']}")
    print()
    
    # Example 4: Query with Governance
    print("-" * 80)
    print("Example 4: Query with Full Governance")
    print("-" * 80)
    
    prompt = "What are the benefits of using Databricks for data engineering?"
    result = gateway.query_with_governance(
        prompt=prompt,
        user_id=user_id,
        apply_pii_masking=True,
        check_toxicity_filter=True
    )
    
    if result["success"]:
        print(f"Response: {result['response'][:200]}...")
        print(f"\nGovernance Summary:")
        print(f"  - Rate limit check: Passed")
        print(f"  - PII detection: {result['governance']['pii_detection']['has_pii']}")
        print(f"  - Toxicity check: Passed")
        print(f"  - Tokens used: {result['governance']['usage']['total_tokens']}")
    else:
        print(f"Error: {result['error']}")
    
    print()
    
    # Example 5: Usage Report
    print("-" * 80)
    print("Example 5: Usage Report")
    print("-" * 80)
    
    # Make a few more requests for demo
    for i in range(3):
        gateway.query_with_governance(
            prompt=f"Test query {i}",
            user_id=user_id
        )
    
    report = gateway.get_usage_report(user_id=user_id)
    
    print(f"User: {report['user_id']}")
    print(f"Total Requests: {report['total_requests']}")
    print(f"Total Tokens: {report['total_tokens']}")
    print(f"PII Detections: {report['pii_detections']}")
    print(f"Toxicity Blocks: {report['toxicity_blocks']}")
    print(f"Avg Tokens/Request: {report['average_tokens_per_request']:.2f}")
    print()
    
    # Best practices
    print("-" * 80)
    print("AI Gateway Best Practices")
    print("-" * 80)
    print()
    print("1. **Rate Limiting**")
    print("   - Set appropriate limits based on user tiers")
    print("   - Implement exponential backoff for retries")
    print("   - Monitor and alert on rate limit violations")
    print()
    print("2. **PII Protection**")
    print("   - Always mask PII in logs and traces")
    print("   - Use tokenization for reversible masking")
    print("   - Comply with GDPR, CCPA, and other regulations")
    print()
    print("3. **Content Filtering**")
    print("   - Filter both input prompts and output responses")
    print("   - Use multiple toxicity detection methods")
    print("   - Provide clear feedback to users on filtered content")
    print()
    print("4. **Usage Tracking**")
    print("   - Track tokens per user/team/organization")
    print("   - Set up cost alerts and budgets")
    print("   - Generate regular usage reports")
    print()
    print("5. **Model Routing**")
    print("   - Route simple queries to smaller, cheaper models")
    print("   - Use complex models only when necessary")
    print("   - Implement fallback strategies")
    print()
    
    print("=" * 80)
    print("Demo completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    main()
