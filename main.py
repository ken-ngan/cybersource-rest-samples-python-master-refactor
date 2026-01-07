"""
Main application entry point for CyberSource REST Samples.
"""
import os
from flask import Flask
from dotenv import load_dotenv
from views import views
from config_loader import SecureConfig, ConfigError

# Load environment variables from .env file
load_dotenv()

# Initialize secure configuration
try:
    config = SecureConfig()
    config.validate()
except ConfigError as e:
    print(f"Configuration Error: {e}")
    print("Please ensure all required environment variables are set.")
    exit(1)

app = Flask(__name__)

# Security: Use environment variable for secret key
app.config['SECRET_KEY'] = config.FLASK_SECRET_KEY

# Security: Disable debug mode in production
app.config['DEBUG'] = config.FLASK_DEBUG
app.config['TEMPLATES_AUTO_RELOAD'] = config.FLASK_DEBUG

# Security: Additional production settings
if not config.FLASK_DEBUG:
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour

app.register_blueprint(views, url_prefix="/views")

if __name__ == "__main__":
    # Determine URL mode for conditional server startup
    url_mode = os.environ.get("URL_MODE", "localhost").lower()
    
    if url_mode == "ngrok":
        # For ngrok: Run without SSL (ngrok handles SSL termination)
        app.run(
            debug=config.FLASK_DEBUG,
            host=config.FLASK_HOST,
            port=config.FLASK_PORT
        )
    else:
        # For localhost: Run with SSL (adhoc certificate for HTTPS)
        app.run(debug=True, port=config.FLASK_PORT, ssl_context='adhoc')