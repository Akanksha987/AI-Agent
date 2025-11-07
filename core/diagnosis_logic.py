"""Core diagnosis logic combining rules and LLM analysis."""
import re
from typing import List, Optional
from core.models import (
    DiagnosisResult, Condition, ConfidenceLevel, 
    UrgencyLevel, MedicalFact
)
from core.gemini_client import GeminiClient
from core.rag_engine import RAGEngine
from core.exceptions import ValidationError
from core.logger import setup_logger

logger = setup_logger(__name__)

# Medical disclaimer
MEDICAL_DISCLAIMER = (
    "⚠️ IMPORTANT: This is not a substitute for professional medical advice. "
    "Always consult with a qualified healthcare provider for proper diagnosis and treatment. "
    "For medical emergencies, call emergency services immediately."
)

# Urgent keywords that require immediate attention
URGENT_KEYWORDS = [
    "chest pain", "heart attack", "stroke", "severe difficulty breathing",
    "can't breathe", "unconscious", "severe bleeding", "severe allergic reaction",
    "severe burn", "severe head injury", "severe abdominal pain", "severe pain",
    "loss of consciousness", "seizure", "choking", "severe trauma",
    "sudden severe headache", "thunderclap headache", "severe dizziness",
    "severe confusion", "severe weakness", "paralysis"
]


def check_urgent_keywords(symptoms: str) -> bool:
    """Check if symptoms contain urgent keywords.
    
    Args:
        symptoms: Symptom description text
        
    Returns:
        True if urgent keywords are found
    """
    symptoms_lower = symptoms.lower()
    for keyword in URGENT_KEYWORDS:
        if keyword in symptoms_lower:
            logger.warning(f"Urgent keyword detected: {keyword}")
            return True
    return False


def validate_symptoms(symptoms: str) -> None:
    """Validate symptom input.
    
    Args:
        symptoms: Symptom description text
        
    Raises:
        ValidationError: If symptoms are invalid
    """
    if not symptoms or not symptoms.strip():
        raise ValidationError("Symptoms cannot be empty. Please describe your symptoms.")
    
    if len(symptoms.strip()) < 3:
        raise ValidationError("Symptom description is too short. Please provide more details.")
    
    if len(symptoms) > 2000:
        raise ValidationError("Symptom description is too long. Please keep it under 2000 characters.")


def parse_llm_response(response: dict) -> DiagnosisResult:
    """Parse LLM response into DiagnosisResult object.
    
    Args:
        response: Dictionary response from LLM
        
    Returns:
        DiagnosisResult object
    """
    conditions = []
    
    for cond_data in response.get("conditions", []):
        try:
            confidence = ConfidenceLevel(cond_data.get("confidence", "Low"))
        except ValueError:
            confidence = ConfidenceLevel.LOW
        
        try:
            urgency = UrgencyLevel(cond_data.get("urgency", "Moderate"))
        except ValueError:
            urgency = UrgencyLevel.MODERATE
        
        condition = Condition(
            name=cond_data.get("name", "Unknown Condition"),
            confidence=confidence,
            reasoning=cond_data.get("reasoning", "No reasoning provided"),
            recommendation=cond_data.get("recommendation", "Consult a healthcare provider"),
            urgency=urgency,
            related_symptoms=cond_data.get("related_symptoms", [])
        )
        conditions.append(condition)
    
    # Determine overall urgency
    is_urgent = response.get("is_urgent", False)
    urgency_level_str = response.get("urgency_level", "Moderate")
    try:
        urgency_level = UrgencyLevel(urgency_level_str)
    except ValueError:
        urgency_level = UrgencyLevel.MODERATE
    
    # If any condition is critical/urgent, flag it
    if not is_urgent:
        for cond in conditions:
            if cond.urgency in [UrgencyLevel.CRITICAL, UrgencyLevel.URGENT]:
                is_urgent = True
                urgency_level = cond.urgency
                break
    
    return DiagnosisResult(
        conditions=conditions,
        flagged=is_urgent,
        urgency_level=urgency_level,
        disclaimer=MEDICAL_DISCLAIMER,
        lifestyle_suggestions=response.get("lifestyle_suggestions"),
        next_steps=response.get("next_steps", []),
        metadata={
            "source": "gemini_ai",
            "conditions_count": len(conditions)
        }
    )


class DiagnosisAnalyzer:
    """Main analyzer for health symptoms."""
    
    def __init__(self, gemini_client: GeminiClient, rag_engine: RAGEngine):
        """Initialize diagnosis analyzer.
        
        Args:
            gemini_client: Gemini API client
            rag_engine: RAG engine for medical facts
        """
        self.gemini_client = gemini_client
        self.rag_engine = rag_engine
        logger.info("DiagnosisAnalyzer initialized")
    
    def analyze_symptoms(
        self, 
        symptoms: str, 
        prompt_type: str = "zero",
        include_lifestyle: bool = False
    ) -> DiagnosisResult:
        """Core diagnosis logic combining rules and LLM.
        
        Args:
            symptoms: Symptom description
            prompt_type: Type of prompting strategy
            include_lifestyle: Whether to include lifestyle suggestions
            
        Returns:
            DiagnosisResult object
        """
        # Validate input
        validate_symptoms(symptoms)
        
        # Check urgent keywords first (rule-based)
        is_urgent_rule = check_urgent_keywords(symptoms)
        logger.info(f"Rule-based urgent check: {is_urgent_rule}")
        
        # Retrieve relevant medical facts using RAG
        medical_facts = self.rag_engine.retrieve_relevant_facts(symptoms)
        logger.info(f"Retrieved {len(medical_facts)} medical facts")
        
        # Get LLM analysis
        try:
            llm_response = self.gemini_client.analyze_symptoms(
                symptoms, 
                medical_facts,
                prompt_type=prompt_type,
                include_lifestyle=include_lifestyle
            )
        except Exception as e:
            logger.error(f"LLM analysis failed: {e}")
            # Return a basic fallback result
            return DiagnosisResult(
                conditions=[Condition(
                    name="Analysis Unavailable",
                    confidence=ConfidenceLevel.LOW,
                    reasoning="Unable to analyze symptoms at this time. Please consult a healthcare provider.",
                    recommendation="Please consult with a healthcare professional for proper evaluation.",
                    urgency=UrgencyLevel.MODERATE
                )],
                flagged=is_urgent_rule,
                urgency_level=UrgencyLevel.URGENT if is_urgent_rule else UrgencyLevel.MODERATE,
                disclaimer=MEDICAL_DISCLAIMER,
                next_steps=["Consult a healthcare provider", "Monitor symptoms"],
                metadata={"error": str(e)}
            )
        
        # Parse LLM response
        result = parse_llm_response(llm_response)
        
        # Combine rule-based and LLM urgency flags
        if is_urgent_rule and not result.flagged:
            result.flagged = True
            if result.urgency_level == UrgencyLevel.MODERATE:
                result.urgency_level = UrgencyLevel.URGENT
        
        # Add metadata
        result.metadata.update({
            "rule_based_urgent": is_urgent_rule,
            "medical_facts_count": len(medical_facts)
        })
        
        logger.info(f"Analysis complete: {len(result.conditions)} conditions, urgent={result.flagged}")
        return result
