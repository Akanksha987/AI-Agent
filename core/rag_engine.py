"""RAG (Retrieval-Augmented Generation) engine for medical facts."""
import re
from typing import List, Optional
from core.models import MedicalFact
from data.medical_facts import get_facts_by_keywords, get_all_facts
from core.exceptions import RAGError
from core.logger import setup_logger

logger = setup_logger(__name__)


class RAGEngine:
    """Retrieval-Augmented Generation engine for medical knowledge."""
    
    def __init__(self, top_k: int = 5):
        """Initialize RAG engine.
        
        Args:
            top_k: Number of facts to retrieve
        """
        self.top_k = top_k
        logger.info(f"RAG Engine initialized with top_k={top_k}")
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from symptom text.
        
        Args:
            text: Symptom description text
            
        Returns:
            List of extracted keywords
        """
        # Convert to lowercase and split
        text_lower = text.lower()
        
        # Common medical keywords to look for
        medical_keywords = [
            "fever", "headache", "pain", "ache", "nausea", "vomiting",
            "diarrhea", "cough", "sore throat", "fatigue", "tired",
            "shortness of breath", "chest pain", "abdominal", "stomach",
            "rash", "itching", "swelling", "dizziness", "lightheaded",
            "chills", "sweating", "muscle", "joint", "stiffness",
            "numbness", "tingling", "weakness", "confusion", "anxiety",
            "depression", "mood", "sleep", "appetite", "weight"
        ]
        
        found_keywords = []
        for keyword in medical_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
        
        # Also extract individual words (excluding common stop words)
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", 
                     "to", "for", "of", "with", "by", "i", "have", "had", "has",
                     "been", "is", "are", "was", "were", "be", "been", "being"}
        
        words = re.findall(r'\b\w+\b', text_lower)
        for word in words:
            if len(word) > 3 and word not in stop_words and word not in found_keywords:
                found_keywords.append(word)
        
        return found_keywords[:20]  # Limit to top 20 keywords
    
    def retrieve_relevant_facts(self, symptoms: str, top_k: Optional[int] = None) -> List[MedicalFact]:
        """Retrieve most relevant medical facts for symptoms.
        
        Args:
            symptoms: Symptom description text
            top_k: Number of facts to retrieve (overrides default)
            
        Returns:
            List of MedicalFact objects with source citations
            
        Raises:
            RAGError: If retrieval fails
        """
        try:
            if not symptoms or not symptoms.strip():
                logger.warning("Empty symptoms provided to RAG engine")
                return []
            
            k = top_k if top_k is not None else self.top_k
            keywords = self.extract_keywords(symptoms)
            
            if not keywords:
                logger.warning("No keywords extracted from symptoms")
                # Return general facts if no keywords found
                all_facts = get_all_facts()
                return all_facts[:k]
            
            logger.debug(f"Extracted keywords: {keywords}")
            facts = get_facts_by_keywords(keywords, k)
            
            if not facts:
                logger.info("No matching facts found, returning general facts")
                all_facts = get_all_facts()
                return all_facts[:k]
            
            logger.info(f"Retrieved {len(facts)} relevant medical facts")
            return facts
            
        except Exception as e:
            logger.error(f"Error in RAG retrieval: {e}")
            raise RAGError(f"Failed to retrieve medical facts: {e}")
    
    def format_facts_for_prompt(self, facts: List[MedicalFact]) -> str:
        """Format medical facts for inclusion in LLM prompt.
        
        Args:
            facts: List of MedicalFact objects
            
        Returns:
            Formatted string of facts
        """
        if not facts:
            return "No specific medical facts available."
        
        formatted = "Medical Facts:\n"
        for i, fact in enumerate(facts, 1):
            formatted += f"{i}. {fact.fact}"
            if fact.source:
                formatted += f" (Source: {fact.source})"
            formatted += "\n"
        
        return formatted
