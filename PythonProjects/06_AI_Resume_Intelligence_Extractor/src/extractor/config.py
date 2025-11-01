"""
config.py

Centralized runtime configuration for ResumeExtractor.
Defines debug flags, field selection, input/output paths, and run metadata.

Author: Sanjeet Prasad
Email: sanjeet8.23@gmail.com
Created: 2025-10-26
"""

import os
from typing import List, Optional
from datetime import datetime

# -------------------------
# 🧠 Field Extraction Flags
# -------------------------

DEFAULT_FIELDS: List[str] = [
    "name",
    "email",
    "phone",
    "location",
    "skills",
    "experience",
    "jobtitle",
    "company",
    "techstack",
    "score",
]

DEBUG_MODE: bool = True
DEBUG_FIELDS: List[str] = []

# -------------------------
# 📂 Input/Output Paths
# -------------------------

OUTPUT_DIR: str = os.path.join("data", "output")
INPUT_DIR: str = os.path.join("data", "resumes")
CUSTOM_OUTPUT_FILENAME: Optional[str] = None

# -------------------------
# ⚙️ Runtime Metadata
# -------------------------

RUNNER_EMAIL: Optional[str] = "sanjeet8.23@gmail.com"
RUN_DATE: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
NUM_THREADS: int = 1
USE_COLOR_OUTPUT: bool = True

