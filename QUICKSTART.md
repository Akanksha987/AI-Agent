# Quick Start Guide

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Get Your API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key

## 3. Set Your API Key

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

## 4. Test the CLI

```bash
python health_sense.py "I have a headache and feel nauseous"
```

## 5. Try the Web Interface

```bash
python run_web.py
```

Then open your browser to: http://localhost:5000

## Example Commands

```bash
# Basic analysis
python health_sense.py "Fever and sore throat for 2 days"

# With lifestyle suggestions
python health_sense.py "Feeling tired and fatigued" --lifestyle

# Save to JSON file
python health_sense.py "Headache and dizziness" --save json

# Use role-based prompting
python health_sense.py "Chest pain" --prompt role
```

## Troubleshooting

**Error: GEMINI_API_KEY not set**
- Make sure you've set the environment variable correctly
- On Windows, you may need to set it in each new terminal session
- Consider using a `.env` file with python-dotenv

**Error: Module not found**
- Make sure you've installed all dependencies: `pip install -r requirements.txt`
- Check that you're in the project directory

**API Errors**
- Verify your API key is correct
- Check your internet connection
- Ensure you have API quota remaining

