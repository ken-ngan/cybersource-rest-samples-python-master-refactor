"""
Centralized database client initialization.
Provides a single source of truth for Supabase client configuration.
"""
import os
from typing import Optional
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase Client with environment variables
SUPABASE_URL: str = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY", "")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "SUPABASE_URL and SUPABASE_KEY must be set in environment variables. "
        "Please check your .env file or environment configuration."
    )

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_supabase_client() -> Client:
    """
    Get the initialized Supabase client.
    
    Returns:
        Client: The Supabase client instance
        
    Raises:
        ValueError: If Supabase credentials are not configured
    """
    if not supabase:
        raise ValueError("Supabase client not initialized. Check SUPABASE_URL and SUPABASE_KEY.")
    return supabase
