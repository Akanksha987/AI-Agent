"""Data models for health diagnosis application."""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum


class ConfidenceLevel(str, Enum):
    """Confidence levels for diagnosis."""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class UrgencyLevel(str, Enum):
    """Urgency levels for medical conditions."""
    CRITICAL = "Critical"
    URGENT = "Urgent"
    MODERATE = "Moderate"
    LOW = "Low"


@dataclass
class MedicalFact:
    """Represents a medical fact with source citation."""
    id: str
    fact: str
    category: str
    keywords: List[str] = field(default_factory=list)
    source: Optional[str] = None
    reliability_score: float = 1.0


@dataclass
class Condition:
    """Represents a possible medical condition."""
    name: str
    confidence: ConfidenceLevel
    reasoning: str
    recommendation: str
    urgency: UrgencyLevel = UrgencyLevel.MODERATE
    related_symptoms: List[str] = field(default_factory=list)


@dataclass
class DiagnosisResult:
    """Complete diagnosis result."""
    conditions: List[Condition]
    flagged: bool = False
    urgency_level: UrgencyLevel = UrgencyLevel.MODERATE
    disclaimer: str = "This is not a substitute for professional medical advice. Please consult a healthcare provider."
    lifestyle_suggestions: Optional[List[str]] = None
    next_steps: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "possible_conditions": [
                {
                    "condition": c.name,
                    "confidence": c.confidence.value,
                    "reasoning": c.reasoning,
                    "recommendation": c.recommendation,
                    "urgency": c.urgency.value,
                    "related_symptoms": c.related_symptoms
                }
                for c in self.conditions
            ],
            "flagged": self.flagged,
            "urgency_level": self.urgency_level.value,
            "lifestyle_suggestions": self.lifestyle_suggestions or [],
            "next_steps": self.next_steps,
            "disclaimer": self.disclaimer,
            "metadata": self.metadata
        }

