"""
ResumeExporter
--------------
Handles structured export of resume data to CSV.
Each resume gets its own CSV named after the input PDF.
"""

import csv
import os

class ResumeExporter:
    def __init__(self, output_dir="data/output", format="csv"):
        self.output_dir = output_dir
        self.format = format
        os.makedirs(self.output_dir, exist_ok=True)

    def export(self, data: dict, resume_filename: str, techstack: tuple = None, score: float = None):
        """
        Export resume data to a file named after the input PDF.

        Args:
            data (dict): Extracted resume fields
            resume_filename (str): Original PDF filename (e.g., SampleResume1.pdf)
            techstack (tuple): (languages, tools, platforms)
            score (float): Resume score
        """
        basename = os.path.splitext(resume_filename)[0]
        output_path = os.path.join(self.output_dir, f"{basename}.{self.format}")

        if self.format == "csv":
            self._export_csv(data, output_path, techstack, score)
        else:
            raise ValueError(f"Unsupported format: {self.format}")

        return output_path

    def _export_csv(self, data: dict, path: str, techstack: tuple, score: float):
        with open(path, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Field", "Value"])

            # Normalize and write fields
            for key, value in data.items():
                label = self._normalize_label(key)
                if isinstance(value, (list, set)):
                    value = "; ".join(sorted(value))
                writer.writerow([label, value])

            # Add tech stack breakdown
            if techstack:
                stack_str = (
                    f"Languages: {', '.join(techstack[0])}\n"
                    f"Tools: {', '.join(techstack[1])}\n"
                    f"Platforms: {', '.join(techstack[2])}"
                )
                writer.writerow(["Tech Stack", stack_str])

            # Add score
            if score is not None:
                writer.writerow(["Resume Score", score])

    def _normalize_label(self, key: str) -> str:
        """Convert internal field keys to human-readable labels."""
        mapping = {
            "name": "Name",
            "email": "Email",
            "phone": "Phone",
            "location": "Location",
            "skills": "Skills",
            "job_titles": "Job Titles",
            "companies": "Companies",
            "experience": "Total Experience",
            "score": "Resume Score",
            "tech_stack": "Tech Stack"
        }
        return mapping.get(key, key.replace("_", " ").title())
