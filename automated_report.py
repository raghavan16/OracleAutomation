import oracledb
import pandas as pd
import matplotlib.pyplot as plt
from google import genai
import os
import smtplib
from email.message import EmailMessage

# --- 1. SETUP ---
# For now, paste your key here. Next, I'll show you how to hide it.
###API_KEY = "AIzaSyAkBhYxYBlMwRjTL6zgDDhR0Qjtyq_CTkA" 
###client = genai.Client(api_key=API_KEY)

# Instead of hardcoding, we "fetch" it from the Mac System
api_key_from_mac = os.environ.get("GEMINI_API_KEY")

# Now use that variable to start the AI client
client = genai.Client(api_key=api_key_from_mac)

# --- 2. DATA LAYER (The "Extract" part) ---

def get_data():
    try:
        # (Your Oracle code remains here...)
        pass 
    except Exception as e:
        print(f"Action: Falling back to 'production_stats.csv'...")
        df = pd.read_csv('production_stats.csv')
        
        # --- ADD THIS CLEANING STEP ---
        # This removes spaces and makes everything UPPERCASE
        df.columns = [c.strip().upper() for c in df.columns]
        
        return df

    try:
        print("Attempting to connect to Oracle Database...")
        # Establishing the connection (The 'Handshake')
        with oracledb.connect(user=user, password=pw, dsn=dsn) as connection:
            print("Database Connection Successful!")
            
            # The SQL Query (Your 'SELECT' statement)
            sql_query = "SELECT SERVICE_NAME, SUCCESS_RATE FROM PRODUCTION_STATS"
            
            # Read directly into a Pandas DataFrame
            df = pd.read_sql(sql_query, con=connection)
            return df

    except Exception as e:
        print(f"Oracle Error: {e}")
        print("Action: Falling back to 'production_stats.csv' to ensure report continuity.")
        return pd.read_csv('production_stats.csv')

# --- 3. VISUALIZATION LAYER (The "Transform" part) ---
def create_graph(df):
    plt.figure(figsize=(10, 6))
    plt.bar(df['Service_Name'], df['Success_Rate'], color='skyblue')
    plt.title('Daily Production Support Performance')
    plt.axhline(y=95, color='r', linestyle='--', label='SLA Target (95%)')
    plt.ylim(0, 105) # Keeps the scale consistent
    plt.legend()
    
    graph_filename = "report_graph.png"
    plt.savefig(graph_filename)
    plt.close()
    return graph_filename

# --- 4. GEN AI LAYER (The "Intelligence" part) ---
def generate_ai_summary(df):
    data_string = df.to_string(index=False)
    
    prompt = f"""
    You are a Senior Production Support Lead. 
    Analyze this daily success rate data:
    {data_string}
    
    Write a concise 2-sentence executive summary for a management email. 
    Identify which service failed the 95% SLA and suggest a likely mainframe-related cause.
    """
    
    # This calls the actual Google Gemini model
    response = client.models.generate_content(
      ###model="gemini-1.5-flash",
      model="gemini-flash-latest",
        contents=prompt
    )
    return response.text
def send_email_report(summary_text, image_path):
    # 1. Fetch credentials from Mac environment
    sender_email = os.environ.get("EMAIL_USER")
    sender_pass = os.environ.get("EMAIL_PASS")
    recipient_email = sender_email  # Sending to yourself for now

    # 2. Build the Email 'Package'
    msg = EmailMessage()
    msg['Subject'] = 'Production Support AI Report - SLA Alert'
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg.set_content(f"Hello Team,\n\nHere is the automated AI analysis of our production stats:\n\n{summary_text}")

    # 3. Attach the Graph Image
    with open(image_path, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='image', subtype='png', filename='report_graph.png')

    # 4. Connect to the 'Mailroom' and Send
    try:
        # For Gmail, the server is smtp.gmail.com on port 465
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_pass)
            smtp.send_message(msg)
            print("Step 4: Email Sent Successfully!")
    except Exception as e:
        print(f"Step 4 Error: Failed to send email. {e}")


# --- 5. EXECUTION (The "Main Line") ---
if __name__ == "__main__":
    try:
        print("Step 1: Fetching Data...")
        df_results = get_data()

        print("Step 2: Creating Graph...")
        path_to_image = create_graph(df_results)

        print("Step 3: Generating AI Summary...")
        real_summary = generate_ai_summary(df_results)

        print("\n" + "="*40)
        print("FINAL REPORT SUMMARY")
        print("="*40)
        print(real_summary)
        print("="*40)

        # New Step: Email the results
        print("Step 4: Emailing Report...")
        send_email_report(real_summary, path_to_image)

        print("\nProcess Complete!")

    except Exception as e:
        print(f"An error occurred: {e}")


 ######       hnfx pspv mlhf xfdz