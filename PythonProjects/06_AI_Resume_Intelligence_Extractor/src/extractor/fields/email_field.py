"""
Field extractor for email address from resume text.

Uses multiple strategies including:
1. Regex match for standard email formats
2. Labeled fields like "Email:"
3. Fallback to first valid match
"""

import re
from extractor.fields.base import BaseFieldExtractor

class ResumeEmailField(BaseFieldExtractor):
    def extract(self):
        # Strategy 1: Simple regex match
        email_pattern = r"\b[\w\.-]+@[\w\.-]+\.\w+\b"
        matches = re.findall(email_pattern, self.text)

        if self.debug:
            self.logger.debug(f"Found {len(matches)} email matches: {matches}")

        # Strategy 2: Prioritize labeled fields like "Email: xyz@abc.com"
        labeled_matches = re.findall(r"(?i)(email|e-mail)\s*[:\-]?\s*([\w\.-]+@[\w\.-]+\.\w+)", self.text)
        if labeled_matches:
            email = labeled_matches[0][1].strip()
            if self.debug:
                self.logger.debug(f"Strategy 2 matched labeled email: {email}")
            return email

        # Strategy 3: Fallback to first valid match
        if matches:
            email = matches[0].strip()
            if self.debug:
                self.logger.debug(f"Strategy 1 fallback matched: {email}")
            return email

        # No match found
        if self.debug:
            self.logger.debug("No email found.")
        return "Not found"

