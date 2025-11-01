"""
Field extractor for company names from resume text.

Uses multiple strategies including:
1. Labeled fields like "Company: XYZ"
2. Table-like rows (e.g., <tr><td>Company</td>)
3. Phrase-based patterns like "at Amazon"
4. Cleanup and filtering of noisy matches
"""

import re
from extractor.fields.base import BaseFieldExtractor

class ResumeCompanyField(BaseFieldExtractor):
    def extract(self):
        candidates = []

        # Strategy 1: Match labeled fields
        label_patterns = [
            r"(?i)Organization\s*[:\-]?\s*([^\n]+)",
            r"(?i)Employer\s*[:\-]?\s*([^\n]+)",
            r"(?i)Company\s*[:\-]?\s*([^\n]+)",
        ]
        for pattern in label_patterns:
            matches = re.findall(pattern, self.text)
            candidates.extend(matches)
            if self.debug and matches:
                self.logger.debug(f"✅ Labeled field matches: {matches}")

        # Strategy 2: Extract from table-like rows
        table_rows = re.findall(r"<tr>\s*<td>([^<]+)</td>", self.text)
        candidates.extend([row.strip() for row in table_rows])
        if self.debug and table_rows:
            self.logger.debug(f"✅ Table row matches: {table_rows}")

        # Strategy 3: Phrase-based patterns
        phrase_patterns = [
            r"\bat\s+([A-Z][a-zA-Z0-9&.,\s]+)",
            r"\bworking\s+in\s+([A-Z][a-zA-Z0-9&.,\s]+)",
        ]
        for pattern in phrase_patterns:
            matches = re.findall(pattern, self.text)
            candidates.extend([match.strip() for match in matches])
            if self.debug and matches:
                self.logger.debug(f"✅ Phrase-based matches: {matches}")

        # Strategy 4: Clean and filter
        final = []
        for c in candidates:
            cleaned = re.sub(r"\(.*?\)", "", c)  # Remove text in parentheses
            cleaned = re.sub(r"\bas\s+a\b.*", "", cleaned, flags=re.IGNORECASE)
            cleaned = re.sub(
                r",?\s*(India|UK|United Kingdom|Bangalore|Noida|Gurgaon|Fleet|Hamshire).*",
                "", cleaned, flags=re.IGNORECASE
            )
            cleaned = cleaned.strip()
            if "FROM TO" in cleaned.upper():
                continue
            if 2 <= len(cleaned.split()) <= 6 and "client" not in cleaned.lower():
                final.append(cleaned)

        unique = sorted(set(final))
        if self.debug:
            self.logger.debug(f"✅ Final company list: {unique}")
        return unique

