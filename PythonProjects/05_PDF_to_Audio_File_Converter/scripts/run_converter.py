#############################################################################
###  Author       : Sanjeet Prasad                                       ###
###  Email        : sanjeet8.23@gmail.com                                ###
###  Description  : CLI launcher for PDF to MP3 conversion               ###
###  Usage        : python scripts/run_converter.py                      ###
###  Date         : 03-05-2023                                           ###
###  Interpreter  : Python 3.11.0                                        ###
#############################################################################

import argparse
from src.pdfaudio.pdf_to_audio_converter import PDFToAudioConverter

def main():
    parser = argparse.ArgumentParser(
        description="Convert a PDF document to MP3 audio using text-to-speech."
    )
    parser.add_argument(
        "--pdf", type=str, default="data/input.pdf",
        help="Path to input PDF file (default: data/input)"
    )
    parser.add_argument(
        "--out", type=str, default="data/output.mp3",
        help="Path to output MP3 file (default: data/output.mp3)"
    )

    args = parser.parse_args()

    converter = PDFToAudioConverter(pdf_path=args.pdf, audio_output=args.out)
    converter.run()

if __name__ == "__main__":
    main()
