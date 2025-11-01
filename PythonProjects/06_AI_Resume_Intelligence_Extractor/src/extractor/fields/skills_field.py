"""
Field extractor for technical skills from resume text.

Uses multiple strategies including:
1. Normalization of bullets, commas, and compound mentions
2. Regex-based keyword matching against known skills
"""

import re
from extractor.fields.base import BaseFieldExtractor
from extractor.utils.constants import known_skills

class ResumeSkillsField(BaseFieldExtractor):
    def extract(self):
        # Strategy 1: Normalize bullets and commas
        normalized_text = self.text.replace("", "\n").replace(",", "\n")

        # Strategy 2: Normalize compound mentions like "C/C++", "C and C++"
        normalized_text = re.sub(
            r"\bC\s*[/,\\&]*(\s*(and)?\s*)?C\+\+", "C\nC++", normalized_text, flags=re.IGNORECASE
        )

        found = set()

        # Strategy 3: Direct keyword match
        for skill in known_skills:
            pattern = rf"\b{re.escape(skill)}\b"
            if skill == "c++":
                pattern = r"(?<!\w)c\+\+(?!\w)"  # Special handling for C++
            if re.search(pattern, normalized_text, re.IGNORECASE):
                found.add(skill.lower())
                if self.debug:
                    self.logger.debug(f"✅ Matched skill: {skill}")

        if self.debug:
            self.logger.debug(f"Total skills found: {len(found)}")

        return found

