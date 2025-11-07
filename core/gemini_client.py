"""Gemini AI client for health diagnosis."""
import json
import time
import os
from typing import Dict, Any, Optional, List
import google.generativeai as genai
from core.models import Condition, ConfidenceLevel, UrgencyLevel, MedicalFact
from core.exceptions import GeminiAPIError
from core.logger import setup_logger

logger = setup_logger(__name__)


class GeminiClient:
    """Client for interacting with Google's Gemini API."""
    
    def __init__(self, api_key: str, timeout: int = 30, max_retries: int = 3):
        """Initialize Gemini client.
        
        Args:
            api_key: Gemini API key
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self._configure_client()
        logger.info("Gemini client initialized")
    
    def _configure_client(self):
        """Configure the Gemini API client."""
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
            logger.error(f"Failed to configure Gemini client: {e}")
            raise GeminiAPIError(f"Failed to configure Gemini API: {e}")
    
    def _build_prompt(self, symptom_text: str, medical_facts: List[MedicalFact], 
                     prompt_type: str = "zero", include_lifestyle: bool = False) -> str:
        """Build prompt for Gemini based on prompt type.
        
        Args:
            symptom_text: User's symptom description
            medical_facts: Retrieved medical facts
            prompt_type: Type of prompting (zero, few, chain, role)
            include_lifestyle: Whether to include lifestyle suggestions
            
        Returns:
            Formatted prompt string
        """
        facts_text = "\n".join([f"- {fact.fact}" for fact in medical_facts])
        
        base_prompt = f"""You are a medical triage assistant. Your role is to help users understand their symptoms and provide informed guidance. You are NOT a replacement for professional medical care.

IMPORTANT DISCLAIMERS:
- This is for informational purposes only
- Always recommend consulting healthcare professionals for proper diagnosis
- Never provide definitive diagnoses
- Flag urgent symptoms that require immediate medical attention

User Symptoms: {symptom_text}

Relevant Medical Information:
{facts_text}

Based on the symptoms and medical information above, provide a structured analysis in JSON format with the following structure:
{{
    "conditions": [
        {{
            "name": "Condition name",
            "confidence": "High/Medium/Low",
            "reasoning": "Brief explanation of why this condition is possible",
            "recommendation": "Recommended actions or next steps",
            "urgency": "Critical/Urgent/Moderate/Low",
            "related_symptoms": ["symptom1", "symptom2"]
        }}
    ],
    "is_urgent": true/false,
    "urgency_level": "Critical/Urgent/Moderate/Low",
    "next_steps": ["step1", "step2", "step3"],
    "lifestyle_suggestions": ["suggestion1", "suggestion2"] (only if relevant)
}}

Guidelines:
1. Provide 1-3 most likely conditions (not more)
2. Use confidence levels appropriately (High only for very clear cases)
3. Always include reasoning for each condition
4. Set is_urgent=true for symptoms requiring immediate care (chest pain, severe difficulty breathing, loss of consciousness, etc.)
5. Provide actionable next steps
6. Be conservative - when in doubt, recommend professional consultation
7. Output ONLY valid JSON, no additional text
"""
        
        if prompt_type == "role":
            base_prompt = "You are an experienced medical triage nurse with 20 years of experience. " + base_prompt
        elif prompt_type == "few":
            base_prompt += "\n\nExample analysis:\n" + json.dumps({
                "conditions": [{
                    "name": "Common Cold",
                    "confidence": "Medium",
                    "reasoning": "Symptoms match common viral infection patterns",
                    "recommendation": "Rest, hydration, over-the-counter symptom relief",
                    "urgency": "Low",
                    "related_symptoms": ["cough", "sore throat"]
                }],
                "is_urgent": False,
                "urgency_level": "Low",
                "next_steps": ["Rest", "Stay hydrated", "Monitor symptoms"]
            }, indent=2)
        
        if include_lifestyle:
            base_prompt += "\n\nAlso provide general lifestyle and wellness suggestions that may help with symptom management."
        
        return base_prompt
    
    def analyze_symptoms(self, symptom_text: str, medical_facts: List[MedicalFact],
                        prompt_type: str = "zero", include_lifestyle: bool = False) -> Dict[str, Any]:
        """Send symptoms to Gemini with medical context.
        
        Args:
            symptom_text: User's symptom description
            medical_facts: RAG-retrieved medical facts
            prompt_type: Type of prompting strategy
            include_lifestyle: Whether to include lifestyle suggestions
            
        Returns:
            Structured diagnosis response dictionary
            
        Raises:
            GeminiAPIError: If API call fails after retries
        """
        prompt = self._build_prompt(symptom_text, medical_facts, prompt_type, include_lifestyle)
        
        for attempt in range(self.max_retries):
            try:
                logger.debug(f"Gemini API call attempt {attempt + 1}/{self.max_retries}")
                
                response = self.model.generate_content(
                    prompt,
                    generation_config={
                        "temperature": 0.3,  # Lower temperature for more consistent medical responses
                        "top_p": 0.8,
                        "top_k": 40,
                        "max_output_tokens": 2048,
                    }
                )
                
                response_text = response.text.strip()
                
                # Try to extract JSON from response
                json_text = self._extract_json(response_text)
                result = json.loads(json_text)
                
                logger.info("Successfully received response from Gemini API")
                return result
                
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse JSON response (attempt {attempt + 1}): {e}")
                if attempt == self.max_retries - 1:
                    # Last attempt - try to create a fallback response
                    logger.error("All attempts failed to parse JSON, creating fallback response")
                    return self._create_fallback_response(symptom_text)
                time.sleep(1)  # Brief delay before retry
                
            except Exception as e:
                logger.error(f"Gemini API error (attempt {attempt + 1}): {e}")
                if attempt == self.max_retries - 1:
                    raise GeminiAPIError(f"Failed to get response from Gemini API after {self.max_retries} attempts: {e}")
                time.sleep(2 ** attempt)  # Exponential backoff
        
        raise GeminiAPIError("Failed to get response from Gemini API")
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON from text response.
        
        Args:
            text: Response text that may contain JSON
            
        Returns:
            Extracted JSON string
        """
        # Try to find JSON in the response
        text = text.strip()
        
        # Look for JSON object boundaries
        start_idx = text.find('{')
        end_idx = text.rfind('}')
        
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            return text[start_idx:end_idx + 1]
        
        # If no JSON found, return the whole text (will fail JSON parse but we handle that)
        return text
    
    def _create_fallback_response(self, symptom_text: str) -> Dict[str, Any]:
        """Create a fallback response when API fails.
        
        Args:
            symptom_text: Original symptom text
            
        Returns:
            Basic fallback response dictionary
        """
        return {
            "conditions": [{
                "name": "Unable to analyze",
                "confidence": "Low",
                "reasoning": "Unable to process symptoms at this time. Please consult a healthcare provider.",
                "recommendation": "Please consult with a healthcare professional for proper evaluation.",
                "urgency": "Moderate",
                "related_symptoms": []
            }],
            "is_urgent": False,
            "urgency_level": "Moderate",
            "next_steps": ["Consult a healthcare provider", "Monitor symptoms", "Seek emergency care if symptoms worsen"],
            "lifestyle_suggestions": []
        }
