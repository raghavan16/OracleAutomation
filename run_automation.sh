#!/bin/bash
# Move to the project directory
cd /Users/raghavaraju/Desktop/OracleAutomation/

# Create a 'Start' marker in the log
echo "--- JOB START: $(date) ---" > cron_log.txt

# Activate the Virtual Environment
source my_env/bin/activate

# Fetch the API Key directly in the shell (Best Practice for Cron)
export GEMINI_API_KEY="YOUR_ACTUAL_API_KEY_HERE"
export EMAIL_USER="raghavagenai@gmail.com"
export EMAIL_PASS="hnfx pspv mlhf xfdz"
source my_env/bin/activate
/Users/raghavaraju/Desktop/OracleAutomation/my_env/bin/python3 automated_report.py >> cron_log.txt 2>&1

# Run the Python script and append (>>) the output
/Users/raghavaraju/Desktop/OracleAutomation/my_env/bin/python3 automated_report.py >> cron_log.txt 2>&1

echo "--- JOB END: $(date) ---" >> cron_log.txt