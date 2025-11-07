"""Data modules for HealthSense."""
from data.medical_facts import MEDICAL_FACTS_DB, get_facts_by_keywords, get_all_facts

__all__ = ["MEDICAL_FACTS_DB", "get_facts_by_keywords", "get_all_facts"]

