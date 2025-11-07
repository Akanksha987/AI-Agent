"""Simple script to run the web interface."""
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

if __name__ == '__main__':
    from web.app import app
    
    port = int(os.getenv('WEB_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"🏥 Starting HealthSense Web Interface...")
    print(f"📡 Server running on http://localhost:{port}")
    print(f"🔧 Debug mode: {debug}")
    print(f"\nPress Ctrl+C to stop the server\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)

