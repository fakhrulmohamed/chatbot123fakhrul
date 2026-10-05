"""
Flask Web Application for College FAQ Chatbot.
"""

import os
from flask import Flask, render_template, request, jsonify
from faq_engine import FAQEngine

app = Flask(__name__)

# Initialize FAQ Engine
FAQ_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "faqs.json")
engine = FAQEngine(FAQ_DATA_PATH)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()
    
    if not message:
        return jsonify({
            "error": "Empty message",
            "answer": "Please ask a question.",
            "suggestions": engine.get_popular_questions(3)
        }), 400

    response = engine.query(message)
    return jsonify(response)

@app.route("/api/categories", methods=["GET"])
def get_categories():
    categories = engine.get_categories()
    return jsonify({"categories": categories})

@app.route("/api/faqs", methods=["GET"])
def get_faqs():
    category = request.args.get("category")
    search = request.args.get("search")
    results = engine.get_faqs_by_category(category=category, search=search)
    return jsonify({"faqs": results, "total": len(results)})

@app.route("/api/popular", methods=["GET"])
def get_popular():
    return jsonify({"questions": engine.get_popular_questions(5)})

@app.route("/api/feedback", methods=["POST"])
def submit_feedback():
    data = request.get_json(silent=True) or {}
    faq_id = data.get("faq_id")
    helpful = data.get("helpful")
    # In a production app, this can be logged to a database or analytics store
    print(f"[Feedback] FAQ {faq_id}: {'Helpful' if helpful else 'Not Helpful'}")
    return jsonify({"status": "success", "message": "Feedback recorded. Thank you!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting College FAQ Chatbot on http://127.0.0.1:{port}")
    app.run(host="127.0.0.1", port=port, debug=True)
