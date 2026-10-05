"""
Crescent University FAQ Chatbot - NLP Matching Engine
Tailored specifically for B.S. Abdur Rahman Crescent Institute of Science & Technology (crescent.education).
"""

import json
import re
import os
from difflib import SequenceMatcher
from typing import List, Dict, Any, Optional, Tuple

STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "her", "here", "hers", "herself", "him",
    "himself", "his", "how", "i", "if", "in", "into", "is", "isn't", "it", "its",
    "itself", "just", "me", "more", "most", "my", "myself", "no", "nor", "not",
    "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours",
    "ourselves", "out", "over", "own", "same", "she", "should", "shouldn't", "so",
    "some", "such", "than", "that", "the", "their", "theirs", "them", "themselves",
    "then", "there", "these", "they", "this", "those", "through", "to", "too",
    "under", "until", "up", "very", "was", "wasn't", "we", "were", "weren't", "what",
    "when", "where", "which", "while", "who", "whom", "why", "with", "would",
    "wouldn't", "you", "your", "yours", "yourself", "yourselves", "tell", "please",
    "want", "know", "give", "information", "detail", "details", "college", "university",
    "institute", "crescent"
}

SYNONYM_MAP = {
    "fee": ["fees", "tuition", "cost", "charge", "charges", "price", "amount", "expense", "expenses"],
    "cieat": ["entrance", "exam", "test", "jee", "admission test", "exam date", "syllabus"],
    "scholarship": ["scholarships", "concession", "waiver", "discount", "financial aid", "grant", "founder", "merit"],
    "hostel": ["hostels", "dorm", "dorms", "kba", "room", "rooms", "accommodation", "stay", "residence", "mess"],
    "mess": ["canteen", "food", "cafeteria", "dining", "meal", "meals", "halal"],
    "placement": ["placements", "job", "jobs", "hiring", "recruit", "recruiter", "recruiters", "package", "salary", "lpa", "career", "cgpc"],
    "internship": ["internships", "intern", "training", "summer training"],
    "admission": ["admissions", "apply", "application", "enroll", "enrollment", "register", "registration", "intake", "seat", "seats", "eligibility"],
    "eligibility": ["criteria", "qualify", "qualification", "requirement", "requirements", "minimum", "percent", "percentage", "marks", "pcm"],
    "exam": ["exams", "examination", "examinations", "midterm", "finals", "backlog", "backlogs", "grade", "grading", "cgpa"],
    "contact": ["phone", "call", "number", "email", "address", "helpline", "reach", "location", "vandalur", "where is"],
    "library": ["book", "books", "reading room", "journal", "journals", "ieee"],
    "curfew": ["timing", "timings", "outpass", "in-time", "night out", "gate"],
    "transport": ["bus", "transportation", "commute", "pickup", "travel", "route", "routes"],
    "ciic": ["incubation", "incubator", "startup", "startups", "entrepreneurship", "funding"],
    "doctor": ["medical", "clinic", "hospital", "health", "medicine", "emergency", "ambulance", "dispensary"],
    "ragging": ["anti-ragging", "harass", "harassment", "bully", "bullying"],
    "ranking": ["naac", "nirf", "accreditation", "grade", "recognized", "ugc", "aicte", "nba"]
}

# Reverse canonical lookup
CANONICAL_LOOKUP = {}
for canonical, variants in SYNONYM_MAP.items():
    CANONICAL_LOOKUP[canonical] = canonical
    for variant in variants:
        CANONICAL_LOOKUP[variant] = canonical


class FAQEngine:
    def __init__(self, faqs_path: str):
        self.faqs_path = faqs_path
        self.faqs: List[Dict[str, Any]] = []
        self.load_faqs()

    def load_faqs(self):
        """Loads and indexes the FAQ knowledge base."""
        if not os.path.exists(self.faqs_path):
            raise FileNotFoundError(f"FAQ file not found: {self.faqs_path}")
        with open(self.faqs_path, "r", encoding="utf-8") as f:
            self.faqs = json.load(f)

    @staticmethod
    def clean_text(text: str) -> str:
        """Lowercases and cleans input text."""
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def tokenize(text: str) -> List[str]:
        """Extracts normalized tokens excluding stopwords."""
        cleaned = FAQEngine.clean_text(text)
        return [w for w in cleaned.split() if w and w not in STOPWORDS]

    @staticmethod
    def expand_tokens(tokens: List[str]) -> set:
        """Expands tokens with domain synonyms."""
        expanded = set(tokens)
        for token in tokens:
            if token in CANONICAL_LOOKUP:
                canonical = CANONICAL_LOOKUP[token]
                expanded.add(canonical)
                if canonical in SYNONYM_MAP:
                    expanded.update(SYNONYM_MAP[canonical])
        return expanded

    def check_chit_chat(self, raw_query: str) -> Optional[Dict[str, Any]]:
        """Handles greetings, praise, and identity for Crescent."""
        cleaned = self.clean_text(raw_query)

        greetings = {"hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening", "vanakkam", "assalamu alaikum"}
        if cleaned in greetings or any(cleaned.startswith(g + " ") for g in greetings):
            return {
                "matched": True,
                "confidence": 1.0,
                "type": "greeting",
                "answer": (
                    "Vanakkam! 👋 Welcome to <b>Crescent Virtual Assistant</b>.<br>"
                    "I am the official AI guide for <b>B.S. Abdur Rahman Crescent Institute of Science & Technology</b> (Vandalur, Chennai).<br><br>"
                    "Ask me about <b>CIEAT entrance exam, B.Tech/MBA admissions, scholarships, tuition fees, KBA hostels, placements, bus routes, or campus contacts</b>!"
                ),
                "suggestions": [
                    "How do I apply for admission at Crescent University?",
                    "What is CIEAT and is it mandatory for B.Tech?",
                    "What is the fee structure for B.Tech courses?",
                    "What are the placement statistics and top recruiting companies?"
                ]
            }

        thanks = {"thanks", "thank you", "thank you so much", "thx", "appreciate it", "great thanks"}
        if cleaned in thanks or any(cleaned.startswith(t + " ") for t in thanks):
            return {
                "matched": True,
                "confidence": 1.0,
                "type": "gratitude",
                "answer": (
                    "You're very welcome! 😊 Always pleased to assist. If you need any further guidance about Crescent University "
                    "or have admissions questions, feel free to ask or reach our helpdesk at <b>+91 95432 77888</b>."
                ),
                "suggestions": [
                    "What hostel facilities and room types are available?",
                    "What scholarships and fee waivers are available at Crescent?",
                    "How do I contact Crescent Admissions Office?"
                ]
            }

        identity = {"who are you", "what is your name", "what can you do", "help", "about you", "tell me about crescent"}
        if cleaned in identity or any(i in cleaned for i in identity):
            return {
                "matched": True,
                "confidence": 1.0,
                "type": "identity",
                "answer": (
                    "I am the official <b>Crescent AI Helpdesk Assistant</b> for B.S. Abdur Rahman Crescent Institute of Science and Technology. 🎓<br><br>"
                    "I provide instantaneous answers directly verified with <a href='https://crescent.education/' target='_blank'><b>crescent.education</b></a> "
                    "covering academic programmes, CIEAT exam registration, scholarships, placement statistics, KBA hostel charges, and campus amenities."
                ),
                "suggestions": [
                    "What is CIEAT and is it mandatory for B.Tech admission?",
                    "What are the eligibility criteria for B.Tech courses at Crescent?",
                    "What is the NAAC accreditation and NIRF ranking?",
                    "What are the hostel and mess charges at Crescent?"
                ]
            }

        return None

    def calculate_score(self, user_text: str, user_tokens: List[str], user_expanded: set, faq: Dict[str, Any]) -> float:
        """Calculates multi-factor similarity score between query and FAQ entry."""
        # 1. Fuzzy string similarity
        question_sim = SequenceMatcher(None, user_text, self.clean_text(faq["question"])).ratio()
        
        pattern_sims = [
            SequenceMatcher(None, user_text, self.clean_text(pattern)).ratio()
            for pattern in faq.get("patterns", [])
        ]
        best_pattern_sim = max(pattern_sims) if pattern_sims else 0.0

        # 2. Token overlap
        faq_tokens = set(self.tokenize(faq["question"]))
        faq_keywords = set(faq.get("keywords", []))
        all_faq_terms = faq_tokens | faq_keywords

        token_overlap = len(set(user_tokens) & all_faq_terms)
        token_jaccard = (
            token_overlap / len(set(user_tokens) | all_faq_terms)
            if (set(user_tokens) | all_faq_terms) else 0.0
        )

        synonym_overlap = len(user_expanded & all_faq_terms)
        synonym_score = min(1.0, synonym_overlap / max(1, len(all_faq_terms)))

        # Specific keyword hits
        keyword_hits = sum(1 for kw in faq_keywords if kw in user_text)
        keyword_boost = min(0.35, keyword_hits * 0.12)

        # Weighted combination
        total_score = (
            (best_pattern_sim * 0.35) +
            (question_sim * 0.25) +
            (token_jaccard * 0.20) +
            (synonym_score * 0.10) +
            keyword_boost
        )

        # Exact token match bonus
        if user_tokens and all(tok in all_faq_terms or tok in user_expanded for tok in user_tokens):
            total_score += 0.22

        return min(1.0, total_score)

    def query(self, user_query: str) -> Dict[str, Any]:
        """Main entry point to query the Crescent FAQ engine."""
        user_query = user_query.strip()
        if not user_query:
            return {
                "matched": False,
                "confidence": 0.0,
                "answer": "Please enter a question or select a query below.",
                "suggestions": self.get_popular_questions(4)
            }

        chit_chat_resp = self.check_chit_chat(user_query)
        if chit_chat_resp:
            return chit_chat_resp

        cleaned_user = self.clean_text(user_query)
        user_tokens = self.tokenize(cleaned_user)
        user_expanded = self.expand_tokens(user_tokens)

        scored_faqs: List[Tuple[float, Dict[str, Any]]] = []
        for faq in self.faqs:
            score = self.calculate_score(cleaned_user, user_tokens, user_expanded, faq)
            scored_faqs.append((score, faq))

        scored_faqs.sort(key=lambda x: x[0], reverse=True)
        best_score, best_faq = scored_faqs[0]

        suggestions = [
            f[1]["question"]
            for f in scored_faqs[1:4]
            if f[0] > 0.15 and f[1]["id"] != best_faq["id"]
        ]
        if len(suggestions) < 3:
            same_cat = [f["question"] for f in self.faqs if f["category"] == best_faq["category"] and f["id"] != best_faq["id"]]
            for q in same_cat:
                if q not in suggestions:
                    suggestions.append(q)
                if len(suggestions) >= 3:
                    break

        if best_score >= 0.48:
            return {
                "matched": True,
                "confidence": round(best_score, 2),
                "status": "high_confidence",
                "faq_id": best_faq["id"],
                "category": best_faq["category"],
                "question": best_faq["question"],
                "answer": best_faq["answer"],
                "quick_links": best_faq.get("quick_links", []),
                "suggestions": suggestions
            }
        elif best_score >= 0.30:
            return {
                "matched": True,
                "confidence": round(best_score, 2),
                "status": "medium_confidence",
                "faq_id": best_faq["id"],
                "category": best_faq["category"],
                "question": best_faq["question"],
                "answer": (
                    f"<i>Here is the closest verified answer from Crescent Education portal:</i><br><br>"
                    f"<b>{best_faq['question']}</b><br>{best_faq['answer']}"
                ),
                "quick_links": best_faq.get("quick_links", []),
                "suggestions": suggestions
            }
        else:
            return {
                "matched": False,
                "confidence": round(best_score, 2),
                "status": "fallback",
                "answer": (
                    "I could not locate an exact match in the Crescent FAQ database for that query. 🧐<br><br>"
                    "You can:<br>"
                    "1. Search using keywords like <b>CIEAT, fees, B.Tech, KBA hostel, placement, bus</b>.<br>"
                    "2. Browse all questions in the <b>Browse FAQs</b> tab.<br>"
                    "3. Contact Crescent Admissions directly at <b>+91 95432 77888</b> or <b>admissions@crescent.education</b>."
                ),
                "suggestions": self.get_popular_questions(4)
            }

    def get_categories(self) -> List[str]:
        cats = []
        for f in self.faqs:
            c = f.get("category", "General")
            if c not in cats:
                cats.append(c)
        return cats

    def get_faqs_by_category(self, category: Optional[str] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
        results = self.faqs
        if category and category.lower() != "all":
            results = [f for f in results if f["category"].lower() == category.lower()]
        if search:
            s = search.lower()
            results = [
                f for f in results
                if s in f["question"].lower() or s in f["answer"].lower() or any(s in kw for kw in f.get("keywords", []))
            ]
        return results

    def get_popular_questions(self, count: int = 4) -> List[str]:
        defaults = [
            "How do I apply for admission at Crescent University?",
            "What is CIEAT and is it mandatory for B.Tech admission?",
            "What is the fee structure for B.Tech and other courses at Crescent?",
            "What are the placement statistics and top recruiting companies at Crescent?",
            "What hostel facilities and room types are available at Crescent?"
        ]
        return defaults[:count]
