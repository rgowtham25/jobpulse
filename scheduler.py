# schedule.py

import schedule
import time
from scrapers.google_job_scraper import fetch_job_links
from notifier.whatsapp_sender import send_whatsapp_message

def job():
    ROLE = "Data Analyst"
    LOCATION = "Bangalore"
    TIME_FILTER = "h"
    MAX_PAGES = 3

    job_links = fetch_job_links(ROLE, LOCATION, TIME_FILTER, MAX_PAGES)

    if job_links:
        print(f"📬 Sending {len(job_links)} job links via WhatsApp...")
        send_whatsapp_message(job_links)
    else:
        print("❌ No new job links found.")

# ✅ Run once immediately
job()

# 🕒 Then schedule every hour
schedule.every(1).hours.do(job)

print("🔁 Scheduler started. First run sent. Next in 1 hour...\n")
while True:
    schedule.run_pending()
    time.sleep(1)
