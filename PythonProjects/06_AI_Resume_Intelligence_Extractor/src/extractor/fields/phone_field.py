"""
Field extractor for phone number from resume text.

Uses multiple strategies including:
1. Indian formats with +91
2. 10-digit mobile numbers
3. International formats
4. Hyphenated or dotted formats
5. Labeled fields like "Phone: ..."
"""

import re
from extractor.fields.base import BaseFieldExtractor

class ResumePhoneField(BaseFieldExtractor):
    def extract(self):
        # Strategy 1: Indian format with +91
        pattern_1 = r"\+91\s?\d{10}"

        # Strategy 2: Indian mobile number without country code
        pattern_2 = r"\b[6-9]\d{9}\b"

        # Strategy 3: International formats
        pattern_3 = r"\+\d{1,3}[-\s]?\d{6,12}"

        # Strategy 4: Hyphenated or dotted formats
        pattern_4 = r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b"

        # Strategy 5: Labeled fields like "Phone: 1234567890"
        pattern_5 = r"(?i)(mobile|phone|contact)\s*[:\-]?\s*(\+?\d[\d\s\-\.]{8,})"

        patterns = [pattern_1, pattern_2, pattern_3, pattern_4, pattern_5]

        for idx, pattern in enumerate(patterns):
            matches = re.findall(pattern, self.text)
            if self.debug:
                self.logger.debug(f"Pattern {idx+1}: {pattern}")
                self.logger.debug(f"Matches: {matches}")

            if matches:
                # If pattern returns tuples (label, number), extract the number
                if isinstance(matches[0], tuple):
                    phone = matches[0][1].strip()
                else:
                    phone = matches[0].strip()

                if self.debug:
                    self.logger.debug(f"✅ Matched phone: {phone}")
                return phone

        if self.debug:
            self.logger.debug("No phone number found.")
        return "Not found"

