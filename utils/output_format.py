"""Output formatting utilities."""
import json
from typing import Dict, Any, Optional


class OutputFormatter:
    """Formats diagnosis results for display."""
    
    def format_json(self, data: Dict[str, Any]) -> str:
        """Format data as JSON.
        
        Args:
            data: Data dictionary
            
        Returns:
            Formatted JSON string
        """
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def format_text(self, data: Dict[str, Any]) -> str:
        """Format data as human-readable text.
        
        Args:
            data: Data dictionary
            
        Returns:
            Formatted text string
        """
        output = []
        output.append("=" * 70)
        output.append("🏥 HealthSense - AI Health Diagnosis Results")
        output.append("=" * 70)
        output.append("")
        
        # Urgency flag
        if data.get("flagged", False):
            urgency = data.get("urgency_level", "Moderate")
            output.append(f"⚠️  URGENCY LEVEL: {urgency.upper()}")
            output.append("")
        
        # Possible conditions
        conditions = data.get("possible_conditions", [])
        if conditions:
            output.append("📋 Possible Conditions:")
            output.append("-" * 70)
            for i, cond in enumerate(conditions, 1):
                output.append(f"\n{i}. {cond.get('condition', 'Unknown')}")
                output.append(f"   Confidence: {cond.get('confidence', 'N/A')}")
                output.append(f"   Urgency: {cond.get('urgency', 'N/A')}")
                output.append(f"   Reasoning: {cond.get('reasoning', 'N/A')}")
                output.append(f"   Recommendation: {cond.get('recommendation', 'N/A')}")
                if cond.get('related_symptoms'):
                    output.append(f"   Related Symptoms: {', '.join(cond['related_symptoms'])}")
            output.append("")
        
        # Next steps
        next_steps = data.get("next_steps", [])
        if next_steps:
            output.append("📝 Recommended Next Steps:")
            output.append("-" * 70)
            for i, step in enumerate(next_steps, 1):
                output.append(f"   {i}. {step}")
            output.append("")
        
        # Lifestyle suggestions
        lifestyle = data.get("lifestyle_suggestions", [])
        if lifestyle:
            output.append("💡 Lifestyle Suggestions:")
            output.append("-" * 70)
            for i, suggestion in enumerate(lifestyle, 1):
                output.append(f"   {i}. {suggestion}")
            output.append("")
        
        # Disclaimer
        disclaimer = data.get("disclaimer", "")
        if disclaimer:
            output.append("⚠️  Important Notice:")
            output.append("-" * 70)
            output.append(f"   {disclaimer}")
            output.append("")
        
        output.append("=" * 70)
        
        return "\n".join(output)
    
    def output(self, data: Dict[str, Any], format_type: str) -> None:
        """Output data in specified format.
        
        Args:
            data: Data to output
            format_type: Output format ('json', 'text', etc.)
        """
        if format_type == 'json':
            print(self.format_json(data))
        elif format_type == 'text':
            print(self.format_text(data))
        else:
            raise ValueError(f"Unsupported format type: {format_type}")
