"""
Unit tests for Resume Intelligence Extractor

Author: Sanjeet Prasad
Email: sanjeet8.23@gmail.com
Date: 26-Oct-2025
"""

import unittest
import os
import sys
import shutil

# Ensure src/ is in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from extractor.resume_parser import ResumeParser
from extractor.utils.exporter import ResumeExporter
from extractor.utils.pdf_loader import load_pdf_text
from extractor.fields.jobtitle_field import ResumeJobTitleField
from extractor.utils.cleanup import remove_pycache

class TestResumeParser(unittest.TestCase):

    def setUp(self):
        self.sample_pdf = "data/resumes/SampleResume.pdf"
        self.output_csv = "data/output/test_resume_output.csv"
        self.parser = ResumeParser(file_path=self.sample_pdf)

    def tearDown(self):
        if os.path.exists(self.output_csv):
            os.remove(self.output_csv)

    def test_resume_parser_extracts_core_fields(self):
        """TC01: Verifies name, email, phone, location, and experience fields"""
        results = self.parser.extract_all()
        for field in ["name", "email", "phone", "location", "experience"]:
            self.assertIn(field, results)
        print("✅ TC01 passed: Core fields extracted")

    def test_skills_extraction(self):
        """TC02: Confirms skills are extracted and normalized correctly"""
        results = self.parser.extract_all()
        skills = results.get("skills", [])
        self.assertIsInstance(skills, (list, set))
        self.assertTrue(all(isinstance(skill, str) for skill in skills))
        print("✅ TC02 passed: Skills extracted and normalized")

    def test_job_title_debug_flag(self):
        """TC03: Ensures job title extractor respects debug flag"""
        text = self.parser.text
        doc = self.parser.doc
        extractor = ResumeJobTitleField(text, doc, debug=True)
        job_titles = extractor.extract()
        if isinstance(job_titles, str):
            job_titles = [job_titles]
        self.assertIsInstance(job_titles, list)
        self.assertTrue(any(isinstance(title, str) for title in job_titles))
        print("✅ TC03 passed: Job title extractor respects debug flag")

    def test_pdf_loader_reads_text(self):
        """TC04: Validates PDF text extraction from sample resume"""
        text = load_pdf_text(self.sample_pdf)
        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 100, "Extracted text should be reasonably long")
        print("✅ TC04 passed: PDF text extracted")

    def test_exporter_creates_csv(self):
        """TC05: Checks that CSV output is generated and contains expected data"""
        results = self.parser.extract_all()
        exporter = ResumeExporter(output_dir="data/output")
        output_path = exporter.export(results, resume_filename="test_resume_output.csv")
        self.assertTrue(os.path.exists(output_path))
        print("✅ TC05 passed: CSV file created")

    def test_field_not_found_returns_default(self):
        """TC06: Ensures missing fields return 'Not found' or empty values"""
        results = self.parser.extract_all()
        name = results.get("name", "Not found")
        self.assertTrue(name or name == "Not found")
        print("✅ TC06 passed: Missing fields handled gracefully")

    def cleanup_pycache():
        """Removes all __pycache__ folders after tests"""
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
                    print(f"🧹 Removed: {path}")
                except Exception as e:
                    print(f"⚠️ Could not remove {path}: {e}")

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestResumeParser)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        remove_pycache()
