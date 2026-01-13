import psycopg2
import pandas as pd
import numpy as np

# --- CONFIGURATION (UPDATED WITH YOUR CREDENTIALS) ---
DB_HOST = "localhost"
DB_NAME = "rasa_db"      # Matched from your tracker_store
DB_USER = "rasa_user"    # Matched from your tracker_store
DB_PASS = "rootadmin"    # Matched from your tracker_store
DB_PORT = "5432"

SQL_FILE = "wbauthusers.sql"
CSV_FILE = "wbauthusers DATA 4 roll numbers.csv"

def setup_database():
    try:
        # 1. Connect to PostgreSQL
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )
        conn.autocommit = True
        cursor = conn.cursor()
        print(f"✅ Connected to database '{DB_NAME}' successfully.")

        # 2. Create Table (Run the SQL file)
        with open(SQL_FILE, 'r') as f:
            sql_commands = f.read()
            cursor.execute(sql_commands)
            print("✅ Table 'wbauthusers' created successfully.")

        # 3. Load and Clean CSV Data
        df = pd.read_csv(CSV_FILE)
        
        # Replace NaN (Not a Number) with None for SQL NULL compatibility
        df = df.replace({np.nan: None})
        
        # 4. Insert Data
        print(f"⏳ Inserting {len(df)} user records...")
        
        insert_query = """
        INSERT INTO wbauthusers (
            userid, loginname, hashpwd, fullname, usercatid, 
            pwdexpirydate, isactive, intramailid, internetmailid, 
            isdeleted, email_otp, otp_expiry, password_reset_token, 
            token_expiry, last_pwd_reset_at
        ) VALUES (
            %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, 
            %s, %s, %s, %s, 
            %s, %s
        )
        ON CONFLICT (userid) DO NOTHING;
        """

        for index, row in df.iterrows():
            cursor.execute(insert_query, (
                row['userid'], row['loginname'], row['hashpwd'], row['fullname'], row['usercatid'],
                row['pwdexpirydate'], row['isactive'], row['intramailid'], row['internetmailid'],
                row['isdeleted'], row['email_otp'], row['otp_expiry'], row['password_reset_token'],
                row['token_expiry'], row['last_pwd_reset_at']
            ))

        print("✅ Data import complete!")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    setup_database()