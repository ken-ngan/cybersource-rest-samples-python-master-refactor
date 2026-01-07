"""
Configuration module for CyberSource integration.
This module provides backward-compatible configuration loading from environment variables.
All secrets should be stored in environment variables, not hardcoded here.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# LOCAL HOST PARAMETERS
LOCAL_HOST = os.environ.get("LOCAL_HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "3000"))

# BASE_URL Configuration - Convenient switcher between localhost and ngrok
# Set URL_MODE environment variable to "localhost" or "ngrok" to switch
# Alternatively, set BASE_URL directly to override
URL_MODE = os.environ.get("URL_MODE", "localhost").lower()

# Predefined URLs
LOCALHOST_URL = f"https://{LOCAL_HOST}:{PORT}"
NGROK_URL = "https://swampier-melida-unsqueamishly.ngrok-free.dev"

# Select BASE_URL based on URL_MODE or use explicit BASE_URL if set
if os.environ.get("BASE_URL"):
    # Explicit BASE_URL takes precedence
    BASE_URL = os.environ.get("BASE_URL")
elif URL_MODE == "ngrok":
    BASE_URL = NGROK_URL
else:
    # Default to localhost
    BASE_URL = LOCALHOST_URL

# CYBS MID PARAMETERS
MERCHANT_ID = os.environ.get("MERCHANT_ID", "gphktoken")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "PROD")

# Configuration Mapping - DEPRECATED: Use environment variables instead
# This dictionary is kept for backward compatibility but should not contain real secrets
# All secrets should be loaded from environment variables
MERCHANT_CONFIG = {
    # This structure is maintained for backward compatibility
    # In production, all values should come from environment variables
    # Format: {MERCHANT_ID}_{ENVIRONMENT}_{CONFIG_KEY}
}

def _load_config_from_env(merchant_id: str, environment: str) -> dict:
    """
    Load merchant configuration from environment variables.
    Format: {MERCHANT_ID}_{ENVIRONMENT}_{CONFIG_KEY}
    """
    prefix = f"{merchant_id}_{environment}_"
    return {
        "MERCHANT_KEY_ID": os.environ.get(f"{prefix}MERCHANT_KEY_ID", ""),
        "MERCHANT_SECRET_KEY": os.environ.get(f"{prefix}MERCHANT_SECRET_KEY", ""),
        "SA_PROFILE_ID": os.environ.get(f"{prefix}SA_PROFILE_ID", ""),
        "SA_ACCESS_KEY": os.environ.get(f"{prefix}SA_ACCESS_KEY", ""),
        "SA_SECRET_KEY": os.environ.get(f"{prefix}SA_SECRET_KEY", ""),
        "SOP_PROFILE_ID": os.environ.get(f"{prefix}SOP_PROFILE_ID", ""),
        "SOP_ACCESS_KEY": os.environ.get(f"{prefix}SOP_ACCESS_KEY", ""),
        "SOP_SECRET_KEY": os.environ.get(f"{prefix}SOP_SECRET_KEY", ""),
        "SOAP_P12_FILE": os.environ.get(
            f"{prefix}SOAP_P12_FILE",
            f"./resources/SOAP_{environment}/{merchant_id}.p12"
        ),
        "SOAP_P12_PASSWORD": os.environ.get(f"{prefix}SOAP_P12_PASSWORD", ""),
        "SOAP_PASSWORD": os.environ.get(f"{prefix}SOAP_PASSWORD", ""),
    }

# Load current merchant configuration from environment variables
current_config = _load_config_from_env(MERCHANT_ID, ENVIRONMENT)

# Export configuration as module-level variables for backward compatibility
# SECURITY: These values come from environment variables, not hardcoded secrets
MERCHANT_KEY_ID = current_config.get("MERCHANT_KEY_ID", "")
MERCHANT_SECRET_KEY = current_config.get("MERCHANT_SECRET_KEY", "")
SA_PROFILE_ID = current_config.get("SA_PROFILE_ID", "")
SA_ACCESS_KEY = current_config.get("SA_ACCESS_KEY", "")
SA_SECRET_KEY = current_config.get("SA_SECRET_KEY", "")
SOP_PROFILE_ID = current_config.get("SOP_PROFILE_ID", "")
SOP_ACCESS_KEY = current_config.get("SOP_ACCESS_KEY", "")
SOP_SECRET_KEY = current_config.get("SOP_SECRET_KEY", "")
SOAP_P12_FILE = current_config.get("SOAP_P12_FILE", "")
SOAP_P12_PASSWORD = current_config.get("SOAP_P12_PASSWORD", "")
SOAP_PASSWORD = current_config.get("SOAP_PASSWORD", "")

# SOAP_USERNAME is usually same as MERCHANT_ID
SOAP_USERNAME = MERCHANT_ID

# [PROD] [CYBS] Simple Order API (for afs)
AFS_SOAP_USERNAME = os.environ.get("AFS_SOAP_USERNAME", "gphkdm")
AFS_SOAP_P12_FILE = os.environ.get("AFS_SOAP_P12_FILE", "./resources/SOAP_PROD/gphkdm.p12")
AFS_SOAP_P12_PASSWORD = os.environ.get("AFS_SOAP_P12_PASSWORD", "")
AFS_SOAP_WSDL = os.environ.get(
    "AFS_SOAP_WSDL",
    "https://ics2ws.ic3.com/commerce/1.x/transactionProcessor/CyberSourceTransaction_NVP_1.211.wsdl"
)

# [PROD] [MPGS] API
MPGS_MERCHANT_ID = os.environ.get("MPGS_MERCHANT_ID", "088008737800")
MPGS_API_PASSWORD = os.environ.get("MPGS_API_PASSWORD", "")
MPGS_BASE_URL = os.environ.get("MPGS_BASE_URL", "gphk.gateway.mastercard.com")
MPGS_API_VERSION = os.environ.get("MPGS_API_VERSION", "100")

# CYBS Endpoints
if ENVIRONMENT == "PROD":
    API_ENDPOINT = "api.cybersource.com"
    SA_URL = "https://secureacceptance.cybersource.com/pay"
    SA_CREATE_TOKEN_URL = "https://secureacceptance.cybersource.com/token/create"
    SA_UPDATE_TOKEN_URL = "https://secureacceptance.cybersource.com/token/update"
    SOP_URL = "https://secureacceptance.cybersource.com/silent/embedded/pay"
    SOP_CREATE_TOKEN_URL = "https://secureacceptance.cybersource.com/silent/token/create"
    SOAP_WSDL = "https://ics2ws.ic3.com/commerce/1.x/transactionProcessor/CyberSourceTransaction_NVP_1.211.wsdl"
else:
    API_ENDPOINT = "apitest.cybersource.com"
    SA_URL = "https://testsecureacceptance.cybersource.com/pay"
    SA_CREATE_TOKEN_URL = "https://testsecureacceptance.cybersource.com/token/create"
    SA_UPDATE_TOKEN_URL = "https://testsecureacceptance.cybersource.com/token/update"
    SOP_URL = "https://testsecureacceptance.cybersource.com/silent/embedded/pay"
    SOP_CREATE_TOKEN_URL = "https://testsecureacceptance.cybersource.com/silent/token/create"
    SOAP_WSDL = "https://ics2wstest.ic3.com/commerce/1.x/transactionProcessor/CyberSourceTransaction_NVP_1.211.wsdl"

# WS-Security XML Namespace Definitions
XML_NAMESPACES = {
    "soap": "http://schemas.xmlsoap.org/soap/envelope/",
    "wsse": "http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd",
    "wsu": "http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd",
    "ds": "http://www.w3.org/2000/09/xmldsig#",
}

# WS-Security Algorithm Definitions
XML_ALGORITHMS = {
    "c14n": "http://www.w3.org/2001/10/xml-exc-c14n#",
    "sha256": "http://www.w3.org/2001/04/xmldsig-more#rsa-sha256",
    "digest": "http://www.w3.org/2001/04/xmlenc#sha256",
    "encoding": "http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary",
    "x509": "http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-x509-token-profile-1.0#X509v3",
}
