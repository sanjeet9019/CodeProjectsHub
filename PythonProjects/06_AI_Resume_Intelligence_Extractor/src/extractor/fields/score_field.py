"""
Resume Intelligence Engine - ResumeScoreField
---------------------------------------------
Author: Sanjeet Prasad
Email: sanjeet8.23@gmail.com
Date: October 25, 2025

Field extractor for resume quality scoring.

Uses multiple criteria to assign a score out of 5:
1. Presence of name
2. Valid email and phone
3. Sufficient job titles
4. Sufficient skills
5. Sufficient companies
"""

from extractor.fields.base import BaseFieldExtractor
from extractor.utils.logger import LoggerFactory  # ✅ Use centralized logger

class ResumeScoreField(BaseFieldExtractor):
    def __init__(self, text, debug=False):
        super().__init__(text, debug)
        self.logger = LoggerFactory(debug=debug).get_logger(__name__)  # ✅ Initialize logger

    def extract(self, name=None, email=None, phone=None, job_titles=None, skills=None, companies=None):
        """
        Computes a resume score based on presence and richness of key fields.

        Args:
            name (str): Extracted name
            email (str): Extracted email
            phone (str): Extracted phone
            job_titles (list): Extracted job titles
            skills (set): Extracted skills
            companies (list): Extracted companies

        Returns:
            str: Score as "X/5"
        """
        score = 0

        # Strategy 1: Presence of name
        if name and name != "Not found":
            score += 1
            self.logger.debug("✅ Name present")

        # Strategy 2: Valid email and phone
        if email and email != "Not found" and phone and phone != "Not found":
            score += 1
            self.logger.debug("✅ Email and phone present")

        # Strategy 3: Sufficient job titles
        if job_titles and len(job_titles) >= 3:
            score += 1
            self.logger.debug(f"✅ Job titles count: {len(job_titles)}")

        # Strategy 4: Sufficient skills
        if skills and len(skills) >= 5:
            score += 1
            self.logger.debug(f"✅ Skills count: {len(skills)}")

        # Strategy 5: Sufficient companies
        if companies and len(companies) >= 3:
            score += 1
            self.logger.debug(f"✅ Companies count: {len(companies)}")

        self.logger.debug(f"📊 Final score: {score}/5")
        return f"{score}/5"
