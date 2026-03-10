import pandas as pd
import numpy as np
import random
import os

# Mapping of careers to typical profiles
career_profiles = {
    "Software Developer": {"skill": ["python", "java", "c++", "javascript", "web"], "domain": ["technology"], "comm": ["average", "good"], "edu": ["btech", "bsc", "mtech", "bca", "mca"]},
    "Data Scientist": {"skill": ["python", "r", "data", "math", "sql"], "domain": ["analytics", "technology", "research"], "comm": ["good", "excellent"], "edu": ["btech", "mtech", "bsc", "msc", "phd"]},
    "Network Engineer": {"skill": ["networking", "linux", "security", "hardware"], "domain": ["technology", "infrastructure"], "comm": ["average", "good"], "edu": ["btech", "diploma", "bsc"]},
    "UI/UX Designer": {"skill": ["design", "figma", "css", "html"], "domain": ["creative", "technology"], "comm": ["good", "excellent"], "edu": ["bdes", "bfa", "ba", "bsc"]},
    "Content Writer": {"skill": ["writing", "seo", "editing"], "domain": ["media", "marketing"], "comm": ["excellent", "good"], "edu": ["ba", "ma", "bba"]},
    "Product Manager": {"skill": ["management", "agile", "strategy"], "domain": ["business", "technology"], "comm": ["excellent"], "edu": ["mba", "btech", "bba"]},
    "Financial Analyst": {"skill": ["finance", "excel", "math", "accounting"], "domain": ["business", "finance"], "comm": ["good", "excellent"], "edu": ["bba", "mba", "bcom", "mcom"]},
    "Biologist": {"skill": ["biology", "research", "lab"], "domain": ["science", "research"], "comm": ["average", "good"], "edu": ["bsc", "msc", "phd", "mbbs"]},
    "Doctor": {"skill": ["biology", "medicine", "diagnosis"], "domain": ["healthcare", "science"], "comm": ["excellent", "good"], "edu": ["mbbs", "md"]},
    "Graphic Designer": {"skill": ["design", "illustrator", "photoshop", "art"], "domain": ["creative", "media"], "comm": ["average", "good"], "edu": ["bfa", "bdes", "diploma"]},
    "Cybersecurity Analyst": {"skill": ["security", "networking", "python", "linux"], "domain": ["technology", "security"], "comm": ["good", "excellent"], "edu": ["btech", "mtech", "bsc"]},
    "Business Analyst": {"skill": ["management", "sql", "excel", "data"], "domain": ["business", "analytics"], "comm": ["excellent", "good"], "edu": ["bba", "mba", "btech"]},
    "Backend Engineer": {"skill": ["java", "python", "node", "sql", "database"], "domain": ["technology"], "comm": ["average", "good"], "edu": ["btech", "mtech", "mca", "bsc"]},
    "AI/ML Engineer": {"skill": ["python", "math", "data", "deep learning"], "domain": ["technology", "analytics"], "comm": ["good", "excellent"], "edu": ["btech", "mtech", "msc"]},
    "Journalist": {"skill": ["writing", "investigation", "interviewing"], "domain": ["media", "news"], "comm": ["excellent"], "edu": ["ba", "ma", "diploma"]},
    "Marketing Manager": {"skill": ["marketing", "management", "seo", "writing"], "domain": ["business", "marketing"], "comm": ["excellent", "good"], "edu": ["mba", "bba"]},
    "HR Manager": {"skill": ["management", "communication", "psychology"], "domain": ["business", "hr"], "comm": ["excellent"], "edu": ["mba", "bba", "ba"]},
    "Chemist": {"skill": ["chemistry", "lab", "research"], "domain": ["science", "research"], "comm": ["average", "good"], "edu": ["bsc", "msc", "phd"]},
    "Mechanical Engineer": {"skill": ["mechanics", "cad", "physics"], "domain": ["engineering", "manufacturing"], "comm": ["average", "good"], "edu": ["btech", "mtech", "diploma"]},
    "Civil Engineer": {"skill": ["construction", "cad", "physics"], "domain": ["engineering", "infrastructure"], "comm": ["average", "good"], "edu": ["btech", "mtech", "diploma"]},
    "Full Stack Developer": {"skill": ["web", "javascript", "python", "database"], "domain": ["technology"], "comm": ["good", "average"], "edu": ["btech", "mca", "bsc"]},
    "Data Analyst": {"skill": ["data", "sql", "excel", "math"], "domain": ["analytics", "business"], "comm": ["good"], "edu": ["bsc", "bba", "btech"]},
    "Machine Learning Engineer": {"skill": ["python", "data", "math"], "domain": ["technology", "analytics"], "comm": ["good"], "edu": ["btech", "mtech", "msc"]},
    "Data Engineer": {"skill": ["data", "python", "sql", "database"], "domain": ["technology", "analytics"], "comm": ["good"], "edu": ["btech", "mca"]},
    "DevOps Engineer": {"skill": ["linux", "networking", "python", "security"], "domain": ["technology", "infrastructure"], "comm": ["good"], "edu": ["btech", "mca"]},
}

data = []
num_samples = 3000

for _ in range(num_samples):
    career = random.choice(list(career_profiles.keys()))
    profile = career_profiles[career]
    
    # Sometimes add noise to simulate real-world varied dataset
    if random.random() < 0.05:
        all_skills = [s for p in career_profiles.values() for s in p["skill"]]
        skill = random.choice(all_skills)
    else:
        skill = random.choice(profile["skill"])
        
    if random.random() < 0.05:
        all_domains = [d for p in career_profiles.values() for d in p["domain"]]
        domain = random.choice(all_domains)
    else:
        domain = random.choice(profile["domain"])
        
    comm = random.choice(["poor", "average", "good", "excellent"]) if random.random() < 0.1 else random.choice(profile["comm"])
    edu = random.choice(["high_school", "diploma", "bsc", "ba", "btech", "bca", "mca", "mtech", "mba", "phd"]) if random.random() < 0.05 else random.choice(profile["edu"])
    
    data.append({
        "technical_skill": skill,
        "communication": comm,
        "preferred_domain": domain,
        "education": edu,
        "career": career
    })

df = pd.DataFrame(data)

os.makedirs("data", exist_ok=True)
csv_path = os.path.join("data", "career_dataset.csv")
df.to_csv(csv_path, index=False)
print(f"Dataset generated and saved to {csv_path} with {len(df)} records.")
