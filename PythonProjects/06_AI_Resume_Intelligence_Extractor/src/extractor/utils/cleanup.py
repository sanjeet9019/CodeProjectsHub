"""
Cleanup utilities for Resume Intelligence Extractor

Author: Sanjeet Prasad
Email: sanjeet8.23@gmail.com
Date: 26-Oct-2025
"""

import os
import shutil
from extractor.utils.logger import LoggerFactory

def remove_pycache(mode="debug"):
    """
    Deletes all __pycache__ folders across known submodules.

    Parameters:
        mode (str): 'debug' for verbose logging, 'silent' for minimal output.
    """
    logger = LoggerFactory(debug=(mode == "debug")).get_logger("Cleanup")

    targets = [
        "scripts/__pycache__",
        "src/extractor/__pycache__",
        "src/extractor/fields/__pycache__",
        "src/extractor/utils/__pycache__",
        "test/__pycache__"
    ]

    for path in targets:
        if os.path.isdir(path):
            try:
                shutil.rmtree(path)
            except Exception as e:
                logger.warning(f"⚠️ Could not remove {path}: {e}")
