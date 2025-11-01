"""
Data structure for storing field extraction results.
Includes value, confidence score, and source method.
"""

from dataclasses import dataclass

@dataclass
class FieldResult:
    value: any                   # Extracted value (str, list, set, etc.)
    confidence: float = 1.0      # Confidence score (0.0 to 1.0)
    source: str = "unknown"      # Extraction method or strategy name

