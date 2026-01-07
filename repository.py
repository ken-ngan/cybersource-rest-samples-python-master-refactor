"""
Repository classes for database operations.
Uses centralized Supabase client from db_client module.
"""
from werkzeug.security import generate_password_hash
from db_client import get_supabase_client

# Get Supabase client from centralized module
supabase = get_supabase_client()

class UserRepository:
    @staticmethod
    def get_user_by_email(email):
        response = supabase.table("users").select("*").eq("email", email).maybe_single().execute()
        
        # Add this check to debug
        if response is None:
            print("❌ Critical Error: Supabase request returned None. Check your API URL and Key.")
            return None
            
        return response.data

    @staticmethod
    def create_user(email, password):
        hashed_pw = generate_password_hash(password, method="pbkdf2:sha256")
        data = {"email": email, "password": hashed_pw}
        response = supabase.table("users").insert(data).execute()
        return len(response.data)

class TokenRepository:
    @staticmethod
    def get_tokens_by_user_id(user_id):
        response = supabase.table("tokens")\
            .select("user_id, mid, payment_instrument_id, card_number, id, instrument_identifier_id")\
            .eq("user_id", user_id).execute()
        return response.data

    @staticmethod
    def get_token_by_id(token_id):
        response = supabase.table("tokens").select("*").eq("id", token_id).maybe_single().execute()
        return response.data

    @staticmethod
    def create_token(user_id, mid, transaction_id, payment_instrument_id, instrument_identifier_id, card_number):
        # Insert the new token
        data = {
            "user_id": user_id, 
            "mid": mid, 
            "transaction_id": transaction_id, 
            "payment_instrument_id": payment_instrument_id, 
            "instrument_identifier_id": instrument_identifier_id, 
            "card_number": card_number
        }
        insert_res = supabase.table("tokens").insert(data).execute()

        # # Deduplicate: In Supabase, it is safer to handle this via a Database Function (RPC) 
        # # or a simple secondary check. Here is a Python-side logic approach:
        # existing = supabase.table("tokens")\
        #     .select("id")\
        #     .eq("user_id", user_id)\
        #     .eq("instrument_identifier_id", instrument_identifier_id)\
        #     .order("id", desc=False).execute()
        
        # if len(existing.data) > 1:
        #     # Delete all but the latest (last) entry
        #     ids_to_delete = [item['id'] for item in existing.data[:-1]]
        #     supabase.table("tokens").delete().in_("id", ids_to_delete).execute()
            
        return len(insert_res.data)

    @staticmethod
    def delete_token(token_id):
        response = supabase.table("tokens").delete().eq("id", token_id).execute()
        return len(response.data)

class TransactionRepository:
    @staticmethod
    def get_transactions_by_user_id(user_id):
        response = supabase.table("transactions").select("*").eq("user_id", user_id).execute()
        return response.data

    @staticmethod
    def get_transaction_by_id(transaction_id):
        response = supabase.table("transactions").select("*").eq("id", transaction_id).maybe_single().execute()
        return response.data
            
    @staticmethod
    def get_transaction_by_reference(user_id, reference_number):
        response = supabase.table("transactions")\
            .select("*")\
            .eq("user_id", user_id)\
            .eq("reference_number", reference_number).execute()
        return response.data

    @staticmethod
    def create_transaction(user_id, mid, reference_number, transaction_id, amount, card_number, eci_raw, decision, reason_code, saved_token=None):
        data = {
            "user_id": user_id,
            "mid": mid,
            "reference_number": reference_number,
            "transaction_id": transaction_id,
            "amount": amount,
            "card_number": card_number,
            "eci_raw": eci_raw,
            "decision": decision,
            "reason_code": reason_code
        }
        if saved_token:
            data["saved_token"] = saved_token
            
        response = supabase.table("transactions").insert(data).execute()
        return len(response.data)

class TempTableRepository:
    @staticmethod
    def create_temp_session(logged_in, user_id, user_email, count_down_time, session_id):
        # Supabase doesn't have a single "DELETE then INSERT" atomic command in the client,
        # but you can chain them or use upsert.
        supabase.table("temp_table").delete().eq("user_id", user_id).execute()
        
        data = {
            "logged_in": logged_in,
            "user_id": user_id,
            "user_email": user_email,
            "count_down_time": count_down_time,
            "session_id": session_id
        }
        response = supabase.table("temp_table").insert(data).execute()
        return len(response.data)

    @staticmethod
    def get_temp_session(session_id):
        # Supabase returns a list of dicts by default, so we don't need the zip(columns) logic
        response = supabase.table("temp_table").select("*").eq("session_id", session_id).maybe_single().execute()
        return response.data
            
    @staticmethod
    def get_temp_session_by_reference(reference_number):
        response = supabase.table("temp_table").select("*").eq("reference_number", reference_number).maybe_single().execute()
        return response.data

    @staticmethod
    def delete_temp_session(session_id):
        response = supabase.table("temp_table").delete().eq("session_id", session_id).execute()
        return len(response.data)
            
    @staticmethod
    def delete_temp_session_by_user(user_id):
        response = supabase.table("temp_table").delete().eq("user_id", user_id).execute()
        return len(response.data)

    @staticmethod
    def update_temp_session(session_id, **kwargs):
        if not kwargs:
            return 0
        response = supabase.table("temp_table").update(kwargs).eq("session_id", session_id).execute()
        return len(response.data)