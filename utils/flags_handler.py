"""Command line argument parsing."""
import argparse
from typing import Any


def parse_args() -> Any:
    """Parse command line arguments.
    
    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="HealthSense CLI - AI Health Diagnosis Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python health_sense.py "I have a headache and feel nauseous"
  python health_sense.py "Chest pain and shortness of breath" --lifestyle
  python health_sense.py "Fever and sore throat" --save json
  python health_sense.py "Fatigue and dizziness" --prompt role
        """
    )
    parser.add_argument(
        "symptoms",
        type=str,
        help="Describe your symptoms (enclose in quotes if multiple words)"
    )
    parser.add_argument(
        "--details",
        action="store_true",
        help="Provide detailed explanation (always enabled)"
    )
    parser.add_argument(
        "--lifestyle",
        action="store_true",
        help="Include lifestyle and wellness suggestions"
    )
    parser.add_argument(
        "--save",
        type=str,
        help="Save output to file (specify 'json', 'txt', or a file path)"
    )
    parser.add_argument(
        "--prompt",
        choices=["zero", "few", "chain", "role"],
        default="zero",
        help="Select prompting strategy (default: zero)"
    )
    parser.add_argument(
        "--no-disclaimer",
        action="store_true",
        help="Skip medical disclaimer (not recommended)"
    )
    return parser.parse_args()
