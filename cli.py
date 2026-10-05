"""
Terminal CLI Interface for Crescent Institute FAQ Chatbot.
Run with: python cli.py
"""

import os
import sys
import re

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from faq_engine import FAQEngine

# Terminal color codes
RED = "\033[91m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"

def clean_html(text: str) -> str:
    """Removes HTML tags and normalizes symbols for safe console display."""
    text = text.replace("₹", "Rs. ")
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"<li>", " * ", text)
    text = re.sub(r"</li>", "\n", text)
    text = re.sub(r"<ol>", "\n", text)
    text = re.sub(r"</ol>", "", text)
    text = re.sub(r"<ul>", "\n", text)
    text = re.sub(r"</ul>", "", text)
    text = re.sub(r"</?[bi]>", "", text)
    text = re.sub(r"<a\s+[^>]*>(.*?)</a>", r"\1", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    return text.strip()

def main():
    faq_file = os.path.join(os.path.dirname(__file__), "data", "faqs.json")
    engine = FAQEngine(faq_file)

    print(f"\n{BOLD}{RED}==================================================================={RESET}")
    print(f"{BOLD}{YELLOW}   CRESCENT VIRTUAL ASSISTANT - B.S. ABDUR RAHMAN CRESCENT INST.   {RESET}")
    print(f"{BOLD}{RED}==================================================================={RESET}")
    print("Welcome! Ask me anything regarding CIEAT 2026, B.Tech/MBA admissions,")
    print("scholarships, fees, KBA hostels, placements, bus routes, or contacts.")
    print(f"Type {YELLOW}'exit'{RESET} or {YELLOW}'quit'{RESET} to end the conversation.\n")
    print(f"{MAGENTA}Suggested Questions:{RESET}")
    for q in engine.get_popular_questions(4):
        print(f"  * {q}")
    print("-" * 67)

    while True:
        try:
            user_input = input(f"\n{BOLD}{CYAN}You: {RESET}").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit", "q"):
                print(f"\n{GREEN}Crescent Assistant:{RESET} Thank you for connecting with Crescent! All the best. Vanakkam! Goodbye!\n")
                break

            response = engine.query(user_input)
            conf = response.get("confidence", 0.0)
            category = response.get("category")

            print(f"\n{BOLD}{RED}Crescent Assistant:{RESET}")
            if category:
                print(f"{YELLOW}[Category: {category} | Verified with crescent.education | Match: {int(conf * 100)}%]{RESET}")

            answer = clean_html(response.get("answer", ""))
            print(answer)

            quick_links = response.get("quick_links", [])
            if quick_links:
                print(f"\n{CYAN}Official Links:{RESET}")
                for link in quick_links:
                    print(f"  -> {link.get('label')}: {link.get('url')}")

            suggestions = response.get("suggestions", [])
            if suggestions:
                print(f"\n{MAGENTA}Related questions you might ask:{RESET}")
                for s in suggestions[:3]:
                    print(f"  -> {s}")

        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{GREEN}Crescent Assistant:{RESET} Goodbye!\n")
            break

if __name__ == "__main__":
    main()
