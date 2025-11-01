"""
Resume Intelligence Engine - ResumeParser
-----------------------------------------
Author: Sanjeet Prasad
Email: sanjeet8.23@gmail.com
Date: October 25, 2025

Main controller class for orchestrating resume field extraction.

This class loads the resume text, initializes NLP, and coordinates field-specific extractors.
Supports threading for parallel extraction and dynamic field selection via CLI or config.
"""

import spacy
from concurrent.futures import ThreadPoolExecutor
from extractor.utils.pdf_loader import load_pdf_text
from extractor.utils.result_types import FieldResult
from extractor.utils.logger import LoggerFactory  # ✅ Updated logger import
from extractor.field_selector import get_selected_fields
from extractor.fields import (
    ResumeNameField, ResumeEmailField, ResumePhoneField, ResumeLocationField,
    ResumeSkillsField, ResumeJobTitleField, ResumeCompanyField,
    ResumeExperienceField, ResumeTechStackField, ResumeScoreField
)

class ResumeParser:
    def __init__(self, file_path, debug=False, selected_fields=None):
        """
        Initialize parser with resume file path and optional debug mode.
        Loads resume text and spaCy NLP model.
        """
        self.file_path = file_path
        self.text = load_pdf_text(file_path)
        self.debug = debug
        self.logger = LoggerFactory(debug=debug).get_logger(__name__) 
        self.nlp = spacy.load("en_core_web_sm")
        # self.nlp = spacy.load("en_core_web_lg")
        self.doc = self.nlp(self.text)
        self.selected_fields = get_selected_fields(selected_fields)

        self.logger.debug(f"Loaded resume: {file_path}")
        self.logger.debug(f"Selected fields: {list(self.selected_fields.keys())}")

    def extract_all(self):
        """
        Extract all selected fields using parallel threads.
        Returns a dictionary of field_name → extracted value.
        """
        results = {}

        def extract_field(name, cls):
            self.logger.debug(f"Extracting field: {name}")
            try:
                if name == "score":
                    extractor = cls(self.text, self.debug) 
                else:
                    extractor = cls(self.text, self.doc, self.debug)  
                result = extractor.extract()
                self.logger.debug(f"Result for {name}: {result}")
                return name, result
            except Exception as e:
                self.logger.error(f"❌ Error extracting '{name}': {e}")
                return name, None

        with ThreadPoolExecutor() as executor:
            futures = {
                name: executor.submit(extract_field, name, cls)
                for name, cls in self.selected_fields.items()
            }
            for name, future in futures.items():
                try:
                    results[name] = future.result()[1]
                except Exception as e:
                    self.logger.error(f"❌ Thread error for '{name}': {e}")
                    results[name] = None

        return results or {}
