import os
import random
import string
import datetime
from supabase import create_client
from dotenv import load_dotenv
from email_utils import send_verification_email, send_password_reset_email

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

def generate_access_code(length=6):
    return ''.join(random.choices(string.digits, k=length))

def generate_Update_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def signup_user(email, password):
    access_code = generate_access_code()
    try:
        supabase.table("users").insert({
            "email": email,
            "password": password,
            "access_code": access_code,
            "is_verified": False
        }).execute()
        send_verification_email(email, access_code)
        return True, access_code
    except Exception as e:
        return False, str(e)

def verify_access_code(supabase, email, code):
    result = supabase.table("users").select("*").eq("email", email).execute()
    
    if not result.data:
        print("Email not found.")
        return False
    
    if result.data[0]["access_code"] != code:
        print("Incorrect code.")
        return False

    # If matched, update
    supabase.table("users").update({"is_verified": True}).eq("email", email).execute()
    print("User verified successfully.")
    return True


def login_user(email, password):
    result = supabase.table("users").select("*").eq("email", email).eq("password", password).eq("is_verified", True).execute()
    return result.data[0] if result.data else None

def update_password(email):
    result = supabase.table("users").select("*").eq("email", email).execute()
    if not result.data:
        return False, "Email not found."
    new_pass = generate_Update_code()
    supabase.table("users").update({"update_code": new_pass}).eq("email", email).execute()
    send_password_reset_email(email, new_pass)

    return True, new_pass

def self_password(email, code, new_password):
    # Check if the email exists
    result = supabase.table("users").select("*").eq("email", email).execute()
    if not result.data: 
        return False, "Email not found."
    supabase.table("users").update({"password": new_password}).eq("email", email).execute()
    return True, "Password updated successfully."


def verify_update_code(supabase, email, code, new_password):
    result = supabase.table("users").select("*").eq("email", email).execute()    
    if not result.data:
        print("Email not found.")
        return False
    if result.data[0]["update_code"] != code:
        print("Incorrect code.")
        return False
    # If matched, update
    supabase.table("users").update({"password": new_password}).eq("email", email).execute()
    print("Password updated successfully.")
    return True





