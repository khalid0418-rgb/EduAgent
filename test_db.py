import os
from dotenv import load_dotenv
from supabase import create_client, Client

# 1. LOAD ENVIRONMENT VARIABLES
# This looks for your .env file and reads the URL and Key
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

def test_connection():
    # Check if variables were actually loaded
    if not url or not key:
        print("❌ Error: SUPABASE_URL or SUPABASE_KEY not found in .env file.")
        return

    try:
        # 2. INITIALIZE CLIENT
        supabase: Client = create_client(url, key)
        print("✅ Client initialized successfully.")

        # 3. RUN WRITE TEST
        print("Attempting to write test data to 'profiles' table...")
        
        test_data = {
            "email": "test@example.com",
            "biz_name": "Test Robotics Hub",
            "biz_niche": "STEM Education",
            "target_audience": "Parents"
        }

        # upsert means: "Update if exists, otherwise Insert"
        response = supabase.table("profiles").upsert(test_data).execute()
        
        print("✅ Write Test Successful! Data saved to Supabase.")
        print(f"Response Data: {response.data}")

    except Exception as e:
        print("❌ Database Test Failed.")
        print(f"Error Details: {e}")

# This ensures the code only runs when you call 'python3 test_db.py'
if __name__ == "__main__":
    test_connection()
