"""
Resume Intelligence Engine - ResumeLocationField
------------------------------------------------
Author: Sanjeet Prasad
Email: sanjeet8.23@gmail.com
Date: October 25, 2025

Extracts current work location from resume text using multi-strategy ensemble scoring.

Strategies used:
    1. Labeled fields (e.g., "Location: Noida")
    2. Phrase-based patterns (e.g., "based in Bangalore")
    3. Experience blocks with city in parentheses (e.g., "Amazon (Noida) – Present")
    4. Address blocks (e.g., "Address: Sector-77, Noida")
    5. Training/project lines (e.g., "SLA Consultants India, Gurgaon")
    6. Near email/phone blocks
    7. spaCy NER (GPE entities)
    8. Current experience override (scans block around "Present" or "Current")
"""

import re
from collections import defaultdict
from extractor.fields.base import BaseFieldExtractor
from extractor.utils.constants import known_cities, city_aliases
from extractor.utils.logger import LoggerFactory

class ResumeLocationField(BaseFieldExtractor):
    def __init__(self, text, doc=None, debug=False):
        super().__init__(text, doc, debug)
        self.logger = LoggerFactory(debug=debug).get_logger(__name__)
        self.text = text
        self.doc = doc
        self.lines = [line.strip() for line in text.splitlines() if line.strip()]
        self.text_length = len(text)
        self.all_candidates = []

    def normalize_city(self, city_name):
        city = city_name.lower().strip()
        city = re.sub(r',?\s*(india|up|uttar pradesh|ncr)\s*$', '', city, flags=re.IGNORECASE)
        return city_aliases.get(city, city)

    def scan_block_for_city(self, block, confidence, method, strategy_num):
        block_lower = block.lower()
        block_pos = self.text.find(block)

        match = re.search(r"\(([^)]+)\)", block)
        if match:
            self._check_candidate_and_add(match.group(1), confidence, block, method, block_pos, strategy_num)

        for city in known_cities:
            if city in block_lower:
                self._check_candidate_and_add(city.title(), confidence, block, method, block_pos, strategy_num)

    def _check_candidate_and_add(self, candidate_text, confidence, context_text, method, start_pos, strategy_num):
        tokens = re.sub(r"[^a-zA-Z\s]", " ", candidate_text).split()
        for token in tokens:
            norm = self.normalize_city(token)
            if norm in known_cities:
                self._add_candidate(norm.title(), confidence, start_pos, context_text, method)
                self.logger.debug(f"🔍 S{strategy_num} matched: {norm.title()}")
                return

    def _add_candidate(self, city, confidence, position, context, method):
        base = confidence * 0.40
        context_lower = context.lower()

        temporal = 1.0 if re.search(r'\b(present|current|ongoing|till\s+date)\b', context_lower) else 0.0
        temporal_score = temporal * 0.30

        context_boost = 0.0
        if "currently" in context_lower or "presently" in context_lower:
            context_boost += 0.20
        if re.search(r'\b(working|employed|residing)\b', context_lower):
            context_boost += 0.15
        if any(neg in context_lower for neg in ["education", "university", "college", "born", "birth"]):
            context_boost -= 0.30
        context_score = max(0, context_boost) * 0.20

        rel_pos = position / max(self.text_length, 1)
        pos_score = (1.0 if rel_pos < 0.1 else 0.8 if rel_pos < 0.4 else 0.5) * 0.10

        final_score = base + temporal_score + context_score + pos_score
        if method == "max_conf_current_exp":
            final_score += 0.15

        self.all_candidates.append({
            'city': city,
            'score': final_score,
            'method': method,
            'position': position
        })
        self.logger.debug(f"🧠 Added: {city} (score: {final_score:.3f}, method: {method})")

    def extract(self):
        return self._extract_location()

    def _extract_location(self):
        # Strategy 1–5: Regex-driven patterns
        # These strategies use regular expressions to extract location clues from labeled fields,
        # descriptive phrases, experience blocks, and training/project lines.
        # Each match is scored and added to the candidate pool.
        strategy_patterns = [
            # Strategy 1: Labeled fields like "Location: Noida"
            (r"(?i)\b(location|address|residence)\b\s*[:\-]?\s*([^\n]+)", 0.85, "labeled_field", 1),
            # Strategy 2: Phrase-based patterns like "based in Bangalore"
            (r"(?i)\b(based\s+(?:out\s+of|in)|located\s+in)\s+([A-Z][a-zA-Z\s,]+)", 0.70, "phrase_pattern", 2),
            (r"\b([A-Z][a-zA-Z\s]+)\s+[–\-]\s*\d{6}", 0.70, "phrase_pattern", 2),
            (r"(?i)Sector\s*[-]?\d{1,3}\s*,?\s*([A-Z][a-zA-Z]+)", 0.70, "phrase_pattern", 2),
            # Strategy 3: Experience blocks with city in parentheses and "Present"/"Current"
            (r"([^\n]{0,100}\(([^)]+)\)[^\n]{0,100}?(present|202\d|current))", 0.95, "work_experience", 3),
            # Strategy 5: Training/project lines like "Consultant, Gurgaon"
            (r"(?i)(training|project|consultant).*?,\s*([A-Z][a-zA-Z\s]+)", 0.65, "training_project", 5),
        ]
        for pattern, confidence, label, num in strategy_patterns:
            for match in re.finditer(pattern, self.text):
                candidate = match.group(2) if len(match.groups()) > 1 else match.group(1)
                self._check_candidate_and_add(candidate, confidence, match.group(0), label, match.start(), num)
        # Strategy 6: Location near email or phone
        self.logger.debug("--- Strategy 6: Near contact ---")
        for i, line in enumerate(self.lines):
            if re.search(r"@[a-zA-Z]+\.[a-zA-Z]+|\+?\d{10}", line):
                block = " ".join(self.lines[max(0, i - 5): min(len(self.lines), i + 2)])
                self.scan_block_for_city(block, 0.65, "near_contact", 6)
                break

        # Strategy 7: spaCy NER for geopolitical entities (GPE)
        self.logger.debug("--- Strategy 7: spaCy NER ---")
        if self.doc and hasattr(self.doc, 'ents'):
            for ent in self.doc.ents:
                if ent.label_ == "GPE":
                    self._check_candidate_and_add(ent.text, 0.75, ent.text, "spacy_ner", ent.start_char, 7)

        # Strategy 8: Override with current experience block
        # Scans 2–3 lines around "Present"/"Current" and boosts confidence
        self.logger.debug("--- Strategy 8: Current Experience Block ---")
        for i, line in enumerate(self.lines):
            if re.search(r'\b(present|current|till\s+date)\b', line.lower()):
                block = " ".join(self.lines[max(0, i - 1): min(len(self.lines), i + 3)])
                self.scan_block_for_city(block, 0.99, "max_conf_current_exp", 8)
                break

        # Strategy 8 override: if any high-confidence current experience match exists, use it directly
        preferred = [c for c in self.all_candidates if c['method'] == "max_conf_current_exp"]
        if preferred:
            best = max(preferred, key=lambda c: c['score'])
            location = self.normalize_city(best['city']).title()
            self.logger.debug(f"✅ Strategy 8 override: {location}")
            return location

        # Ensemble voting: group candidates by normalized city and compute weighted scores
        if self.all_candidates:
            grouped = defaultdict(list)
            for c in self.all_candidates:
                grouped[self.normalize_city(c['city'])].append(c['score'])

            scores = {
                city: sum(vals)/len(vals)*0.60 + max(vals)*0.30 + min(len(vals)/4.0, 1.0)*0.10
                for city, vals in grouped.items()
            }

            best_city, best_score = max(scores.items(), key=lambda x: x[1])
            if best_score >= 0.40:
                location = best_city.title()
                self.logger.debug(f"✅ Selected: {location} (score: {best_score:.3f})")
                return location

        # Fallback if no valid candidates found
        self.logger.debug("❌ No location found.")
        return "Not found"
