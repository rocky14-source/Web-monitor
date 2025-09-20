import requests
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ===== CONFIG =====
URL = "https://www.simplecirc.com/subscribe/s-magazine"   # page to monitor
SEARCH_TEXT = "AMAZON e-GIFT CARD SOLD OUT"              # text to watch for
STATE_FILE = "last_state.txt"

EMAIL_FROM = "rocky14indian@gmail.com"
EMAIL_TO = "rocky14indian@gmail.com"
EMAIL_PASSWORD = os.environ.get("rtwn yski dcao ufqq")  # from GitHub Secrets
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
# ==================

def get_page_content():
    r = requests.get(URL, timeout=10)
    r.raise_for_status()
    return r.text

def send_email():
    subject = f"Product Update: {URL}"
    body = f"The product status has changed!\nCheck here: {URL}"

    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)

def main():
    content = get_page_content()

    # Check if "Sold Out" is in page
    current_state = "SOLD_OUT" if SEARCH_TEXT.lower() in content.lower() else "AVAILABLE"

    # Read last known state
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            last_state = f.read().strip()
    else:
        last_state = ""

    # Detect change
    if current_state != last_state:
        if last_state == "SOLD_OUT" and current_state == "AVAILABLE":
            send_email()
        with open(STATE_FILE, "w") as f:
            f.write(current_state)

if __name__ == "__main__":
    main()
