"""
Resume Intelligence Engine - BaseFieldExtractor
-----------------------------------------------
Author: Sanjeet Prasad
Email: sanjeet8.23@gmail.com
Date: October 25, 2025

Base class for all field extractors.
Provides shared access to resume text, spaCy doc, and debug logger.
"""

from extractor.utils.logger import LoggerFactory  # ✅ Updated to use LoggerFactory

class BaseFieldExtractor:
    def __init__(self, text, doc=None, debug=False):
        self.text = text
        self.doc = doc
        self.debug = debug
        self.logger = LoggerFactory(debug=debug).get_logger(self.__class__.__name__)  # ✅ Centralized logger

    def extract(self):
        raise NotImplementedError("Subclasses must implement extract()")
