# microproject-NLP
Career Guidance Chatbot

## 📁 Project Structure

```
career_chatbot/
├── app.py                  # Flask backend + chatbot logic
├── requirements.txt
├── model/
│   ├── train_model.py      # Train & save ML models
│   ├── rf_model.pkl        # Random Forest model (generated)
│   ├── dt_model.pkl        # Decision Tree model (generated)
│   └── label_encoders.pkl  # Encoders (generated)
├── templates/
│   ├── index.html          # Main chat UI
│   └── history.html        # Chat history page
└── static/
    ├── css/style.css
    └── js/chat.js
```

---

## ⚙️ Setup & Run

### Step 1 – Clone / Download the project
```bash
cd career_chatbot
```

### Step 2 – Create a virtual environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### Step 3 – Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 – Train the ML model
```bash
cd model
python train_model.py
cd ..
```
This generates `rf_model.pkl`, `dt_model.pkl`, and `label_encoders.pkl`.

### Step 5 – Run the Flask app
```bash
python app.py
```

### Step 6 – Open in browser
```
http://127.0.0.1:5000
```

---

## 🧠 How the ML Model Works

| Feature | Options |
|---|---|
| Technical Skill | python, java, web, data, design, networking, writing, management, finance, biology, chemistry, physics, math, art, music |
| Communication | excellent / good / average |
| Preferred Domain | technology / analytics / creative / business / science / media |
| Education | btech / mtech / bsc / msc / mba / bba / ba / ma / mbbs / bdes / bfa / mfa / diploma |

The model uses **Label Encoding** on all categorical inputs, then runs a **Random Forest Classifier** (100 estimators) to predict the best career match. Top-3 predictions with confidence % are also shown.

---

## 🌐 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS (custom) |
| Backend | Python, Flask |
| ML Models | scikit-learn (Random Forest + Decision Tree) |
| Database | SQLite (via Flask-SQLAlchemy) |

---

## 📦 Key Features

- 🤖 Interactive step-by-step chatbot conversation
- 🎯 ML-based career prediction with confidence scores
- 🏆 Top 3 career recommendations shown
- 💡 Career info: description, salary range, growth, skills
- 📜 Chat history saved in SQLite
- 🔄 Quick-option buttons for easy input
- 📱 Responsive design

