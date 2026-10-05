# 🎓 CrescentAssist - B.S. Abdur Rahman Crescent Institute FAQ Chatbot

An intelligent, full-stack Virtual Assistant and Query Helpdesk Portal designed specifically for **B.S. Abdur Rahman Crescent Institute of Science and Technology** ([crescent.education](https://crescent.education/)), Vandalur, Chennai.

Developed by **[@fakhrulmohamed](https://github.com/fakhrulmohamed)**.

![CrescentAssist Banner](https://img.shields.io/badge/NAAC-A%2B%20Accredited-red?style=flat-square)
![University](https://img.shields.io/badge/Crescent-crescent.education-blue?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![Framework](https://img.shields.io/badge/Flask-3.1-green?style=flat-square&logo=flask)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)

---

## 🏛️ About Crescent Institute of Science and Technology

B.S. Abdur Rahman Crescent Institute of Science and Technology (formerly Crescent Engineering College) is a premier 40+ year-old Deemed-to-be-University located on GST Road, Vandalur, Chennai, accredited with **A+ Grade by NAAC** and ranked top in innovation (ARIIA/NIRF).

This chatbot is designed to provide prospective students, admitted students, and parents with 24/7 instant answers verified directly against official college announcements.

---

## ✨ Features

- **🎨 Official College Branding:**
  - Designed around Crescent's official visual identity: **Crescent Crimson Red (`#D90B1C`)**, **Midnight Navy Blue (`#1C315E`)**, and **Collegiate Gold (`#F7BC31`)**.
  - Official high-resolution Crescent Institute insignia in header, avatars, and announcement banner.
- **📚 College Knowledge Base (`data/faqs.json`):**
  - **Admissions & CIEAT 2026:** Online proctored Crescent Institute Engineering Admission Test (CIEAT), JEE Main/SAT exemptions, 12th PCM 50% eligibility criteria, and step-by-step portal application.
  - **Academic Schools:** Crescent School of Business (CSB), Crescent School of Architecture (CSA), Crescent School of Law (CSL), Crescent School of Pharmacy (CSP), School of Computer Science & Applications, School of Life Sciences, and Ph.D.
  - **Tuition & Scholarships:** Merit-based tuition tiers, installment payments, Founder's Merit Scholarship, sports scholarships, and the *"India in a Classroom"* scheme.
  - **Placements & Career (CGPC):** 88%+ placement record, super-dream packages up to ₹40 LPA, average packages ₹4.5–6.5 LPA, and top recruiters (Amazon, Zoho, Microsoft, TCS, Cognizant, Infosys, Wipro, L&T, IBM).
  - **KBA Hostels & Residential Life:** Separate KBA Men's & Girls' hostel blocks, AC/Non-AC room options, Halal multi-cuisine mess food, 8:30 PM/9:00 PM curfew, and biometric parent outpass approval.
  - **Campus Facilities & CIIC:** Crescent Innovation and Incubation Council (100+ funded startups), Central Library (90,000+ volumes, IEEE/DELNET), 50+ luxury bus routes across Chennai, 24/7 Health Care Centre, and campus mosque.
  - **Emergency & Helpdesk:** Admissions hotlines (`+91 95432 77888` / `+91 94990 01725`), email (`admissions@crescent.education`), and 24/7 Anti-Ragging helpline.
- **💻 Dual-Mode Interactive Web Portal:**
  - **Ask Crescent AI Tab:** Conversational interface with bubble timestamps, typing indicators, suggested follow-ups, and clickable official links.
  - **Browse FAQs Directory Tab:** Instant searchable knowledge base accordion with real-time text filter and category pills.
  - **Voice & Accessibility:** Speech-to-Text microphone recording and Text-to-Speech audio reader.
  - **Dark / Light Theme:** Custom toggle persisted across sessions.
- **🖥️ Terminal CLI Mode (`cli.py`):**
  - Lightweight console chatbot for instant testing without browser overhead.
- **⚡ RESTful API:**
  - Clean Flask endpoints (`/api/chat`, `/api/faqs`, `/api/categories`, `/api/feedback`) ready for integration into mobile apps or university portals.

---

## 📁 Project Structure

```text
college-faq-chatbot/
├── data/
│   └── faqs.json            # Crescent University FAQ dataset
├── templates/
│   └── index.html           # Crescent-themed responsive HTML5 UI
├── static/
│   ├── style.css            # Crescent Crimson & Navy styling
│   ├── app.js               # Frontend chat, voice, and directory logic
│   └── crescent-logo-white.png # Official Crescent University logo
├── app.py                   # Flask server with REST API endpoints
├── cli.py                   # Terminal CLI interface
├── faq_engine.py            # Crescent NLP matching engine
├── test_app.py              # Automated test suite (all 7 tests pass)
├── requirements.txt         # Minimal dependency list (Flask)
├── .gitignore               # Git ignore rules
└── README.md                # Documentation
```

---

## 🚀 Quickstart Guide

### 1. Requirements
Ensure Python 3.10+ and Git are installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Web Application
```bash
python app.py
```
Open your browser and navigate to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🖥️ Running in Terminal (CLI Mode)

To interact with the chatbot directly in PowerShell or CMD:
```bash
python cli.py
```

---

## 🧪 Running Automated Tests

Run the test suite to verify all endpoints and the matching engine:
```bash
python test_app.py
```

---

## 🌐 Official University References
* **Website:** [https://crescent.education/](https://crescent.education/)
* **Admissions Portal:** [https://crescent.education/engineering-admissions-2026/](https://crescent.education/engineering-admissions-2026/)
* **Placements:** [https://crescent.education/placement/](https://crescent.education/placement/)
* **Campus Address:** GST Road, Vandalur, Chennai – 600048, Tamil Nadu, India.
