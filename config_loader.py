"""
Secure configuration loader with environment variable support.
Validates required configuration and provides safe defaults.
"""
import os
from typing import Dict, Optional, Any
from pathlib import Path


class ConfigError(Exception):
    """Raised when configuration is invalid or missing."""
    pass


class SecureConfig:
    """
    Secure configuration manager that loads settings from environment variables.
    Provides validation and type conversion.
    """
    
    def __init__(self):
        """Initialize configuration from environment variables."""
        self._validate_required_env_vars()
        self._load_config()
    
    def _validate_required_env_vars(self) -> None:
        """Validate that critical environment variables are set."""
        required_vars = [
            'FLASK_SECRET_KEY',
            'MERCHANT_ID',
            'ENVIRONMENT'
        ]
        missing = [var for var in required_vars if not os.environ.get(var)]
        if missing:
            raise ConfigError(
                f"Missing required environment variables: {', '.join(missing)}. "
                f"Please set them in your .env file or environment."
            )
    
    def _load_config(self) -> None:
        """Load all configuration values."""
        # Flask Configuration
        self.FLASK_SECRET_KEY = os.environ['FLASK_SECRET_KEY']
        self.FLASK_DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
        self.FLASK_PORT = int(os.environ.get('FLASK_PORT', '3000'))
        self.FLASK_HOST = os.environ.get('FLASK_HOST', '127.0.0.1')
        
        # Base URL Configuration - Convenient switcher between localhost and ngrok
        # Set URL_MODE environment variable to "localhost" or "ngrok" to switch
        # Alternatively, set BASE_URL directly to override
        url_mode = os.environ.get("URL_MODE", "localhost").lower()
        localhost_url = f"https://{self.FLASK_HOST}:{self.FLASK_PORT}"
        ngrok_url = "https://swampier-melida-unsqueamishly.ngrok-free.dev"
        
        if os.environ.get("BASE_URL"):
            # Explicit BASE_URL takes precedence
            self.BASE_URL = os.environ.get("BASE_URL")
        elif url_mode == "ngrok":
            self.BASE_URL = ngrok_url
        else:
            # Default to localhost
            self.BASE_URL = localhost_url
        
        # CyberSource Configuration
        self.MERCHANT_ID = os.environ['MERCHANT_ID']
        self.ENVIRONMENT = os.environ['ENVIRONMENT']
        
        if self.ENVIRONMENT not in ['PROD', 'CAS']:
            raise ConfigError(
                f"ENVIRONMENT must be 'PROD' or 'CAS', got '{self.ENVIRONMENT}'"
            )
        
        # Load merchant-specific configuration
        self._load_merchant_config()
        
        # Supabase Configuration
        self.SUPABASE_URL = os.environ.get(
            'SUPABASE_URL',
            'https://itczbvtnjkfzjqmkfapc.supabase.co'
        )
        self.SUPABASE_KEY = os.environ.get('SUPABASE_KEY', '')
        
        if not self.SUPABASE_KEY:
            raise ConfigError("SUPABASE_KEY must be set in environment variables")
        
        # MPGS Configuration
        self.MPGS_MERCHANT_ID = os.environ.get('MPGS_MERCHANT_ID', '088008737800')
        self.MPGS_API_PASSWORD = os.environ.get('MPGS_API_PASSWORD', '')
        self.MPGS_BASE_URL = os.environ.get(
            'MPGS_BASE_URL',
            'gphk.gateway.mastercard.com'
        )
        self.MPGS_API_VERSION = os.environ.get('MPGS_API_VERSION', '100')
        
        # AFS SOAP Configuration
        self.AFS_SOAP_USERNAME = os.environ.get('AFS_SOAP_USERNAME', 'gphkdm')
        self.AFS_SOAP_P12_FILE = os.environ.get(
            'AFS_SOAP_P12_FILE',
            './resources/SOAP_PROD/gphkdm.p12'
        )
        self.AFS_SOAP_P12_PASSWORD = os.environ.get('AFS_SOAP_P12_PASSWORD', '')
        self.AFS_SOAP_WSDL = os.environ.get(
            'AFS_SOAP_WSDL',
            'https://ics2ws.ic3.com/commerce/1.x/transactionProcessor/CyberSourceTransaction_NVP_1.211.wsdl'
        )
        
        # Set API endpoints based on environment
        self._set_endpoints()
        
        # SOAP Username
        self.SOAP_USERNAME = self.MERCHANT_ID
    
    def _load_merchant_config(self) -> None:
        """Load merchant-specific configuration from environment variables."""
        # Build config key from merchant ID and environment
        config_prefix = f"{self.MERCHANT_ID}_{self.ENVIRONMENT}_"
        
        # Load merchant configuration
        self.MERCHANT_KEY_ID = os.environ.get(f'{config_prefix}MERCHANT_KEY_ID', '')
        self.MERCHANT_SECRET_KEY = os.environ.get(f'{config_prefix}MERCHANT_SECRET_KEY', '')
        self.SA_PROFILE_ID = os.environ.get(f'{config_prefix}SA_PROFILE_ID', '')
        self.SA_ACCESS_KEY = os.environ.get(f'{config_prefix}SA_ACCESS_KEY', '')
        self.SA_SECRET_KEY = os.environ.get(f'{config_prefix}SA_SECRET_KEY', '')
        self.SOP_PROFILE_ID = os.environ.get(f'{config_prefix}SOP_PROFILE_ID', '')
        self.SOP_ACCESS_KEY = os.environ.get(f'{config_prefix}SOP_ACCESS_KEY', '')
        self.SOP_SECRET_KEY = os.environ.get(f'{config_prefix}SOP_SECRET_KEY', '')
        
        # SOAP Configuration
        self.SOAP_P12_FILE = os.environ.get(
            f'{config_prefix}SOAP_P12_FILE',
            f'./resources/SOAP_{self.ENVIRONMENT}/{self.MERCHANT_ID}.p12'
        )
        self.SOAP_P12_PASSWORD = os.environ.get(f'{config_prefix}SOAP_P12_PASSWORD', '')
        self.SOAP_PASSWORD = os.environ.get(f'{config_prefix}SOAP_PASSWORD', '')
        
        # Validate that P12 file exists if SOAP is being used
        if self.SOAP_P12_FILE and not Path(self.SOAP_P12_FILE).exists():
            raise ConfigError(
                f"SOAP P12 file not found: {self.SOAP_P12_FILE}. "
                f"Please check the path or set {config_prefix}SOAP_P12_FILE correctly."
            )
    
    def _set_endpoints(self) -> None:
        """Set API endpoints based on environment."""
        if self.ENVIRONMENT == "PROD":
            self.API_ENDPOINT = "api.cybersource.com"
            self.SA_URL = 'https://secureacceptance.cybersource.com/pay'
            self.SA_CREATE_TOKEN_URL = 'https://secureacceptance.cybersource.com/token/create'
            self.SA_UPDATE_TOKEN_URL = 'https://secureacceptance.cybersource.com/token/update'
            self.SOP_URL = 'https://secureacceptance.cybersource.com/silent/embedded/pay'
            self.SOP_CREATE_TOKEN_URL = 'https://secureacceptance.cybersource.com/silent/token/create'
            self.SOAP_WSDL = 'https://ics2ws.ic3.com/commerce/1.x/transactionProcessor/CyberSourceTransaction_NVP_1.211.wsdl'
        else:
            self.API_ENDPOINT = "apitest.cybersource.com"
            self.SA_URL = 'https://testsecureacceptance.cybersource.com/pay'
            self.SA_CREATE_TOKEN_URL = 'https://testsecureacceptance.cybersource.com/token/create'
            self.SA_UPDATE_TOKEN_URL = 'https://testsecureacceptance.cybersource.com/token/update'
            self.SOP_URL = 'https://testsecureacceptance.cybersource.com/silent/embedded/pay'
            self.SOP_CREATE_TOKEN_URL = 'https://testsecureacceptance.cybersource.com/silent/token/create'
            self.SOAP_WSDL = 'https://ics2wstest.ic3.com/commerce/1.x/transactionProcessor/CyberSourceTransaction_NVP_1.211.wsdl'
    
    def get_merchant_config_dict(self) -> Dict[str, Any]:
        """
        Get merchant configuration as a dictionary for backward compatibility.
        This maintains compatibility with existing code that expects config attributes.
        """
        return {
            'MERCHANT_KEY_ID': self.MERCHANT_KEY_ID,
            'MERCHANT_SECRET_KEY': self.MERCHANT_SECRET_KEY,
            'SA_PROFILE_ID': self.SA_PROFILE_ID,
            'SA_ACCESS_KEY': self.SA_ACCESS_KEY,
            'SA_SECRET_KEY': self.SA_SECRET_KEY,
            'SOP_PROFILE_ID': self.SOP_PROFILE_ID,
            'SOP_ACCESS_KEY': self.SOP_ACCESS_KEY,
            'SOP_SECRET_KEY': self.SOP_SECRET_KEY,
            'SOAP_P12_FILE': self.SOAP_P12_FILE,
            'SOAP_P12_PASSWORD': self.SOAP_P12_PASSWORD,
            'SOAP_PASSWORD': self.SOAP_PASSWORD,
        }
    
    def validate(self) -> None:
        """
        Validate configuration completeness.
        Raises ConfigError if critical configuration is missing.
        """
        if not self.MERCHANT_KEY_ID or not self.MERCHANT_SECRET_KEY:
            raise ConfigError(
                f"Merchant credentials not configured for {self.MERCHANT_ID} in {self.ENVIRONMENT} environment. "
                f"Please set {self.MERCHANT_ID}_{self.ENVIRONMENT}_MERCHANT_KEY_ID and "
                f"{self.MERCHANT_ID}_{self.ENVIRONMENT}_MERCHANT_SECRET_KEY"
            )


# WS-Security XML Namespace Definitions (unchanged, no secrets)
XML_NAMESPACES = {
    'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
    'wsse': 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd',
    'wsu': 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd',
    'ds': 'http://www.w3.org/2000/09/xmldsig#'
}

# WS-Security Algorithm Definitions (unchanged, no secrets)
XML_ALGORITHMS = {
    'c14n': 'http://www.w3.org/2001/10/xml-exc-c14n#',
    'sha256': 'http://www.w3.org/2001/04/xmldsig-more#rsa-sha256',
    'digest': 'http://www.w3.org/2001/04/xmlenc#sha256',
    'encoding': 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary',
    'x509': 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-x509-token-profile-1.0#X509v3'
}
