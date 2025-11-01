"""
Field extractor for grouping technical skills into categories.

Uses strategies including:
1. Normalization of skill casing and spacing
2. Keyword matching against categorized sets:
   - Languages
   - Tools
   - Platforms
"""

from extractor.fields.base import BaseFieldExtractor

class ResumeTechStackField(BaseFieldExtractor):
    def extract(self, skills=None):
        """
        Groups extracted skills into categories: languages, tools, platforms.

        Args:
            skills (set): Raw skills extracted from ResumeSkillsField

        Returns:
            tuple: (languages, tools, platforms) — each as a sorted list
        """
        if not skills or not isinstance(skills, (set, list)):
            if self.debug:
                self.logger.debug("⚠️ No skills provided to group.")
            return [], [], []

        # Strategy 1: Normalize skill casing and spacing
        normalized_skills = {s.strip().lower() for s in skills if isinstance(s, str)}

        # Strategy 2: Match against categorized keywords
        language_keywords = {
            "c", "c++", "java", "python", "sql", "pl/sql", "apex", "soql", "r", "javascript"
        }
        tool_keywords = {
            "git", "jira", "valgrind", "wireshark", "makefile", "gdb", "visual studio",
            "salesforce", "data loader", "workbench", "omnistudio", "omniscript", "lightning components"
        }
        platform_keywords = {
            "linux", "windows", "macos", "as400", "mainframe"
        }

        languages = sorted(normalized_skills & language_keywords)
        tools = sorted(normalized_skills & tool_keywords)
        platforms = sorted(normalized_skills & platform_keywords)

        if self.debug:
            self.logger.debug(f"🧠 Languages: {languages}")
            self.logger.debug(f"🧰 Tools: {tools}")
            self.logger.debug(f"🖥️ Platforms: {platforms}")

        return languages, tools, platforms

