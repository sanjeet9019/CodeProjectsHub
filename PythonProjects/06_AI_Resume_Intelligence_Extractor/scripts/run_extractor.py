"""
Resume Intelligence Parser
-----------------------------------------
Author: Sanjeet Prasad
Email: sanjeet8.23@gmail.com
Description: Extracts structured insights from resume PDFs using a modular, extensible Python engine.
Date: October 25, 2025

Features:
- Single resume file (PDF)
- Optional debug mode (--debug)
- Optional field selection (--fields name,email,skills)
- Batch mode (--all): parses all PDFs in data/resumes/
- Auto-saves output as CSV in data/output/
"""

import sys
import os
import argparse
import time 

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from extractor.utils.logger import LoggerFactory
from extractor.resume_parser import ResumeParser
from extractor.fields.score_field import ResumeScoreField
from extractor.fields.techstack_field import ResumeTechStackField
from extractor.fields.jobtitle_field import ResumeJobTitleField
from extractor.fields.skills_field import ResumeSkillsField
from extractor.utils.exporter import ResumeExporter
from extractor.utils.cleanup import remove_pycache

def display_field(label, value):
    if isinstance(value, (list, set)) and not value:
        return f"{label}: Not found"
    if isinstance(value, str) and value.strip().lower() == "not found":
        return f"{label}: Not found"
    return f"{label}: {value}"

def display_stack(label, items):
    if not items:
        return f"    - {label}: Not found"
    return f"    - {label}: {', '.join(items)}"

def main():
    parser = argparse.ArgumentParser(
        description="Resume Intelligence Extractor",
        epilog="Examples:\n"
             "\n"
             "  py scripts/run_extractor.py                                 # Uses default SampleResume.pdf\n"
             "  py scripts/run_extractor.py data/resumes/SampleResume.pdf # Parse specific resume\n"
             "  py scripts/run_extractor.py --all                           # Parse all resumes in data/resumes/\n"
             "  py scripts/run_extractor.py resume.pdf --fields name,email --debug-job-title\n",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("file", nargs="?", default="data/resumes/SampleResume.pdf")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging for all fields")
    parser.add_argument("--debug-job-title", action="store_true", help="Enable debug logging only for job title extractor")
    parser.add_argument("--debug-skills", action="store_true", help="Enable debug logging only for skills extractor")
    parser.add_argument("--debug-score", action="store_true", help="Enable debug logging only for score extractor")
    parser.add_argument("--debug-techstack", action="store_true", help="Enable debug logging only for tech stack extractor")
    parser.add_argument("--fields", help="Comma-separated list of fields to extract (e.g., name,email,skills)")
    parser.add_argument("--all", action="store_true", help="Parse all PDFs in data/resumes/")

    args = parser.parse_args()
    logger = LoggerFactory(debug=args.debug).get_logger("ResumeExtractor")
    selected_fields = args.fields.split(",") if args.fields else None

    resume_files = []
    if args.all:
        resume_dir = "data/resumes"
        if not os.path.isdir(resume_dir):
            logger.error("Folder not found: data/resumes/")
            sys.exit(1)
        resume_files = [os.path.join(resume_dir, f) for f in os.listdir(resume_dir) if f.lower().endswith(".pdf")]
        if not resume_files:
            logger.warning("No PDF resumes found in data/resumes/")
            sys.exit(1)
    else:
        if not os.path.isfile(args.file):
            logger.error(f"File not found: {args.file}")
            print("💡 Tip: Place your resume at data/resumes/SampleResume.pdf or use --all to process all.")
            sys.exit(1)
        resume_files = [args.file]

    # --- START MODIFIED LOGIC FOR TIMING ---
    global_start_time = time.time()
    
    for resume_path in resume_files:
        print(f"\n📂 Processing: {resume_path}")
        filename = os.path.basename(resume_path)
        
        timing_data = {}
        total_extraction_time = 0

        # Phase 1: Core Fields (Parser Initialization & Core Extraction)
        start_time_core = time.time()
        engine = ResumeParser(file_path=resume_path, debug=args.debug, selected_fields=selected_fields)
        results = engine.extract_all()
        end_time_core = time.time()
        duration_core = end_time_core - start_time_core
        timing_data["Core Fields (Name, Email, Exp, Loc)"] = duration_core
        total_extraction_time += duration_core

        # Phase 2: Individual Field Extractors (Job Titles, Skills, Tech Stack, Score)

        # 1. Job Titles
        start_time = time.time()
        job_titles = ResumeJobTitleField(engine.text, engine.doc, debug=args.debug or args.debug_job_title).extract()
        end_time = time.time()
        duration = end_time - start_time
        timing_data["Job Titles"] = duration
        total_extraction_time += duration

        # 2. Skills
        start_time = time.time()
        skills = ResumeSkillsField(engine.text, engine.doc, debug=args.debug or args.debug_skills).extract()
        end_time = time.time()
        duration = end_time - start_time
        timing_data["Skills"] = duration
        total_extraction_time += duration
        
        # Pull core fields from results for use in subsequent extractors
        companies = results.get("companies", [])
        name = results.get("name", "Not found")
        email = results.get("email", "Not found")
        phone = results.get("phone", "Not found")

        # 3. Tech Stack (Dependent on Skills)
        start_time = time.time()
        if skills:
            techstack = ResumeTechStackField(engine.text, debug=args.debug or args.debug_techstack).extract(skills)
        else:
            techstack = ([], [], [])
            if args.debug or args.debug_techstack:
                logger.warning("Tech stack skipped: no skills provided")
        end_time = time.time()
        duration = end_time - start_time
        timing_data["Tech Stack"] = duration
        total_extraction_time += duration

        # 4. Resume Score
        start_time = time.time()
        score = ResumeScoreField(engine.text, debug=args.debug or args.debug_score).extract(
            name=name, email=email, phone=phone,
            job_titles=job_titles, skills=skills, companies=companies
        )
        end_time = time.time()
        duration = end_time - start_time
        timing_data["Resume Score"] = duration
        total_extraction_time += duration
        
        # --- END OF EXTRACTION AND TIMING ---

        logger.debug(f"Extracted name: {name}")
        logger.debug(f"Extracted email: {email}")
        logger.debug(f"Extracted phone: {phone}")
        logger.debug(f"Extracted skills: {skills}")
        logger.debug(f"Extracted job titles: {job_titles}")
        logger.debug(f"Extracted companies: {companies}")
        logger.debug(f"Extracted score: {score}")

        job_titles_display = ", ".join(job_titles) if isinstance(job_titles, list) else job_titles

        # --- DISPLAY RESULTS ---
        print("\n📄 Final Resume Intelligence Output")
        print("👤 Name:", name)
        print("📧 Email:", email)
        print("📞 Phone:", phone)
        print(display_field("📍 Current Location", results.get("location")))
        print(display_field("🛠️ Skills", ", ".join(sorted(skills)) if skills else "Not found"))
        print(display_field("💼 Job Titles", job_titles_display))
        print(display_field("🏢 Companies", ", ".join(companies) if companies else "Not found"))
        print(display_field("🗓️ Total Experience", results.get("experience")))
        print(display_field("📊 Resume Score", score))
        print("🧠 Tech Stack:")
        print(display_stack("Languages", techstack[0]))
        print(display_stack("Tools", techstack[1]))
        print(display_stack("Platforms", techstack[2]))

        # --- DISPLAY TIMING (CONDITIONAL) ---
        if args.debug:
            print("\n⏱️ Execution Time Breakdown (DEBUG):")
            for module, duration in timing_data.items():
                print(f"    - {module:<36}: {duration:.4f} seconds")
            
            print("-" * 43)
            print(f"    - {'TOTAL EXTRACTION TIME':<36}: {total_extraction_time:.4f} seconds")
            print("-" * 43)
        # --- END DISPLAY TIMING ---

        exporter = ResumeExporter(output_dir="data/output")
        # Ensure only accepted arguments are passed to exporter.export()
        output_path = exporter.export(results, resume_filename=filename, techstack=techstack, score=score)

        print("\n📤 CSV Export Complete")
        print(f"📁 Saved to: {output_path}")
        remove_pycache()

if __name__ == "__main__":
    main()