"""
Resume Intelligence Engine - Latest Job Title Field Extractor (Hierarchical/Semantic Heuristics)
--------------------------------------------------------------------------------------------------
Author: Sanjeet Prasad
Email: sanjeet8.23@gmail.com
Date: October 26, 2025

NEW ROBUST IMPLEMENTATION based on Hierarchical and Semantic Parsing Design Proposal.
"""

import re
from datetime import datetime
from typing import Optional, List, Dict
import dateparser
from fuzzywuzzy import fuzz
from extractor.fields.base import BaseFieldExtractor
from extractor.utils.constants import (
    WORK_EXPERIENCE_HEADERS,       
    CURRENT_JOB_KEYWORDS,           
    JOB_TITLE_NOISE_PATTERNS,       
    TITLE_ABBREVIATIONS,            
    JOB_TITLE_INDICATORS,           
    TITLE_ACRONYMS                  
)

class ResumeJobTitleField(BaseFieldExtractor):
    """
    Extracts the current or most recent job title from a resume using a robust,
    hierarchical parsing model.
    """
    SECTION_HEADERS = WORK_EXPERIENCE_HEADERS     
    CURRENT_EMPLOYMENT_KEYWORDS = CURRENT_JOB_KEYWORDS
    TITLE_NOISE_PATTERNS = JOB_TITLE_NOISE_PATTERNS
    ABBREVIATIONS = TITLE_ABBREVIATIONS
    TITLE_INDICATORS = JOB_TITLE_INDICATORS

    def extract(self) -> str:

        if self.debug:
            self.logger.debug("=" * 70)
            self.logger.debug("🚀 Starting Latest Job Title Extraction (Hierarchical Model)")
            self.logger.debug("=" * 70)

        # STRATEGY 0: Check Career Summary/Header for current role mention (High Priority)
        current_title = self._extract_title_from_header()
        if current_title:
            if self.debug:
                self.logger.debug(f"🎉 FINAL RESULT (Header Strategy): {current_title}")
            return current_title

        # Stage 1: Segmentation
        work_exp_section = self._find_work_experience_section()
        work_exp_section = self._ensure_text(work_exp_section)
        if not work_exp_section:
            if self.debug:
                self.logger.debug("⚠️ No work experience section found. Checking for 'Fresher' or 'Trainee' keywords.")
            
            # FALLBACK: Scan the whole text for "fresher", "trainee", or "intern" as a title
            # This pattern looks for a title-like phrase (4-30 chars) ending in one of the keywords
            fresher_pattern = r'\b([A-Za-z\s]{4,30}(?:trainee|fresher|intern))\b'
            # Avoid matching "objective" sentences
            avoid_pattern = r'(seeking|looking\s+for|objective|career|role\s+of)'

            for line in self.text.split('\n'):
                line_lower = line.lower().strip()
                
                # Avoid objective lines
                if re.search(avoid_pattern, line_lower):
                    continue

                match = re.search(fresher_pattern, line, re.IGNORECASE)
                if match:
                    # Found a potential title. Extract the matched group.
                    raw_title = match.group(1).strip()
                    title = self._clean_and_normalize_title(raw_title)

                    if title: 
                        if self.debug:
                            self.logger.debug(f"🎉 FINAL RESULT (Fresher Fallback): {title}")
                        return title

            if self.debug:
                self.logger.debug("❌ FAILED: No work experience section or 'Fresher' keywords found.")
            return "" # Exit if nothing is found
            
        # record absolute start offset of the work experience section for later position calculations
        work_section_start = self.text.find(work_exp_section) if work_exp_section else 0
        self._current_work_section_start = work_section_start
        job_entries = self._parse_job_entries(work_exp_section)

        if not job_entries:
            if self.debug:
                self.logger.debug("❌ FAILED: No job entries could be parsed")
            return ""

        # Stage 2: Structuring & Dating
        jobs_with_dates = self._extract_dates_from_jobs(job_entries)
        if not jobs_with_dates:
            if self.debug:
                self.logger.debug("❌ FAILED: No jobs with valid dates found")
            return ""

        # Stage 3: Prioritization
        latest_job = self._get_latest_job(jobs_with_dates)
        if not latest_job:
            if self.debug:
                self.logger.debug("❌ FAILED: Could not determine latest job")
            return ""

        title = self._extract_title_from_job(latest_job)

        if not title:
            # pragmatic fallback: search nearby parsed job blocks and the work experience text for a labelled Title:
            work_section_text = work_exp_section or self._find_work_experience_section() or self.text
            candidate = self._find_labelled_title_near(latest_job, jobs_with_dates, work_section_text, radius_chars=1200)
            if candidate:
                title = candidate
                if self.debug:
                    line_no = self._line_no_from_pos(latest_job.get('raw_position'))
                    self.logger.debug(f"    🔁 Fallback: found labelled title near latest job @ line {line_no}: {title}")
            else:
                if self.debug:
                    line_no = self._line_no_from_pos(latest_job.get('raw_position'))
                    self.logger.debug(f"❌ FAILED: Could not extract title from latest job @ line {line_no}")
                return ""
        
        if not title:
            if self.debug:
                self.logger.debug("❌ FAILED: Could not extract title from latest job")
            return ""

        if self.debug:
            self.logger.debug(f"🎉 FINAL RESULT: {title}")
        return title

    def _extract_title_from_header(self) -> Optional[str]:
        """STRATEGY 0: Extracts job title from the resume header/summary area."""
        header_text = self.text[:1500]

        # Look for "working as [TITLE] for/in/at [Company]"
        pattern = r'(?:presently|currently|working)\s+as\s+(\b[A-Z][a-zA-Z\s,]+?)(?:\s+for|\s+in|\s+at|\s*[,;:\n])'
        match = re.search(pattern, header_text, re.IGNORECASE)

        if match:
            raw_title = match.group(1).strip()
            title = self._clean_and_normalize_title(raw_title)
            # Ensure the extracted title looks like a job title
            if title and any(ind in title.lower() for ind in self.TITLE_INDICATORS) and len(title.split()) >= 2:
                if self.debug:
                    self.logger.debug(f"    💡 Header Title Found: {title}")
                return title
        
        # Secondary check for titles near the top but less explicitly labelled (e.g., Priti Kumari's resume)
        top_lines = header_text.split('\n')[:5]
        for line in top_lines:
            if re.search(r'\b(Analyst|Architect|Manager|Engineer|Lead)\b', line, re.IGNORECASE) and len(line.split()) < 10:
                # Exclude lines that are clearly just names or contact info
                if not re.match(r'^\s*[A-Z][a-z]+(\s+[A-Z][a-z]+)*\s*$', line):
                    title = self._clean_and_normalize_title(line)
                    if title and any(ind in title.lower() for ind in self.TITLE_INDICATORS):
                        if self.debug:
                             self.logger.debug(f"    💡 Header Title Found (Secondary): {title}")
                        return title
        
        return None

    def _find_work_experience_section(self) -> Optional[str]:
        """Identifies and returns the full work experience section."""
        # Existing logic is good for defining section boundaries
        text_lower = self.text.lower()
        best_position = -1
        
        for header in self.SECTION_HEADERS:
            # IMPROVED FIX: Use a pattern that reliably finds the header as a standalone title,
            # allowing for line breaks/bullets/non-word characters (OCR noise) before and after it.
            pattern = r'(?:\n|^)\s*(\W*)(' + re.escape(header) + r')(\W*)\s*'
            match = re.search(pattern, text_lower)
            
            if match:
                # Use match.start(2) to get the position of the captured header itself (it's the second group in the new pattern).
                header_start = match.start(2)
                
                if header_start < best_position or best_position == -1:
                    best_position = header_start

        if best_position == -1:
            return None
        
        section_start = best_position
        section_end = len(self.text)
        
        # Define end of section by finding the next major header
        for next_header in ["education", "skills", "projects", "certifications", "achievements", "academic"]:
            pattern = r'\b' + next_header + r'\b'
            # Start search a bit after the work experience header
            match = re.search(pattern, text_lower[section_start + 10:], re.IGNORECASE)
            if match:
                section_end = section_start + 10 + match.start()
                break

        return self.text[section_start:section_end].strip()

    def _parse_job_entries(self, work_exp_text: str) -> List[Dict[str, str]]:
        """
        STAGE 1.3: Robustly parses work experience section into individual job entries.
        Uses Date Ranges as primary anchors for segmentation.
        """
        job_entries = []
        work_exp_text = self._ensure_text(work_exp_text)
        # Pattern to find a reliable date range (Month YYYY - Month YYYY/Present)
        date_pattern = r'(\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*[\'’]?\s*\d{2,4}\s*[-–—]\s*(?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*[\'’]?\s*\d{2,4}|\b(?:Present|Till\s*Date|Current|Ongoing|--)\b))'
        
        # Find all date range matches and their positions
        date_matches = list(re.finditer(date_pattern, work_exp_text, re.IGNORECASE))
        
        # Use date match starts as the primary boundaries
        entry_positions = [m.start() for m in date_matches]
        
        # Also include position/title labels as secondary anchors if they are near the top of the text
        title_pattern = r'\b(?:role|title|designation|position)\s*[:\-\s]'
        title_matches = list(re.finditer(title_pattern, work_exp_text, re.IGNORECASE))
        
        # Add title matches that aren't immediately after a date match
        for m in title_matches:
            is_near_date = any(abs(m.start() - p) < 50 for p in entry_positions)
            if not is_near_date:
                 entry_positions.append(m.start())

        entry_positions = sorted(list(set(entry_positions)))

        if not entry_positions:
            if self.debug:
                self.logger.debug("    ⚠️ No strong date/title boundaries found, using line breaks as fallback.")
            return self._parse_unstructured_jobs(work_exp_text)

        if self.debug:
            self.logger.debug(f"    📍 Found {len(entry_positions)} entry boundaries (Date/Title Anchors)")

        # Create job blocks based on sorted boundaries
        for i, start in enumerate(entry_positions):
            end = entry_positions[i + 1] if i + 1 < len(entry_positions) else len(work_exp_text)
            entry_text = work_exp_text[start:end].strip()

            if len(entry_text) < 40:
                continue

            job_entries.append({
                'text': entry_text,
                'raw_position': start
            })

            if self.debug:
                preview = entry_text[:80].replace('\n', ' ')
                self.logger.debug(f"    📦 Job block {i+1}: {preview}...")

        return job_entries

    def _parse_unstructured_jobs(self, work_exp_text: str) -> List[Dict[str, str]]:
        """Fallback parser for unstructured work experience sections, groups by company name/title appearance."""
        # Simple fallback for cases where strong anchors fail
        job_entries = []
        lines = work_exp_text.split('\n')
        current_block = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Heuristic to detect a new job entry start
            is_new_job_start = (
                re.search(r'^\s*(\d+\.|\*|•|➤)\s*[A-Z][a-z]+', line) and 
                any(ind in line.lower() for ind in self.TITLE_INDICATORS) and
                not re.search(r'(responsibilities|description|project|skill)', line, re.IGNORECASE)
            )
            
            if is_new_job_start and current_block:
                block_text = '\n'.join(current_block)
                if len(block_text) > 40:
                    job_entries.append({'text': block_text, 'raw_position': len(job_entries)})
                current_block = [line]
            else:
                current_block.append(line)
        
        if current_block:
            block_text = '\n'.join(current_block)
            if len(block_text) > 40:
                job_entries.append({'text': block_text, 'raw_position': len(job_entries)})
        
        return job_entries


    def _extract_title_from_job(self, job_entry: Dict) -> Optional[str]:
        """
        STAGE 2.2: Extracts job title using a hierarchical tagging strategy.
        Improved to handle labelled Title lines that appear anywhere in the job block.
        """
        text = job_entry['text']
        lines = [l.rstrip() for l in text.split('\n')]

        # 0. Robust labelled-title anywhere in block (simple and forgiving)
        # Matches: Title: Senior Principal Engineer
        labelled_anywhere = re.search(r'\b(?:title|designation|role|position)\s*[:\-]\s*(.+)', text, re.IGNORECASE)
        if labelled_anywhere:
            raw_title = labelled_anywhere.group(1).strip()
            # Stop at common next-field cues if present on same line
            raw_title = re.split(r'\s{2,}|[,;|\n]|(?:Project Duration|Project Name|Client Name|Roles|Responsibilities)', raw_title, flags=re.IGNORECASE)[0]
            title = self._clean_and_normalize_title(raw_title)
            if title and any(ind in title.lower() for ind in self.TITLE_INDICATORS):
                if self.debug: self.logger.debug(f"    ✓ Title extracted (Labelled-anywhere): {title}")
                return title

        # 1. PRIORITY A (existing approach with non-consuming lookahead) -- keep as is but try without strict lookahead
        stop_keywords = r'(?=\s*(?:Project|Duration|Team|Client|Development|Description|Roles?|Organization|Company|Project\s*Name|Responsibilities|Date|Environment|Skills?)\s*[:\-\n]?)'
        pattern_labelled = r'(?:title|role|designation|position)\s*[:\-]\s*([A-Z][^\n]*?)' + stop_keywords
        match_labelled = re.search(pattern_labelled, text, re.IGNORECASE)
        if match_labelled:
            raw_title = match_labelled.group(1).strip()
            title = self._clean_and_normalize_title(raw_title)
            if title and any(ind in title.lower() for ind in self.TITLE_INDICATORS):
                if self.debug: self.logger.debug(f"    ✓ Title extracted (Labelled): {title}")
                return title


        # 2. PRIORITY B: Proximity/Position-Based Tagging (Top 6 lines)
        # Expand window to top 6 lines to catch titles that appear slightly lower
        for line in lines[:6]:
            line = line.strip()
            if not line:
                continue
            # permit titles with 1-8 words (covers "Senior Principal Engineer")
            if 3 <= len(line) <= 120 and 1 <= len(line.split()) <= 8:
                if any(ind in line.lower() for ind in self.TITLE_INDICATORS):
                    # FIX 1: Remove the exclusion for '\d{4}' (dates) as they often share the line with the title.
                    # Only exclude lines that look purely like a company or organization descriptor.
                    if not (re.search(r'(Pvt|LLC|Inc|Corp|Ltd|University)', line, re.IGNORECASE) or re.search(r'Client Name|Organization', line, re.IGNORECASE)):
                        
                         # FIX 2: Targeted extraction to strip leading company/number and trailing date from the line.
                        raw_title = line

                        # 1. Strip leading number/bullet point and potential company name (up to a major separator).
                        # This targets "1. Amazon Development center (Noida) - Senior Advisor..."
                        separator_match = re.search(r'[-–—:](.*)', raw_title)

                        if separator_match:
                            # If separator found, use everything after it as the raw title candidate
                            raw_title = separator_match.group(1).strip()
                        else:
                            # Fallback: If no clear separator, just strip the leading bullet/number
                            raw_title = re.sub(r'^\s*(\d+\.|\*|•|➤)\s*', '', raw_title).strip()
                            
                        # 2. Remove date info/parentheses from the end, which _clean_and_normalize_title will handle
                        # but we strip common post-title noise here for better focus.
                        # The cleaning function already removes all parentheses, so we primarily rely on that.

                        title = self._clean_and_normalize_title(raw_title)
                        
                        if title and any(ind in title.lower() for ind in self.TITLE_INDICATORS):
                            if self.debug: self.logger.debug(f"    ✓ Title extracted (Proximity): {title}")
                            return title

        # 3. PRIORITY C: Unlabelled Title with Company/Date Context (wider scan)
        # Look for a candidate title line that has a title indicator and appears above a company/date context
        for i in range(max(0, len(lines) - 1)):
            line = lines[i].strip()
            if not line:
                continue
            if any(ind in line.lower() for ind in self.TITLE_INDICATORS):
                # search the next up-to-4 lines for company/date/context
                context_window = ' '.join(lines[i+1:i+5]).strip()
                if re.search(r'(Company|Organization|Client|University|Pvt|Ltd|Corp)', context_window, re.IGNORECASE) or self._parse_dates_from_text(context_window):
                    title = self._clean_and_normalize_title(line)
                    if title:
                        if self.debug: self.logger.debug(f"    ✓ Title extracted (Context-wide): {title}")
                        return title

        # 4. Final fallback: try to find a concise title-like phrase anywhere (common multi-word patterns)
        # e.g., "Senior Principal Engineer" not labelled, not near top but present inside block
        matches = re.findall(r'([A-Z][A-Za-z&/\-\s]{3,60}(?:Engineer|Lead|Manager|Developer|Architect|Analyst|Principal|Specialist|Consultant|Technician|Administrator|Director))', text)
        for m in matches:
            title = self._clean_and_normalize_title(m.strip())
            if title and any(ind in title.lower() for ind in self.TITLE_INDICATORS):
                if self.debug: self.logger.debug(f"    ✓ Title extracted (Pattern-any): {title}")
                return title

        return None

    def _find_labelled_title_near(self, latest_job: Dict, all_jobs: List[Dict], work_section_text: str, radius_chars: int = 1200) -> Optional[str]:
        """
        Fallback: search for a labelled Title: ... anywhere near the latest_job position.
        Prioritize other current job blocks first, ordered by proximity to the latest_job raw_position.
        radius_chars controls how many characters before/after latest_job raw_position we scan in the full resume.
        Returns a normalized title string or None.
        """
        start_pos = latest_job.get('raw_position', 0) or 0

        # Prioritize current jobs first, then by absolute proximity to latest_job
        def proximity(j): 
            return abs((j.get('raw_position') or 0) - start_pos)
        prioritized = sorted(all_jobs, key=lambda j: (0 if j.get('is_current') else 1, proximity(j)))

        # 1) Search other parsed job blocks (prefer current blocks)
        for job in prioritized:
            if job is latest_job:
                continue
            text = job.get('text', '') or ''
            m = re.search(r'\b(?:title|designation|role|position)\s*[:\-]\s*(.+)', text, re.IGNORECASE)
            if m:
                candidate = m.group(1).strip()
                candidate = re.split(r'\s{2,}|[,;|\n]|(?:Project Duration|Project Name|Client Name|Roles|Responsibilities)', candidate, flags=re.IGNORECASE)[0]
                title = self._clean_and_normalize_title(candidate)
                if title:
                    return title

        # 2) As a last resort, search the raw work section text around latest_job absolute position
        # Ensure we search in the full resume text so raw_position is interpreted as absolute offset.
        full_text = self.text or work_section_text or ''
        search_start = max(0, start_pos - radius_chars)
        search_end = min(len(full_text), start_pos + radius_chars)
        snippet = full_text[search_start:search_end]

        m = re.search(r'\b(?:title|designation|role|position)\s*[:\-]\s*(.+)', snippet, re.IGNORECASE)
        if m:
            candidate = m.group(1).strip()
            candidate = re.split(r'\s{2,}|[,;|\n]|(?:Project Duration|Project Name|Client Name|Roles|Responsibilities)', candidate, flags=re.IGNORECASE)[0]
            title = self._clean_and_normalize_title(candidate)
            if title:
                return title

        return None

    def _line_no_from_pos(self, pos: int) -> int:
        """Return 1-based resume line number for a character offset position in self.text."""
        if pos is None or pos < 0:
            return -1
        return (self.text[:pos].count('\n') + 1) if self.text else -1

    def _get_latest_job(self, jobs_with_dates: List[Dict]) -> Optional[Dict]:
        """STAGE 3: Prioritizes current jobs and then most recent past jobs."""
        if not jobs_with_dates:
            return None
        
        current_jobs = [job for job in jobs_with_dates if job.get('is_current')]
        past_jobs = [job for job in jobs_with_dates if not job.get('is_current')]

        if current_jobs:
            # Sort current jobs by the latest start date (most recently started job is latest)
            latest_job = max(current_jobs, key=lambda x: x.get('start_date').timestamp() if x.get('start_date') else 0)
            if self.debug: self.logger.debug(f"    🏆 Latest Job (Current): {latest_job.get('date_str')}")
            return latest_job
        
        if past_jobs:
            # Sort past jobs by the latest end date
            latest_job = max(past_jobs, key=lambda x: x.get('end_date').timestamp() if x.get('end_date') else 0)
            if self.debug: self.logger.debug(f"    🏆 Latest Job (Past): {latest_job.get('date_str')}")
            return latest_job
            
        return None

    def _extract_dates_from_jobs(self, job_entries: List[Dict]) -> List[Dict]:
        """Extracts start and end dates from each job entry and attaches status.
        If no dates are found for a block we keep it as a candidate (is_current False)
        so downstream logic can still extract titles from undated job blocks.
        """
        jobs_with_dates = []

        for entry in job_entries:
            text = entry['text']
            date_info = self._parse_dates_from_text(text)

            if date_info:
                entry['start_date'] = date_info['start_date']
                entry['end_date'] = date_info['end_date']
                entry['is_current'] = date_info['is_current']
                entry['date_str'] = date_info['date_str']
                jobs_with_dates.append(entry)

                if self.debug:
                    status = "CURRENT" if date_info['is_current'] else "PAST"
                    self.logger.debug(f"    📅 Job Block @ {entry.get('raw_position')}: {date_info['date_str']} ({status})")
            else:
                # Keep undated blocks as candidates for title extraction and fallback heuristics
                entry['start_date'] = None
                entry['end_date'] = None
                entry['is_current'] = False
                entry['date_str'] = None
                jobs_with_dates.append(entry)

                if self.debug:
                    self.logger.debug(f"    ⚠️  No dates found for job block @ {entry.get('raw_position')} - kept as undated candidate")

        return jobs_with_dates

    def _parse_dates_from_text(self, text: str) -> Optional[Dict]:
        """Parses date range from job entry text."""
        date_range_patterns = [
            # Pattern 1: Month 'YY - Month 'YY/Present (e.g., Jul’20 - Present)
            r'(\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*[\'’]?\s*\d{2,4})\s*[-–—]\s*(\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*[\'’]?\s*\d{2,4}|\b(?:Present|Till\s*Date|Current|Ongoing|--)\b)',
            # Pattern 2: YYYY - YYYY/Present
            r'\(?(\d{4})\s*[-–—]+\s*(\d{4}|present|current|till\s*date)\)?',
            # Pattern 3: MM/YYYY - MM/YYYY
            r'(\d{1,2}/\d{4})\s*[-–—]+\s*(\d{1,2}/\d{4}|present|current|till\s*date)',
        ]
        
        for pattern in date_range_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                start_str = match.group(1).replace('’', "'")
                end_str = match.group(2).replace('’', "'") if match.lastindex >= 2 and match.group(2) else None
                
                is_current = False
                if end_str:
                    is_current = any(keyword in end_str.lower() for keyword in self.CURRENT_EMPLOYMENT_KEYWORDS) or end_str == '--'
                
                start_date = self._parse_single_date(start_str)
                
                if is_current or not end_str:
                    end_date = datetime.now()
                    is_current = True
                else:
                    end_date = self._parse_single_date(end_str)
                
                if start_date or end_date:
                    return {
                        'start_date': start_date,
                        'end_date': end_date,
                        'is_current': is_current,
                        'date_str': match.group(0),
                    }
        
        return None

    def _parse_single_date(self, date_str: str) -> Optional[datetime]:
        """Parses a single date string into datetime object."""
        try:
            # First, try robust dateparser
            parsed = dateparser.parse(
                date_str,
                settings={
                    'PREFER_DAY_OF_MONTH': 'first',
                    'PREFER_DATES_FROM': 'past',
                    'RETURN_AS_TIMEZONE_AWARE': False
                }
            )
            if parsed:
                return parsed
        except Exception:
            pass
        
        # Manual fallback for common resume formats (e.g., 'Mar 15', 'Jul 20')
        manual_patterns = [
            (r'([A-Z][a-z]+)\s*[\']?(\d{4})', lambda m: datetime.strptime(f"{m.group(1)} {m.group(2)}", '%B %Y')),
            (r'([A-Z][a-z]{2,})\s*[\']?(\d{2})', lambda m: datetime.strptime(f"{m.group(1)} 20{m.group(2)}", '%b %Y')),
            (r'(\d{1,2})/(\d{4})', lambda m: datetime(int(m.group(2)), int(m.group(1)), 1)),
            (r'^(\d{4})$', lambda m: datetime(int(m.group(1)), 1, 1)),
        ]
        
        for pattern, parser in manual_patterns:
            match = re.match(pattern, date_str.strip(), re.IGNORECASE)
            if match:
                try:
                    return parser(match)
                except (ValueError, AttributeError):
                    continue
        
        return None

    def _clean_and_normalize_title(self, title: str) -> str:
        """Cleans and normalizes the extracted title."""
        if not title:
            return ""
        
        ACRONYMS = {'CEO', 'CTO', 'CFO', 'CIO', 'CMO', 'COO', 'VP', 'SVP', 'EVP', 'AVP', 
                    'IT', 'HR', 'QA', 'UI', 'UX', 'AI', 'ML', 'SME', 'POC', 'R&D', 'SA'}
        
        # Remove noise patterns
        for noise_pattern in self.TITLE_NOISE_PATTERNS:
            title = re.sub(noise_pattern, '', title, flags=re.IGNORECASE)
        
        # Remove anything in parentheses unless it's an acronym
        title = re.sub(r'\s*\([^)]*\)', '', title)
        
        # Expand abbreviations
        words = title.split()
        expanded_words = []
        
        for word in words:
            word_clean = word.lower().rstrip('.')
            if word_clean in self.ABBREVIATIONS:
                expanded_words.append(self.ABBREVIATIONS[word_clean])
            else:
                expanded_words.append(word)
        
        title = ' '.join(expanded_words)
        title = re.sub(r'^[,;:\-–—\|\s]+|[,\-–—\|\s]+$', '', title) # Clean leading/trailing punctuation
        title = re.sub(r'\s+', ' ', title)
        title = re.sub(r'\s+[-–—]\s+', ' ', title)
        title = re.sub(r'\s*\band\b\s*', ' and ', title, flags=re.IGNORECASE)
        title = title.strip()
        
        if len(title) < 3 or len(title) > 120:
            return ""
        
        if not re.search(r'[a-zA-Z]{3,}', title):
            return ""
        
        # Title case formatting
        if title.islower() or title.isupper():
            parts = re.split(r'(\s+|-)', title)
            title_cased = []
            
            for part in parts:
                if part.strip() and part not in [' ', '-']:
                    if len(part) <= 3 and part.upper() in ACRONYMS:
                        title_cased.append(part.upper())
                    else:
                        title_cased.append(part.title())
                else:
                    title_cased.append(part)
            
            title = ''.join(title_cased)
        
        return title
        
        
    def _ensure_text(self, s: Optional[str]) -> str:
        """
        Return a safe string for regex and parsing functions.
        Normalizes None to empty string and coerces bytes to str when needed.
        Also strips common null whitespace so downstream length checks behave.
        """
        if s is None:
            return ""
        if isinstance(s, bytes):
            try:
                s = s.decode("utf-8", errors="ignore")
            except Exception:
                s = s.decode("latin-1", errors="ignore")
        # ensure str type
        s = str(s)
        # normalize NULs and weird whitespace
        s = s.replace("\x00", " ").strip()
        return s