"""Medical facts database for RAG retrieval."""
from typing import List
from core.models import MedicalFact


# Comprehensive medical facts database
MEDICAL_FACTS_DB: List[MedicalFact] = [
    # Fever and Infections
    MedicalFact(
        id="fever_001",
        fact="Fever is typically defined as a body temperature above 100.4°F (38°C). It's often a sign of infection or inflammation.",
        category="Fever",
        keywords=["fever", "temperature", "hot", "chills", "sweating"],
        source="Mayo Clinic",
        reliability_score=0.95
    ),
    MedicalFact(
        id="infection_001",
        fact="Common symptoms of viral infections include fever, fatigue, body aches, and respiratory symptoms.",
        category="Infection",
        keywords=["infection", "viral", "bacterial", "flu", "cold"],
        source="CDC",
        reliability_score=0.95
    ),
    
    # Respiratory
    MedicalFact(
        id="respiratory_001",
        fact="Shortness of breath, especially when accompanied by chest pain, can indicate serious conditions requiring immediate medical attention.",
        category="Respiratory",
        keywords=["shortness of breath", "difficulty breathing", "chest pain", "wheezing"],
        source="American Lung Association",
        reliability_score=0.98
    ),
    MedicalFact(
        id="respiratory_002",
        fact="Persistent cough lasting more than 3 weeks should be evaluated by a healthcare provider.",
        category="Respiratory",
        keywords=["cough", "persistent", "chronic"],
        source="American Thoracic Society",
        reliability_score=0.90
    ),
    
    # Headache and Neurological
    MedicalFact(
        id="headache_001",
        fact="Migraines often present with throbbing pain, nausea, sensitivity to light and sound, and can last 4-72 hours.",
        category="Neurological",
        keywords=["migraine", "headache", "throbbing", "nausea", "light sensitivity"],
        source="American Migraine Foundation",
        reliability_score=0.92
    ),
    MedicalFact(
        id="headache_002",
        fact="Sudden severe headache (thunderclap headache) requires immediate medical evaluation as it may indicate serious conditions.",
        category="Neurological",
        keywords=["sudden headache", "severe headache", "thunderclap"],
        source="Mayo Clinic",
        reliability_score=0.98
    ),
    
    # Digestive
    MedicalFact(
        id="digestive_001",
        fact="Gastroenteritis (stomach flu) typically causes nausea, vomiting, diarrhea, and abdominal cramps, usually resolving within 1-3 days.",
        category="Digestive",
        keywords=["nausea", "vomiting", "diarrhea", "stomach", "abdominal", "cramps"],
        source="CDC",
        reliability_score=0.93
    ),
    MedicalFact(
        id="digestive_002",
        fact="Severe abdominal pain, especially with fever or bloody stools, requires prompt medical evaluation.",
        category="Digestive",
        keywords=["severe abdominal pain", "bloody stool", "fever"],
        source="American Gastroenterological Association",
        reliability_score=0.95
    ),
    
    # Cardiovascular
    MedicalFact(
        id="cardiac_001",
        fact="Chest pain, especially when radiating to the arm, jaw, or back, along with shortness of breath, may indicate a heart condition requiring immediate attention.",
        category="Cardiovascular",
        keywords=["chest pain", "heart", "cardiac", "arm pain", "jaw pain"],
        source="American Heart Association",
        reliability_score=0.99
    ),
    
    # Fatigue
    MedicalFact(
        id="fatigue_001",
        fact="Chronic fatigue can be caused by various factors including sleep disorders, anemia, thyroid issues, or mental health conditions.",
        category="General",
        keywords=["fatigue", "tiredness", "exhaustion", "weakness"],
        source="Mayo Clinic",
        reliability_score=0.88
    ),
    
    # Skin
    MedicalFact(
        id="skin_001",
        fact="Rash with fever, especially in children, should be evaluated by a healthcare provider to rule out serious conditions.",
        category="Dermatological",
        keywords=["rash", "skin", "redness", "itching"],
        source="American Academy of Dermatology",
        reliability_score=0.90
    ),
    
    # Pain
    MedicalFact(
        id="pain_001",
        fact="Acute pain that is severe, sudden, or accompanied by other symptoms like fever or loss of function should be evaluated promptly.",
        category="General",
        keywords=["severe pain", "acute pain", "sudden pain"],
        source="American Pain Society",
        reliability_score=0.87
    ),
    
    # Mental Health
    MedicalFact(
        id="mental_001",
        fact="Persistent feelings of sadness, anxiety, or changes in sleep and appetite patterns may indicate mental health concerns that benefit from professional support.",
        category="Mental Health",
        keywords=["sadness", "anxiety", "depression", "mood"],
        source="National Institute of Mental Health",
        reliability_score=0.90
    ),
]


def get_facts_by_keywords(keywords: List[str], top_k: int = 5) -> List[MedicalFact]:
    """Get medical facts matching keywords (simple keyword matching)."""
    scored_facts = []
    
    for fact in MEDICAL_FACTS_DB:
        score = 0
        fact_keywords_lower = [k.lower() for k in fact.keywords]
        user_keywords_lower = [k.lower() for k in keywords]
        
        for user_keyword in user_keywords_lower:
            for fact_keyword in fact_keywords_lower:
                if user_keyword in fact_keyword or fact_keyword in user_keyword:
                    score += 1
                    break
        
        if score > 0:
            # Weight by reliability and match score
            final_score = score * fact.reliability_score
            scored_facts.append((final_score, fact))
    
    # Sort by score and return top_k
    scored_facts.sort(key=lambda x: x[0], reverse=True)
    return [fact for _, fact in scored_facts[:top_k]]


def get_all_facts() -> List[MedicalFact]:
    """Get all medical facts."""
    return MEDICAL_FACTS_DB

