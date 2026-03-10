import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import pickle
import os

# ─── SAMPLE TRAINING DATA ───────────────────────────────────────────────────
# Columns: technical_skill, communication, preferred_domain, education, career
data = {
    "technical_skill": [
        "python", "java", "web", "data", "design", "python", "java", "web",
        "data", "design", "python", "networking", "networking", "writing",
        "writing", "management", "management", "finance", "finance", "biology",
        "biology", "chemistry", "physics", "math", "math", "art", "art",
        "music", "music", "python", "data", "web", "design", "java",
        "networking", "writing", "management", "finance", "biology", "chemistry"
    ],
    "communication": [
        "average", "good", "excellent", "average", "good", "excellent",
        "average", "good", "excellent", "average", "good", "excellent",
        "average", "excellent", "good", "excellent", "good", "excellent",
        "good", "excellent", "average", "average", "average", "good",
        "excellent", "good", "excellent", "good", "excellent", "good",
        "excellent", "average", "average", "excellent", "good", "excellent",
        "average", "average", "good", "excellent"
    ],
    "preferred_domain": [
        "technology", "technology", "technology", "technology", "creative",
        "technology", "technology", "technology", "analytics", "creative",
        "analytics", "technology", "technology", "media", "media", "business",
        "business", "business", "business", "science", "science", "science",
        "science", "analytics", "technology", "creative", "creative", "creative",
        "creative", "analytics", "analytics", "technology", "creative",
        "technology", "technology", "media", "business", "business", "science",
        "science"
    ],
    "education": [
        "btech", "btech", "bsc", "btech", "bdes", "mtech", "mtech", "bsc",
        "mtech", "bdes", "mtech", "btech", "diploma", "ba", "ma", "mba",
        "bba", "mba", "bba", "mbbs", "bsc", "bsc", "bsc", "msc", "mtech",
        "bfa", "mfa", "diploma", "bfa", "btech", "msc", "bsc", "bdes",
        "mtech", "diploma", "ba", "bba", "mba", "bsc", "msc"
    ],
    "career": [
        "Software Developer", "Software Engineer", "Web Developer",
        "Data Analyst", "UI/UX Designer", "Machine Learning Engineer",
        "Backend Engineer", "Full Stack Developer", "Data Scientist",
        "Graphic Designer", "Data Engineer", "Network Engineer",
        "System Administrator", "Content Writer", "Journalist",
        "Product Manager", "Business Analyst", "Financial Analyst",
        "Investment Banker", "Doctor", "Biologist", "Chemist",
        "Physicist", "Statistician", "Research Scientist",
        "Illustrator", "Art Director", "Music Producer",
        "Sound Engineer", "AI/ML Researcher", "Business Intelligence Analyst",
        "Frontend Developer", "Motion Graphics Designer",
        "DevOps Engineer", "Cybersecurity Analyst", "Technical Writer",
        "Operations Manager", "Risk Analyst", "Pharmacist", "Lab Scientist"
    ]
}

df = pd.DataFrame(data)

# ─── ENCODE CATEGORICAL FEATURES ────────────────────────────────────────────
le_dict = {}
feature_cols = ["technical_skill", "communication", "preferred_domain", "education"]

for col in feature_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    le_dict[col] = le

le_target = LabelEncoder()
df["career"] = le_target.fit_transform(df["career"])
le_dict["career"] = le_target

X = df[feature_cols]
y = df["career"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ─── TRAIN RANDOM FOREST ─────────────────────────────────────────────────────
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_acc = accuracy_score(y_test, rf_model.predict(X_test))
print(f"Random Forest Accuracy: {rf_acc:.2f}")

dt_model = DecisionTreeClassifier(random_state=42)
dt_model.fit(X_train, y_train)
dt_acc = accuracy_score(y_test, dt_model.predict(X_test))
print(f"Decision Tree Accuracy: {dt_acc:.2f}")

# ─── SAVE MODELS & ENCODERS ──────────────────────────────────────────────────
os.makedirs("model", exist_ok=True)
with open("model/rf_model.pkl", "wb") as f:
    pickle.dump(rf_model, f)
with open("model/dt_model.pkl", "wb") as f:
    pickle.dump(dt_model, f)
with open("model/label_encoders.pkl", "wb") as f:
    pickle.dump(le_dict, f)

print("✅ Models saved successfully!")
