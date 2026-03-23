import urllib.request
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os

SITE_URL     = "https://d2eehadi.pythonanywhere.com"
FROM_EMAIL   = "haadii.ali.2007@gmail.com"
TO_EMAIL     = "haadii.ali.2007@gmail.com"
APP_PASSWORD = os.environ["APP_PASSWORD"]

def check_site():
    try:
        response = urllib.request.urlopen(SITE_URL, timeout=10)
        return response.status, None
    except urllib.error.HTTPError as e:
        return e.code, str(e)
    except Exception as e:
        return 0, str(e)

def send_alert(status, error):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    body = f"""
Site Monitor Alert
==================
Time:   {now}
Site:   {SITE_URL}
Status: {status}
Error:  {error}
"""
    msg = MIMEText(body)
    msg["Subject"] = f"Site Down [{status}]"
    msg["From"]    = FROM_EMAIL
    msg["To"]      = TO_EMAIL
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(FROM_EMAIL, APP_PASSWORD)
        smtp.send_message(msg)
    print(f"{datetime.now()} - Alert sent")

def main():
    status, error = check_site()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if status < 400:
        print(f"{now} - OK: site is up")
    else:
        print(f"{now} - DOWN: {status}")
        send_alert(status, error)

if __name__ == "__main__":
    main()
