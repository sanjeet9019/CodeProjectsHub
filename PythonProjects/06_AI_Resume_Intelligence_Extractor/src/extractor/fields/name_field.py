"""
Resume Intelligence Engine - ResumeNameField
--------------------------------------------
Author: Sanjeet Prasad
Email: sanjeet8.23@gmail.com
Date: October 25, 2025

Field extractor for candidate name from resume text.

Uses multiple strategies including:
1. First line heuristic
2. Proximity to email/phone
3. Top-of-document regex
4. Labeled fields like "Name:"
5. spaCy NER with regex validation
"""

import re
from extractor.fields.base import BaseFieldExtractor
from extractor.utils.logger import LoggerFactory  # ✅ Centralized logger

class ResumeNameField(BaseFieldExtractor):
    def __init__(self, text, doc=None, debug=False):
        super().__init__(text, doc, debug)
        self.logger = LoggerFactory(debug=debug).get_logger(__name__)  # ✅ Use LoggerFactory

    def extract(self):
        lines = [line.strip() for line in self.text.splitlines() if line.strip()]
        bad_first_line = {"resume", "curriculum vitae", "cv", "dw_tag_subprogram", "dma", "dmrc"}
        name = None

        # Strategy 1: First line heuristic
        first_line = lines[0] if lines else ""
        if first_line.lower() not in bad_first_line and len(first_line.split()) >= 2:
            if re.match(r"^([A-Z][a-z]+|[A-Z]+)(\s+([A-Z][a-z]+|[A-Z]+)){1,2}$", first_line):
                name = first_line
            elif re.match(r"^[A-Z]{2,}(?:\s+[A-Z]{2,}){1,2}$", first_line):
                name = first_line
            if name:
                self.logger.debug(f"Strategy 1 matched: {name}")

        # Strategy 2: Above email/phone
        if not name:
            email_pattern = r"\b[\w\.-]+@[\w\.-]+\.\w+\b"
            phone_pattern = r"\+91\s?\d{10}"
            for i, line in enumerate(lines):
                if re.search(email_pattern, line) or re.search(phone_pattern, line):
                    for j in range(max(0, i - 5), i):
                        candidate_line = lines[j].strip()
                        match = re.match(r"^([A-Z]{2,}(?:\s+[A-Z]{2,}){1,2})", candidate_line)
                        if match:
                            candidate = match.group(1)
                            if not re.search(r"(university|college|school|board|session|education)", candidate, re.IGNORECASE):
                                name = candidate
                                self.logger.debug(f"Strategy 2 matched: {name}")
                                break
                    if name:
                        break

        # Strategy 3: Top-of-document regex
        if not name:
            top_text = self.text[:500]
            name_matches = re.findall(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+|[A-Z]{2,}\s+[A-Z]{2,})\b", top_text)
            name_matches = [n for n in name_matches if n.lower() not in bad_first_line and len(n.split()) >= 2]
            if name_matches:
                name = name_matches[0]
                self.logger.debug(f"Strategy 3 matched: {name}")

        # Strategy 4: Labeled fields
        if not name:
            label_matches = re.findall(r"(?i)(name|candidate name)\s*[:\-]?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})", self.text)
            if label_matches:
                name = label_matches[0][1]
                self.logger.debug(f"Strategy 4 matched: {name}")

        # Strategy 5: spaCy NER
        if not name and self.doc:
            for ent in self.doc.ents:
                if ent.label_ == "PERSON" and len(ent.text.split()) >= 2:
                    candidate = ent.text.strip()
                    if re.search(r"(university|college|institute|school|session|board|percentage|education)", candidate, re.IGNORECASE):
                        continue
                    if re.match(r"^([A-Z][a-z]+|[A-Z]+)(\s+([A-Z][a-z]+|[A-Z]+)){1,2}$", candidate):
                        name = candidate
                        self.logger.debug(f"Strategy 5 matched: {name}")
                        break

        return name or "Not found"
