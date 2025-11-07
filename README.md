# 🤖 HealthSense - AI Health Diagnosis Assistant

An AI-powered health diagnosis assistant using Google's Gemini AI, LLMs, and Retrieval-Augmented Generation (RAG) to analyze user symptoms, suggest potential conditions, and offer informed next steps—securely and responsibly.

## 🚀 Features

- **Natural Language Symptom Input**: Gemini AI interprets complex, free-form health descriptions
- **RAG-Powered Insights**: Retrieves accurate medical facts from verified sources
- **Condition Prediction**: Suggests potential health issues with reasoning and confidence levels
- **Triage Suggestions**: Recommends basic care steps (e.g., rest, hydrate, consult doctor)
- **Critical Flagging**: Identifies urgent symptoms requiring immediate attention
- **Web Interface**: Beautiful, modern web UI for easy interaction
- **CLI Interface**: Command-line tool for quick analysis
- **Multiple Prompting Strategies**: Zero-shot, few-shot, and role-based prompting
- **Ethical & Private**: Maintains strict data privacy; not a replacement for licensed medical advice

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Setup

1. Clone the repository:
```bash
git clone https://github.com/username/healthsense-cli.git
cd healthsense-cli
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set your Gemini API key:

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

**Windows (Command Prompt):**
```cmd
set GEMINI_API_KEY=your_api_key_here
```

**Linux/Mac:**
```bash
export GEMINI_API_KEY="your_api_key_here"
```

**Or create a `.env` file:**
```
GEMINI_API_KEY=your_api_key_here
```

## 🎯 Usage

### CLI Usage

```bash
# Basic symptom input
python health_sense.py "I've had a sore throat and mild fever for 2 days"

# Get detailed explanation with condition suggestions
python health_sense.py "Headache, nausea, light sensitivity" --details

# Include lifestyle suggestions
python health_sense.py "Fatigue after work" --lifestyle

# Use different prompting strategy
python health_sense.py "Chest pain and shortness of breath" --prompt role

# Export diagnosis to file
python health_sense.py "Stomach cramps and diarrhea" --save json
python health_sense.py "Fever and cough" --save diagnosis.txt
```

### Web Interface

Start the web server:
```bash
python run_web.py
```

Then open your browser to `http://localhost:5000`

You can also customize the port:
```bash
set WEB_PORT=8080
python run_web.py
```

## 📋 Output Format

### JSON Output

```json
{
  "possible_conditions": [
    {
      "condition": "Migraine",
      "confidence": "High",
      "reasoning": "User reports nausea, light sensitivity, and headache—common migraine indicators.",
      "recommendation": "Hydration, dark room rest, consult physician if recurring",
      "urgency": "Moderate",
      "related_symptoms": ["headache", "nausea", "light sensitivity"]
    }
  ],
  "flagged": false,
  "urgency_level": "Moderate",
  "lifestyle_suggestions": [
    "Maintain regular sleep schedule",
    "Stay hydrated",
    "Avoid known triggers"
  ],
  "next_steps": [
    "Rest in a dark, quiet room",
    "Stay hydrated",
    "Consult a healthcare provider if symptoms persist"
  ],
  "disclaimer": "⚠️ IMPORTANT: This is not a substitute for professional medical advice..."
}
```

### Text Output

The CLI provides a beautifully formatted text output with:
- Urgency level indicators
- Condition details with confidence levels
- Reasoning and recommendations
- Next steps
- Lifestyle suggestions (if requested)
- Medical disclaimer

## 🏗️ Architecture

```
AI-Health-Diagnosis/
├── health_sense.py          # Main CLI entry point
├── run_web.py               # Web interface launcher
├── generativeai.py          # Legacy module (backward compatibility)
├── core/
│   ├── __init__.py
│   ├── models.py            # Data models (DiagnosisResult, Condition, etc.)
│   ├── config.py            # Configuration management
│   ├── logger.py            # Logging setup
│   ├── exceptions.py        # Custom exceptions
│   ├── gemini_client.py     # Gemini AI integration
│   ├── rag_engine.py        # Medical knowledge retrieval
│   └── diagnosis_logic.py   # Symptom analysis and reasoning
├── data/
│   ├── __init__.py
│   └── medical_facts.py     # Curated medical knowledge base
├── utils/
│   ├── __init__.py
│   ├── output_format.py     # JSON/text response formatting
│   └── flags_handler.py     # CLI argument parsing
├── web/
│   ├── __init__.py
│   ├── app.py               # Flask web application
│   └── templates/
│       └── index.html       # Web UI
├── requirements.txt
├── .gitignore
└── README.md
```

## 🎨 CLI Flags

- `--details`: Provides full condition reasoning and suggestions (always enabled)
- `--lifestyle`: Include lifestyle and wellness suggestions
- `--save [format]`: Save output to file (specify 'json', 'txt', or a file path)
- `--prompt [type]`: Select prompting strategy (zero, few, chain, role) - default: zero
- `--no-disclaimer`: Skip medical disclaimer (not recommended)

## 🔧 Configuration

Environment variables:

- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `GEMINI_TIMEOUT`: API timeout in seconds (default: 30)
- `GEMINI_MAX_RETRIES`: Maximum retry attempts (default: 3)
- `RAG_TOP_K`: Number of medical facts to retrieve (default: 5)
- `LOG_LEVEL`: Logging level (default: INFO)
- `WEB_PORT`: Web server port (default: 5000)
- `FLASK_DEBUG`: Enable Flask debug mode (default: false)

## 🛡️ Safety & Ethics

- **Not a Medical Device**: This tool is for informational purposes only
- **Always Consult Professionals**: Never use this as a replacement for professional medical care
- **Emergency Situations**: For medical emergencies, call emergency services immediately
- **Privacy**: No user data is stored or transmitted to third parties (except to Gemini API for analysis)
- **Disclaimer**: All outputs include appropriate medical disclaimers

## 🧪 How It Works

1. **Input Processing**: User provides symptom description
2. **Keyword Extraction**: RAG engine extracts relevant medical keywords
3. **Knowledge Retrieval**: Retrieves relevant medical facts from curated database
4. **AI Analysis**: Gemini AI analyzes symptoms with medical context
5. **Rule-Based Validation**: Checks for urgent keywords and validates results
6. **Result Formatting**: Formats and presents results with confidence levels and recommendations

## 🤝 Contributing

Pull requests welcome! Please ensure:
- Medical references are from trusted sources
- Code follows existing style and patterns
- All tests pass
- Documentation is updated

## 📝 License

[Add your license here]

## ⚠️ Disclaimer

This application is provided for educational and informational purposes only. It is not intended to be a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition. Never disregard professional medical advice or delay in seeking it because of something you have read or generated using this application.

For medical emergencies, call your local emergency services immediately.
