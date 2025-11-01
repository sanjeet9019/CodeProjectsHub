#############################################################################
###  Author       : Sanjeet Prasad                                       ###
###  Email        : sanjeet8.23@gmail.com                                ###
###  Description  : PDF to MP3 Audio Converter – Speech Synthesis Tool   ###
###                 Reads multi-page PDF and converts it to speech/audio ###
###  Date         : 24-10-2025#############################################################################
###  Author       : Sanjeet Prasad                                       ###
###  Email        : sanjeet8.23@gmail.com                                ###
###  Description  : PDF to MP3 Audio Converter – Speech Synthesis Tool   ###
###                 Reads multi-page PDF and converts it to speech/audio ###
###  Date         : 03-05-2023                                           ###
###  Interpreter  : Python 3.11.0                                        ###
#############################################################################

import pyttsx3   # Text-to-speech library: https://pyttsx3.readthedocs.io/en/latest/
import PyPDF2    # PDF parser: https://pypdf2.readthedocs.io/en/3.0.0/
import os
from tqdm import tqdm

class PDFToAudioConverter:
    """
    Converts a multi-page PDF document into an MP3 audio file using pyttsx3.
    """

    def __init__(self, pdf_path="data/input.pdf", audio_output="data/output.mp3"):
        self.pdf_path = pdf_path
        self.audio_output = audio_output
        self.tts_engine = pyttsx3.init()
        self.pdf_reader = None
        self.pdf_file = None
        self.word_count = 0

    def read_pdf(self):
        """Open and load PDF pages"""
        if not os.path.exists(self.pdf_path):
            print(f"❌ PDF file '{self.pdf_path}' not found.")
            return

        try:
            self.pdf_file = open(self.pdf_path, "rb")
            self.pdf_reader = PyPDF2.PdfReader(self.pdf_file)
            print(f"📄 Loaded PDF: {self.pdf_path} with {len(self.pdf_reader.pages)} pages.")
        except Exception as e:
            print(f"⚠️ Error reading PDF: {e}")

    def convert_to_audio(self):
        """Convert each page of PDF to audio and save to MP3"""
        if not self.pdf_reader:
            print("⚠️ PDF reader not initialized.")
            return

        all_text = ""
        try:
            for page_num, page in tqdm(enumerate(self.pdf_reader.pages), total=len(self.pdf_reader.pages), desc="🔄 Processing pages"):
                try:
                    text = page.extract_text()
                    if text:
                        preview = text[:200].replace("\n", " ")
                        print(f"\n🗣️ Page {page_num + 1} Preview:\n{preview}...\n")
                        all_text += text + "\n"
                    else:
                        print(f"⚠️ Page {page_num + 1} contains no readable text.")
                except Exception as e:
                    print(f"⚠️ Error extracting text from page {page_num + 1}: {e}")
        except KeyboardInterrupt:
            print("\n⛔ Conversion interrupted by user during page processing.")
            return

        if all_text:
            self.word_count = len(all_text.split())
            estimated_minutes = self.word_count / 150

            try:
                self.tts_engine.say(all_text)
                self.tts_engine.save_to_file(all_text, self.audio_output)
                self.tts_engine.runAndWait()
                self.tts_engine.stop()
                print(f"\n✅ Audio saved to '{self.audio_output}'")
                print(f"🕒 Estimated audio duration: ~{estimated_minutes:.2f} minutes")
            except KeyboardInterrupt:
                print("\n⛔ Conversion interrupted by user during audio synthesis.")
            except Exception as e:
                print(f"⚠️ Error converting to speech: {e}")

    def run(self):
        """Run full PDF-to-audio conversion pipeline"""
        print("\n🔧 Starting PDF to MP3 Conversion...\n")
        try:
            self.read_pdf()
            self.convert_to_audio()
        except KeyboardInterrupt:
            print("\n⛔ Conversion interrupted by user.")
        finally:
            if self.pdf_file:
                self.pdf_file.close()

        if self.pdf_reader:
            estimated_minutes = self.word_count / 150
            print("\n📊 Summary:")
            print(f"   📄 Pages processed     : {len(self.pdf_reader.pages)}")
            print(f"   🔊 Words synthesized   : {self.word_count}")
            print(f"   💾 Output file         : {self.audio_output}")
            print(f"   🕒 Estimated duration  : ~{estimated_minutes:.2f} minutes")

        print("\n🎧 Conversion Complete.\n")
                                           ###
###  Interpreter  : Python 3.11.0                                        ###
#############################################################################

import pyttsx3   # Text-to-speech library: https://pyttsx3.readthedocs.io/en/latest/
import PyPDF2    # PDF parser: https://pypdf2.readthedocs.io/en/3.0.0/
import os

class PDFToAudioConverter:
    """
    Converts a multi-page PDF document into an MP3 audio file using pyttsx3.
    """

    def __init__(self, pdf_path="data/input.pdf", audio_output="data/output.mp3"):
        self.pdf_path = pdf_path
        self.audio_output = audio_output
        self.tts_engine = pyttsx3.init()
        self.pdf_reader = None
        self.pdf_file = None  # Keep file reference open during processing
        self.word_count = 0

    def read_pdf(self):
        """Open and load PDF pages"""
        if not os.path.exists(self.pdf_path):
            print(f"❌ PDF file '{self.pdf_path}' not found.")
            return

        try:
            self.pdf_file = open(self.pdf_path, "rb")
            self.pdf_reader = PyPDF2.PdfReader(self.pdf_file)
            print(f"📄 Loaded PDF: {self.pdf_path} with {len(self.pdf_reader.pages)} pages.")
        except Exception as e:
            print(f"⚠️ Error reading PDF: {e}")

    def convert_to_audio(self):
        """Convert each page of PDF to audio and save to MP3"""
        if not self.pdf_reader:
            print("⚠️ PDF reader not initialized.")
            return

        all_text = ""
        for page_num, page in enumerate(self.pdf_reader.pages):
            try:
                text = page.extract_text()
                if text:
                    print(f"\n🗣️ Page {page_num + 1} Text:\n{text}\n")
                    all_text += text + "\n"
                else:
                    print(f"⚠️ Page {page_num + 1} contains no readable text.")
            except Exception as e:
                print(f"⚠️ Error extracting text from page {page_num + 1}: {e}")

        if all_text:
            self.word_count = len(all_text.split())
            estimated_minutes = self.word_count / 150  # Assuming 150 words/minute

            try:
                self.tts_engine.say(all_text)
                self.tts_engine.save_to_file(all_text, self.audio_output)
                self.tts_engine.runAndWait()
                self.tts_engine.stop()
                print(f"\n✅ Audio saved to '{self.audio_output}'")
                print(f"🕒 Estimated audio duration: ~{estimated_minutes:.2f} minutes")
            except Exception as e:
                print(f"⚠️ Error converting to speech: {e}")

    def run(self):
        """Run full PDF-to-audio conversion pipeline"""
        print("\n🔧 Starting PDF to MP3 Conversion...\n")
        self.read_pdf()
        self.convert_to_audio()
        if self.pdf_file:
            self.pdf_file.close()

        if self.pdf_reader:
            estimated_minutes = self.word_count / 150
            print("\n📊 Summary:")
            print(f"   📄 Pages processed     : {len(self.pdf_reader.pages)}")
            print(f"   🔊 Words synthesized   : {self.word_count}")
            print(f"   💾 Output file         : {self.audio_output}")
            print(f"   🕒 Estimated duration  : ~{estimated_minutes:.2f} minutes")

        print("\n🎧 Conversion Complete.\n")
