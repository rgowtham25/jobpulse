# whatsapp_sender.py 

from twilio.rest import Client
import os

# 🔒 Set your credentials (or load from environment variables)
TWILIO_ACCOUNT_SID = "ACe85de827b0eba12fd4f2ca1a211ef98c"
TWILIO_AUTH_TOKEN = "2bc4e8a6ddf9f0918d4031e9ae9fbefb"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Twilio Sandbox number
RECIPIENT_NUMBER = "whatsapp:+919750257792"       # Your number (must be verified in sandbox)

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_whatsapp_message(job_links):
    if not job_links:
        return

    message_text = "🔔 New Job Postings:\n\n"
    for title, link in job_links:
        message_text += f"📌 {title}\n🔗 {link}\n\n"

    try:
        message = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            to=RECIPIENT_NUMBER,
            body=message_text.strip()
        )
        print(f"✅ WhatsApp message sent! SID: {message.sid}")
    except Exception as e:
        print(f"❌ Failed to send message: {e}")


def send_whatsapp_message_custom(job_links, recipient_number):
    if not job_links:
        return False

    message_text = "🔔 New Job Postings:\n\n"
    for title, link in job_links:
        message_text += f"📌 {title}\n🔗 {link}\n\n"

    try:
        message = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            to=f"whatsapp:{recipient_number}",
            body=message_text.strip()
        )
        print(f"✅ WhatsApp message sent to {recipient_number}! SID: {message.sid}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
