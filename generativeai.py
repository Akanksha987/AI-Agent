"""Legacy generative AI module - use core.diagnosis_logic instead."""
from typing import List
from core.diagnosis_logic import DiagnosisAnalyzer
from core.gemini_client import GeminiClient
from core.rag_engine import RAGEngine
from core.config import Config


def generate_diagnosis(symptoms: List[str], medical_facts: List[str]) -> str:
    """
    Generate a medical diagnosis based on symptoms and medical facts.
    
    NOTE: This is a legacy function. For new code, use DiagnosisAnalyzer directly.

    Args:
        symptoms (List[str]): A list of symptoms reported by the patient.
        medical_facts (List[str]): A list of relevant medical facts.

    Returns:
        str: A generated diagnosis in JSON format.
    """
    try:
        config = Config.from_env()
        gemini_client = GeminiClient(
            api_key=config.gemini_api_key,
            timeout=config.timeout
        )
        rag_engine = RAGEngine()
        analyzer = DiagnosisAnalyzer(gemini_client, rag_engine)
        
        # Convert list to string
        symptoms_text = ", ".join(symptoms)
        
        # Analyze
        result = analyzer.analyze_symptoms(symptoms_text)
        
        # Return as JSON string
        import json
        return json.dumps(result.to_dict(), indent=2)
    except Exception as e:
        return f'{{"error": "Failed to generate diagnosis: {e}"}}'