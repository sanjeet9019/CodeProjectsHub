#############################################################################
###  Author       : Sanjeet Prasad                                       ###
###  Email        : sanjeet8.23@gmail.com                                ###
###  Description  : Unit tests for PDFToAudioConverter class             ###
###  Framework    : unittest                                              ###
###  Date         : 24-10-2025                                           ###
#############################################################################

import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.pdfaudio.pdf_to_audio_converter import PDFToAudioConverter

class TestPDFToAudioConverter(unittest.TestCase):
    """Unit tests for PDFToAudioConverter"""

    def setUp(self):
        """Prepare test instance with known input/output paths"""
        self.test_pdf = "data/input.pdf"
        self.test_output = "data/test_output.mp3"
        self.converter = PDFToAudioConverter(pdf_path=self.test_pdf, audio_output=self.test_output)

    def test_pdf_file_exists(self):
        """Verify input PDF file is present"""
        self.assertTrue(os.path.exists(self.test_pdf), f"Missing test PDF: {self.test_pdf}")

    def test_read_pdf_initializes_reader(self):
        """Ensure PDF reader is initialized after reading"""
        self.converter.read_pdf()
        self.assertIsNotNone(self.converter.pdf_reader, "PDF reader not initialized.")

    def test_convert_to_audio_runs_without_error(self):
        """Ensure audio conversion completes without exceptions"""
        self.converter.read_pdf()
        try:
            self.converter.convert_to_audio()
        except Exception as e:
            self.fail(f"convert_to_audio() raised an exception: {e}")

    def test_audio_file_created(self):
        """Verify MP3 file is generated"""
        self.converter.read_pdf()
        self.converter.convert_to_audio()
        self.assertTrue(os.path.exists(self.test_output), "Output MP3 file not created.")

    def tearDown(self):
        """Clean up generated test audio file"""
        if os.path.exists(self.test_output):
            os.remove(self.test_output)

if __name__ == "__main__":
    unittest.main()
