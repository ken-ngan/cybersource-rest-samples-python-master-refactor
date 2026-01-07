"""
Database utility functions.
Uses centralized Supabase client from db_client module.
"""
from db_client import get_supabase_client

# Get Supabase client from centralized module
supabase = get_supabase_client()

def get_users():
    """
    Example of a SELECT query:
    Equivalent to 'SELECT * FROM users'
    """
    try:
        response = supabase.table("users").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error fetching users: {e}")
        return None

def add_user(username, email):
    """
    Example of an INSERT query:
    Equivalent to 'INSERT INTO users (username, email) VALUES (...)'
    """
    try:
        data = {"username": username, "email": email}
        response = supabase.table("users").insert(data).execute()
        return response.data
    except Exception as e:
        print(f"Error adding user: {e}")
        raise e

if __name__ == "__main__":
    # Test connection by fetching data from a table
    try:
        # Simplest connectivity test
        supabase.table("users").select("count", count="exact").limit(1).execute()
        print("✅ Supabase Library connection successful!")
    except Exception as e:
        print(f"❌ connection failed: {e}")