from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import sqlite3
import pickle
import numpy as np
import os

app = Flask(__name__)
app.secret_key = "career_chatbot_secret_key_2026"
DB_PATH = "career_chatbot.db"

# ─── DATABASE HELPERS ────────────────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            response TEXT NOT NULL,
            career_predicted TEXT,
            timestamp TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ─── LOAD ML MODELS ───────────────────────────────────────────────────────────
def load_models():
    with open("model/rf_model.pkl", "rb") as f:
        rf_model = pickle.load(f)
    with open("model/dt_model.pkl", "rb") as f:
        dt_model = pickle.load(f)
    with open("model/label_encoders.pkl", "rb") as f:
        le_dict = pickle.load(f)
    return rf_model, dt_model, le_dict

rf_model, dt_model, le_dict = load_models()

# ─── CAREER DESCRIPTIONS ─────────────────────────────────────────────────────
CAREER_INFO = {
    "Software Developer": {
        "desc": "Build and maintain software applications and systems.",
        "skills": ["Python", "Java", "Git", "Problem Solving"],
        "salary": "₹4L – ₹20L per annum",
        "growth": "Very High"
    },
    "Data Scientist": {
        "desc": "Analyze complex data to extract insights and build predictive models.",
        "skills": ["Python", "ML", "Statistics", "SQL"],
        "salary": "₹6L – ₹25L per annum",
        "growth": "Very High"
    },
    "UI/UX Designer": {
        "desc": "Design intuitive and visually appealing user interfaces.",
        "skills": ["Figma", "Adobe XD", "Wireframing", "User Research"],
        "salary": "₹4L – ₹18L per annum",
        "growth": "High"
    },
    "Machine Learning Engineer": {
        "desc": "Develop and deploy ML models into production systems.",
        "skills": ["Python", "TensorFlow", "PyTorch", "Cloud"],
        "salary": "₹8L – ₹30L per annum",
        "growth": "Very High"
    },
    "Web Developer": {
        "desc": "Create and maintain websites and web applications.",
        "skills": ["HTML", "CSS", "JavaScript", "React"],
        "salary": "₹3L – ₹15L per annum",
        "growth": "High"
    },
    "Product Manager": {
        "desc": "Lead product strategy, roadmap, and cross-functional teams.",
        "skills": ["Communication", "Strategy", "Analytics", "Leadership"],
        "salary": "₹8L – ₹35L per annum",
        "growth": "High"
    },
    "Data Analyst": {
        "desc": "Interpret data and provide actionable business insights.",
        "skills": ["Excel", "SQL", "Tableau", "Python"],
        "salary": "₹4L – ₹16L per annum",
        "growth": "High"
    },
    "Cybersecurity Analyst": {
        "desc": "Protect systems and networks from digital attacks.",
        "skills": ["Networking", "Ethical Hacking", "Linux", "Firewalls"],
        "salary": "₹5L – ₹22L per annum",
        "growth": "Very High"
    },
}

DEFAULT_CAREER_INFO = {
    "desc": "A rewarding career path aligned with your skills and interests.",
    "skills": ["Domain Knowledge", "Communication", "Problem Solving"],
    "salary": "Varies by industry",
    "growth": "Good"
}

# ─── CHATBOT CONVERSATION FLOW ────────────────────────────────────────────────
CONVERSATION_STEPS = [
    ("greeting", None),
    ("name", "What is your name?"),
    ("technical_skill", "What is your primary technical skill? (e.g., python, java, web, data, design, networking, writing, management, finance, biology, chemistry, physics, math, art, music)"),
    ("communication", "How would you rate your communication skills? (excellent / good / average)"),
    ("preferred_domain", "Which domain interests you most? (technology / analytics / creative / business / science / media)"),
    ("education", "What is your highest education level? (btech / mtech / bsc / msc / mba / bba / ba / ma / mbbs / bdes / bfa / mfa / diploma)"),
    ("predict", None),
]

def safe_encode(le, value, col_name):
    """Encode a value, using closest match if not seen."""
    classes = list(le.classes_)
    value = value.lower().strip()
    if value in classes:
        return le.transform([value])[0]
    # Fallback: try to find a partial match
    for c in classes:
        if value in c or c in value:
            return le.transform([c])[0]
    return 0  # Default to first class

def predict_career(user_data, model_choice="rf"):
    try:
        features = []
        for col in ["technical_skill", "communication", "preferred_domain", "education"]:
            enc = safe_encode(le_dict[col], user_data[col], col)
            features.append(enc)

        features = np.array(features).reshape(1, -1)
        model = rf_model if model_choice == "rf" else dt_model
        pred_encoded = model.predict(features)[0]
        career = le_dict["career"].inverse_transform([pred_encoded])[0]

        # Get top 3 predictions with probabilities
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(features)[0]
            top3_idx = np.argsort(probs)[::-1][:3]
            top3 = [(le_dict["career"].inverse_transform([i])[0], round(probs[i]*100, 1)) for i in top3_idx]
        else:
            top3 = [(career, 100.0)]

        return career, top3
    except Exception as e:
        return "Software Developer", [("Software Developer", 90.0)]

def get_career_info(career):
    return CAREER_INFO.get(career, DEFAULT_CAREER_INFO)

def process_message(user_message, session_data):
    step = session_data.get("step", 0)
    user_inputs = session_data.get("user_inputs", {})
    bot_response = ""
    next_step = step

    if step == 0:
        bot_response = (
            "👋 Hello! I'm your <strong>Career Guidance Chatbot</strong>.<br><br>"
            "I'll help you discover the best career path based on your skills, interests, and background. "
            "This will take just a minute!<br><br>"
            "Let's start — <strong>What is your name?</strong>"
        )
        next_step = 1

    elif step == 1:
        user_inputs["name"] = user_message
        bot_response = (
            f"Nice to meet you, <strong>{user_message}</strong>! 😊<br><br>"
            "💻 <strong>What is your primary technical skill?</strong><br>"
            "<small>Options: python, java, web, data, design, networking, writing, management, finance, biology, chemistry, physics, math, art, music</small>"
        )
        next_step = 2

    elif step == 2:
        user_inputs["technical_skill"] = user_message.lower().strip()
        bot_response = (
            "Great! 🎯<br><br>"
            "🗣️ <strong>How would you rate your communication skills?</strong><br>"
            "<small>Options: excellent / good / average</small>"
        )
        next_step = 3

    elif step == 3:
        val = user_message.lower().strip()
        if val not in ["excellent", "good", "average"]:
            val = "good"
        user_inputs["communication"] = val
        bot_response = (
            "Noted! 📋<br><br>"
            "🌐 <strong>Which domain interests you the most?</strong><br>"
            "<small>Options: technology / analytics / creative / business / science / media</small>"
        )
        next_step = 4

    elif step == 4:
        user_inputs["preferred_domain"] = user_message.lower().strip()
        bot_response = (
            "Excellent choice! 🎓<br><br>"
            "📚 <strong>What is your highest education level?</strong><br>"
            "<small>Options: btech / mtech / bsc / msc / mba / bba / ba / ma / mbbs / bdes / bfa / mfa / diploma</small>"
        )
        next_step = 5

    elif step == 5:
        user_inputs["education"] = user_message.lower().strip()
        career, top3 = predict_career(user_inputs)
        info = get_career_info(career)
        session_data["predicted_career"] = career

        skills_html = "".join(f'<span class="skill-tag">{s}</span>' for s in info["skills"])
        top3_html = "".join(
            f'<div class="top3-item"><span class="career-name">{c}</span> <span class="prob">{p}%</span></div>'
            for c, p in top3
        )

        bot_response = (
            f"🎉 Analysis complete, <strong>{user_inputs.get('name', 'there')}</strong>!<br><br>"
            f"<div class='result-card'>"
            f"<div class='result-title'>🏆 Best Career Match</div>"
            f"<div class='career-result'>{career}</div>"
            f"<div class='result-desc'>{info['desc']}</div>"
            f"<div class='result-meta'>"
            f"<div>💰 <strong>Salary:</strong> {info['salary']}</div>"
            f"<div>📈 <strong>Growth:</strong> {info['growth']}</div>"
            f"</div>"
            f"<div class='skills-section'><strong>🛠 Key Skills to Develop:</strong><br>{skills_html}</div>"
            f"<div class='top3-section'><strong>📊 Top 3 Predictions:</strong>{top3_html}</div>"
            f"</div><br>"
            "Would you like to <strong>explore another career</strong> or do you have any questions? "
            "Type <em>'restart'</em> to start over or ask me anything!"
        )
        next_step = 6

        # Save to DB
        try:
            conn = get_db()
            conn.execute(
                "INSERT INTO chat_history (message, response, career_predicted) VALUES (?, ?, ?)",
                (str(user_inputs), career, career)
            )
            conn.commit()
            conn.close()
        except:
            pass

    elif step == 6:
        if "restart" in user_message.lower():
            session_data["step"] = 0
            session_data["user_inputs"] = {}
            return process_message("start", session_data)
        else:
            faq_responses = {
                "salary": f"The typical salary for your predicted career varies by experience and location. Entry level starts around ₹3–6L, and senior roles can reach ₹20–40L+ per annum.",
                "skills": "Focus on building technical skills through online platforms like Coursera, Udemy, and also work on projects for your portfolio.",
                "scope": "The tech and data fields are growing rapidly. Stay updated with industry trends and continuously upskill.",
                "courses": "Platforms like Coursera, edX, NPTEL, and Udemy offer great courses. For certifications, look at Google, AWS, and Microsoft certs.",
            }
            resp = "I'd be happy to help! Here are some tips: 💡<br><br>"
            answered = False
            for key, answer in faq_responses.items():
                if key in user_message.lower():
                    resp = f"💡 {answer}<br><br>Type <em>'restart'</em> to explore another career path!"
                    answered = True
                    break
            if not answered:
                resp = (
                    "That's a great question! 😊 I recommend:<br>"
                    "• Researching your predicted career field online<br>"
                    "• Connecting with professionals on LinkedIn<br>"
                    "• Building projects to add to your portfolio<br><br>"
                    "Type <em>'restart'</em> to get a new career recommendation!"
                )
        bot_response = resp
        next_step = 6

    session_data["step"] = next_step
    session_data["user_inputs"] = user_inputs
    return bot_response, session_data

# ─── ROUTES ───────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    session.clear()
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if "chat_session" not in session:
        session["chat_session"] = {"step": 0, "user_inputs": {}}

    session_data = session["chat_session"]
    response, updated_session = process_message(user_message, session_data)
    session["chat_session"] = updated_session
    session.modified = True

    return jsonify({"response": response})

@app.route("/reset", methods=["POST"])
def reset():
    session.clear()
    return jsonify({"status": "reset"})

@app.route("/history")
def history():
    conn = get_db()
    chats = conn.execute(
        "SELECT * FROM chat_history ORDER BY timestamp DESC LIMIT 20"
    ).fetchall()
    conn.close()
    return render_template("history.html", chats=chats)

# ─── RUN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)
