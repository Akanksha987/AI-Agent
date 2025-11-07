"""Main entry point for HealthSense CLI application."""
import sys
import os
from pathlib import Path
from typing import Optional

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.config import Config
from core.logger import setup_logger
from core.exceptions import (
    HealthSenseError, GeminiAPIError, ConfigurationError, ValidationError
)
from core.gemini_client import GeminiClient
from core.rag_engine import RAGEngine
from core.diagnosis_logic import DiagnosisAnalyzer
from utils.flags_handler import parse_args
from utils.output_format import OutputFormatter

logger = setup_logger("healthsense")


def validate_input(symptoms: str) -> None:
    """Validate user input."""
    if not symptoms or not symptoms.strip():
        raise ValidationError("Please provide symptoms to analyze.")


def analyze_health_query(symptoms: str, args) -> dict:
    """Analyze health query and return results.
    
    Args:
        symptoms: Symptom description
        args: Parsed command line arguments
        
    Returns:
        Dictionary containing diagnosis results
    """
    try:
        # Initialize configuration
        config = Config.from_env()
        
        # Initialize components
        gemini_client = GeminiClient(
            api_key=config.gemini_api_key,
            timeout=config.timeout,
            max_retries=config.max_retries
        )
        
        rag_engine = RAGEngine(top_k=config.rag_top_k)
        analyzer = DiagnosisAnalyzer(gemini_client, rag_engine)
        
        # Perform analysis
        result = analyzer.analyze_symptoms(
            symptoms=symptoms,
            prompt_type=args.prompt,
            include_lifestyle=args.lifestyle
        )
        
        # Convert to dictionary
        return result.to_dict()
        
    except ConfigurationError as e:
        logger.error(f"Configuration error: {e}")
        print(f"\n❌ Configuration Error: {e}\n")
        print("Please set your GEMINI_API_KEY environment variable:")
        print("  Windows: set GEMINI_API_KEY=your_key_here")
        print("  Linux/Mac: export GEMINI_API_KEY=your_key_here")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise


def output_result(result: dict, format_type: Optional[str], save_path: Optional[str] = None) -> None:
    """Output result in specified format.
    
    Args:
        result: Diagnosis result dictionary
        format_type: Output format ('json' or 'text')
        save_path: Optional path to save output
    """
    formatter = OutputFormatter()
    
    if format_type == "json":
        output = formatter.format_json(result)
    else:
        output = formatter.format_text(result)
    
    print(output)
    
    # Save to file if requested
    if save_path:
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                if format_type == "json":
                    import json
                    json.dump(result, f, indent=2)
                else:
                    f.write(output)
            print(f"\n✅ Results saved to: {save_path}")
        except Exception as e:
            logger.error(f"Failed to save output: {e}")
            print(f"\n❌ Failed to save output: {e}")


def main():
    """Main entry point."""
    try:
        # Parse arguments
        args = parse_args()
        
        # Validate input
        validate_input(args.symptoms)
        
        # Analyze symptoms
        logger.info(f"Analyzing symptoms: {args.symptoms[:50]}...")
        result = analyze_health_query(args.symptoms, args)
        
        # Determine output format
        format_type = "json" if args.save and args.save.lower() == "json" else "text"
        if args.save and args.save.lower() == "txt":
            format_type = "text"
        
        # Generate save path if requested
        save_path = None
        if args.save:
            if args.save.lower() in ["json", "txt"]:
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                ext = "json" if args.save.lower() == "json" else "txt"
                save_path = f"diagnosis_{timestamp}.{ext}"
            else:
                save_path = args.save
        
        # Output result
        output_result(result, format_type, save_path)
        
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)
    except GeminiAPIError as e:
        logger.error(f"API error: {e}")
        print("\n❌ Service temporarily unavailable. Please try again later.")
        print("If the problem persists, check your API key and internet connection.\n")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        print("\n\n⚠️  Interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Unexpected error: {e}", exc_info=True)
        print("\n❌ An unexpected error occurred. Please check the logs for details.")
        print(f"Error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
