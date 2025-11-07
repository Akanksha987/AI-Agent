"""Web interface for HealthSense using Flask."""
from flask import Flask, render_template, request, jsonify
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.config import Config
from core.logger import setup_logger
from core.exceptions import (
    GeminiAPIError, ConfigurationError, ValidationError
)
from core.gemini_client import GeminiClient
from core.rag_engine import RAGEngine
from core.diagnosis_logic import DiagnosisAnalyzer

app = Flask(__name__)
logger = setup_logger("healthsense.web")

# Initialize components
try:
    config = Config.from_env()
    gemini_client = GeminiClient(
        api_key=config.gemini_api_key,
        timeout=config.timeout,
        max_retries=config.max_retries
    )
    rag_engine = RAGEngine(top_k=config.rag_top_k)
    analyzer = DiagnosisAnalyzer(gemini_client, rag_engine)
    logger.info("Web application initialized successfully")
except ConfigurationError as e:
    logger.error(f"Configuration error: {e}")
    analyzer = None


@app.route('/')
def index():
    """Render main page."""
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """API endpoint for symptom analysis."""
    if analyzer is None:
        return jsonify({
            "error": "Service not configured. Please set GEMINI_API_KEY environment variable."
        }), 500
    
    try:
        data = request.get_json()
        symptoms = data.get('symptoms', '').strip()
        prompt_type = data.get('prompt_type', 'zero')
        include_lifestyle = data.get('include_lifestyle', False)
        
        if not symptoms:
            return jsonify({"error": "Symptoms are required"}), 400
        
        # Analyze symptoms
        result = analyzer.analyze_symptoms(
            symptoms=symptoms,
            prompt_type=prompt_type,
            include_lifestyle=include_lifestyle
        )
        
        return jsonify(result.to_dict())
        
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except GeminiAPIError as e:
        logger.error(f"API error: {e}")
        return jsonify({"error": "Service temporarily unavailable. Please try again later."}), 503
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return jsonify({"error": "An unexpected error occurred"}), 500


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "configured": analyzer is not None
    })


if __name__ == '__main__':
    port = int(os.getenv('WEB_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)

