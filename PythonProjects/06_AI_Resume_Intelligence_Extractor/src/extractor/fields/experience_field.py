"""
Field extractor for total experience from resume text.

Uses multiple strategies including:
1. Date range parsing (e.g., "Jan 2010 – Mar 2020")
2. Phrase-based detection (e.g., "15+ years of experience")
3. Labeled fields like "Total Experience: 12 years"
4. Combines and selects best estimate
"""

import re
from datetime import datetime
from dateutil import parser as date_parser
from extractor.fields.base import BaseFieldExtractor

class ResumeExperienceField(BaseFieldExtractor):
    def extract(self):
        total_months = 0
        now = datetime.now()

        # Strategy 1: Extract date ranges like "Jan 2010 – Mar 2020"
        date_ranges = re.findall(
            r"([A-Za-z]{3,9}[\s']?\d{2,4})\s*[-–]\s*(?:([A-Za-z]{3,9}[\s']?\d{2,4})|(--))",
            self.text,
        )
        for start_str, end_str, dash in date_ranges:
            try:
                start_date = date_parser.parse(start_str, fuzzy=True)
                end_date = date_parser.parse(end_str, fuzzy=True) if end_str and end_str != "--" else now
                months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
                if months > 0:
                    total_months += months
                    if self.debug:
                        self.logger.debug(f"✅ Parsed range: {start_str} to {end_str or 'Present'} → {months} months")
            except Exception as e:
                if self.debug:
                    self.logger.debug(f"⚠️ Failed to parse range: {start_str} to {end_str} → {e}")

        # Strategy 2: Phrase-based detection like "15+ years of experience"
        yoe_matches = re.findall(
            r"\b(\d{1,2})\s*\+?\s*(?:years|yrs)\s+(?:of\s+)?experience\b",
            self.text,
            re.IGNORECASE,
        )

        # Strategy 3: Labeled phrases like "Total Experience: 12 years"
        yoe_phrases = re.findall(
            r"(?:total\s+)?(?:experience\s*[:\-]?\s*)(\d{1,2})\s*\+?\s*(?:years|yrs)",
            self.text,
            re.IGNORECASE,
        )

        # Strategy 4: Combine and choose best
        yoe_values = [int(y) for y in yoe_matches + yoe_phrases if int(y) < 50]
        yoe_from_text = max(yoe_values) if yoe_values else None

        years = total_months // 12
        months = total_months % 12

        if self.debug:
            self.logger.debug(f"🧮 Total months from ranges: {total_months} → {years}y {months}m")
            if yoe_from_text:
                self.logger.debug(f"📌 Phrase-based experience: {yoe_from_text}+ years")

        if yoe_from_text and yoe_from_text * 12 > total_months:
            return f"{yoe_from_text}+ years"
        return f"{years} years {months} months"

