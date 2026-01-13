# import os
# import psycopg2
# import yaml
# import subprocess
# import google.generativeai as genai
# from dotenv import load_dotenv
# from pathlib import Path
# import time

# # --- CONFIGURATION ---
# env_path = Path(__file__).parent / ".env"
# load_dotenv(dotenv_path=env_path)

# api_key = os.getenv("GKEY")
# if not api_key:
#     # Hardcoded backup just in case
#     api_key = "AIzaSyAKS2mPV9OludY136Kxezd189AP79cVnH0" 

# os.environ["GOOGLE_API_KEY"] = api_key
# genai.configure(api_key=api_key)

# DB_CONFIG = {
#     "host": os.getenv("DB_HOST", "localhost"),
#     "database": os.getenv("DB_NAME", "rasa_db"),
#     "user": os.getenv("DB_USER", "rasa_user"),
#     "password": os.getenv("DB_PASS", "rootadmin"),
#     "port": os.getenv("DB_PORT", "5432")
# }

# NLU_FILE_PATH = "data/nlu.yml"

# def get_existing_intents():
#     try:
#         with open(NLU_FILE_PATH, 'r', encoding='utf-8') as f:
#             nlu_data = yaml.safe_load(f)
#     except FileNotFoundError:
#         print(f"Error: {NLU_FILE_PATH} not found.")
#         return [], {}
    
#     intents = [item['intent'] for item in nlu_data.get('nlu', []) if 'intent' in item]
#     return intents, nlu_data

# def classify_message_with_retry(message, existing_intents):
#     """Tries to classify, and waits/retries if API limit is hit"""
    
#     intent_list_str = ", ".join(existing_intents)
#     prompt = f"""
#     Act as a Data Labeling Expert for a Rasa chatbot.
#     User message: "{message}"
#     Valid intents: [{intent_list_str}]
    
#     Task: Match the message to ONE existing intent. If it fits none or is spam, output "nlu_fallback".
#     Output format: Just the intent name.
#     """
    
#     # Retry up to 3 times
#     for attempt in range(3):
#         try:
#             # Re-init config to be safe
#             genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
#             model = genai.GenerativeModel('gemini-2.5-flash')
            
#             response = model.generate_content(prompt)
#             predicted_intent = response.text.strip()
            
#             if predicted_intent in existing_intents:
#                 return predicted_intent
#             return "nlu_fallback"
            
#         except Exception as e:
#             if "429" in str(e):
#                 wait_time = 60  # Wait 1 minute if quota exceeded
#                 print(f"   ⏳ Quota hit. Pausing for {wait_time}s before retry {attempt + 1}/3...")
#                 time.sleep(wait_time)
#                 continue # Try again
#             else:
#                 print(f"   ⚠️ Error: {e}")
#                 return "nlu_fallback"
                
#     return "nlu_fallback" # Give up after retries

# def update_nlu_file(new_data):
#     with open(NLU_FILE_PATH, 'a', encoding='utf-8') as f:
#         f.write("\n") 
#         for intent, examples in new_data.items():
#             print(f"📝 Adding {len(examples)} new examples to intent: {intent}")
#             f.write(f"# Auto-added examples for {intent}\n")
#             f.write(f"- intent: {intent}\n")
#             f.write("  examples: |\n")
#             for ex in examples:
#                 f.write(f"    - {ex}\n")
#             f.write("\n")

# def main():
#     print("🚀 Starting Auto-Train Pipeline (Auto-Retry Mode)...")
    
#     try:
#         conn = psycopg2.connect(**DB_CONFIG)
#         cursor = conn.cursor()
#     except Exception as e:
#         print(f"❌ Database connection failed: {e}")
#         return

#     # Process 5 at a time to be safe
#     cursor.execute("SELECT id, user_message FROM fallback_logs WHERE is_trained = FALSE LIMIT 5")
#     rows = cursor.fetchall()
    
#     if not rows:
#         print("✅ No new fallbacks to train.")
#         conn.close()
#         return

#     intents, _ = get_existing_intents()
#     new_training_data = {} 
#     processed_ids = []

#     print(f"🔍 Processing {len(rows)} messages...")

#     for row_id, message in rows:
#         # Standard small delay between requests
#         time.sleep(2)
        
#         predicted_intent = classify_message_with_retry(message, intents)
        
#         if predicted_intent and predicted_intent != 'nlu_fallback':
#             if predicted_intent not in new_training_data:
#                 new_training_data[predicted_intent] = []
#             new_training_data[predicted_intent].append(message)
#             processed_ids.append(row_id)
#             print(f"   👉 Mapped: '{message}' -> {predicted_intent}")
#         else:
#             processed_ids.append(row_id) # Mark as processed so we don't loop forever
#             print(f"   ⚠️ Skipped: '{message}' (Unclear/Spam)")

#     if new_training_data:
#         print("📂 Updating nlu.yml...")
#         update_nlu_file(new_training_data)
        
#         if processed_ids:
#             cursor.execute(
#                 "UPDATE fallback_logs SET is_trained = TRUE WHERE id = ANY(%s)", 
#                 (processed_ids,)
#             )
#             conn.commit()

#         print("🤖 Starting Rasa training...")
#         try:
#             subprocess.run(["rasa", "train"], check=True)
#             print("✅ Training complete! Please restart your Rasa server.")
#         except Exception as e:
#             print(f"❌ Training failed: {e}")
            
#     elif processed_ids:
#         # If we skipped everything (spam/irrelevant), still mark them as trained
#         cursor.execute(
#             "UPDATE fallback_logs SET is_trained = TRUE WHERE id = ANY(%s)", 
#             (processed_ids,)
#         )
#         conn.commit()
#         print("✅ Processed items (all were skipped). No training needed.")
    
#     conn.close()

# if __name__ == "__main__":
#     main()
#---------------------KISHAN AUTO TRAIN 19TH DEC 2026 UPDATE END-----------------------
import os
import psycopg2
import yaml
import subprocess
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path
import time
from datetime import datetime
import select # Required for waiting on DB events

# --- CONFIGURATION ---
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GKEY")
if not api_key:
    api_key = "AIzaSyAKS2mPV9OludY136Kxezd189AP79cVnH0" 

os.environ["GOOGLE_API_KEY"] = api_key
genai.configure(api_key=api_key)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "rasa_db"),
    "user": os.getenv("DB_USER", "rasa_user"),
    "password": os.getenv("DB_PASS", "rootadmin"),
    "port": os.getenv("DB_PORT", "5432")
}

NLU_FILE_PATH = "data/nlu.yml"

# ... [Keep your helper functions: get_existing_intents, classify_message_with_retry, update_nlu_file] ...
# (Paste the exact same helper functions from previous code here to keep file short for reading)
# Just ensure 'classify_message_with_retry' and others are defined above 'process_pending_logs'

def get_existing_intents():
    # ... (Same as before) ...
    try:
        with open(NLU_FILE_PATH, 'r', encoding='utf-8') as f:
            nlu_data = yaml.safe_load(f)
    except FileNotFoundError:
        return [], {}
    intents = [item['intent'] for item in nlu_data.get('nlu', []) if 'intent' in item]
    return intents, nlu_data

def classify_message_with_retry(message, existing_intents):
    # ... (Same as before) ...
    intent_list_str = ", ".join(existing_intents)
    prompt = f"Act as Data Labeling Expert. Message: '{message}'. Intents: [{intent_list_str}]. Output intent name only or 'nlu_fallback'."
    for attempt in range(3):
        try:
            genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            predicted = response.text.strip()
            return predicted if predicted in existing_intents else "nlu_fallback"
        except Exception as e:
            if "429" in str(e):
                time.sleep(60)
                continue
    return "nlu_fallback"

def update_nlu_file(new_data):
    # ... (Same as before) ...
    with open(NLU_FILE_PATH, 'a', encoding='utf-8') as f:
        f.write("\n") 
        for intent, examples in new_data.items():
            f.write(f"# Auto-added\n- intent: {intent}\n  examples: |\n")
            for ex in examples:
                f.write(f"    - {ex}\n")

def process_pending_logs():
    """Reads ALL pending logs and trains."""
    print(f"\n🚀 Trigger Received! Processing batch at {datetime.now().strftime('%H:%M:%S')}")
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # We fetch MORE rows now since we waited for 100
        cursor.execute("SELECT id, user_message FROM fallback_logs WHERE is_trained = FALSE LIMIT 200")
        rows = cursor.fetchall()
        
        if not rows:
            print("   False alarm: No rows found.")
            conn.close()
            return

        intents, _ = get_existing_intents()
        new_training_data = {} 
        processed_ids = []

        print(f"   🔍 Processing {len(rows)} messages...")

        for row_id, message in rows:
            time.sleep(2) # Still keep rate limit safe
            predicted_intent = classify_message_with_retry(message, intents)
            
            if predicted_intent and predicted_intent != 'nlu_fallback':
                if predicted_intent not in new_training_data:
                    new_training_data[predicted_intent] = []
                new_training_data[predicted_intent].append(message)
                processed_ids.append(row_id)
            else:
                processed_ids.append(row_id) # Mark spam as processed

        if new_training_data:
            print("   📂 Updating nlu.yml...")
            update_nlu_file(new_training_data)
            
            # Mark as trained
            cursor.execute("UPDATE fallback_logs SET is_trained = TRUE WHERE id = ANY(%s)", (processed_ids,))
            conn.commit()

            print("   🤖 Starting Rasa training...")
            subprocess.run(["rasa", "train"], check=True)
            print("   ✅ Training complete! New model ready.")
            
        elif processed_ids:
            cursor.execute("UPDATE fallback_logs SET is_trained = TRUE WHERE id = ANY(%s)", (processed_ids,))
            conn.commit()
            print("   ✅ Batch processed (all skipped).")
        
        conn.close()

    except Exception as e:
        print(f"❌ Error during processing: {e}")

if __name__ == "__main__":
    print(f"🎧 Listener Service Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("   - Waiting for PostgreSQL signal: 'start_auto_train'")
    print("   - Triggers when fallback count >= 10")

    conn = psycopg2.connect(**DB_CONFIG)
    # ISOLATION_LEVEL_AUTOCOMMIT is required for LISTEN to work asynchronously
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    
    cursor = conn.cursor()
    cursor.execute("LISTEN start_auto_train;") # Must match the SQL name

    while True:
        try:
            # select.select blocks until the database sends data (Efficient! No CPU usage)
            if select.select([conn], [], [], 60) == ([], [], []):
                # Timeout every 60s just to print a heartbeat (optional)
                # print(".", end="", flush=True) 
                pass
            else:
                conn.poll() # Read the event
                while conn.notifies:
                    notify = conn.notifies.pop(0)
                    print(f"\n🔔 Notification received from DB: {notify.channel}")
                    process_pending_logs()
                    
        except KeyboardInterrupt:
            print("\n🛑 Stopping Listener.")
            break
        except Exception as e:
            print(f"❌ Connection Error: {e}")
            time.sleep(5)
            # Reconnect logic would go here in production