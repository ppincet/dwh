'''
logger implementation
'''
from pathlib import Path
from logging.handlers import RotatingFileHandler
import logging
import smtplib
import sys
from email.message import EmailMessage

def send_emergency_alert(error_text: str):
    SMTP_SERVER = "smtp.example.com"
    SMTP_PORT = 587
    SMTP_USER = "user@example.com"
    SMTP_PASSWORD = "your_password"
    ADMIN_EMAIL = "admin@example.com"

    try:
        msg = EmailMessage()
        msg.set_content(error_text)
        msg["Subject"] = "[FATAL CRASH] Engine CLI: fatal crash"
        msg["From"] = SMTP_USER
        msg["To"] = ADMIN_EMAIL

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            
    except Exception as mail_err:
        print(f"FATAL: Не удалось отправить аварийный email: {mail_err}", file=sys.stderr)

audit_logger = logging.getLogger("ETLAuditLogger")
audit_logger.setLevel(logging.INFO)
audit_logger.propagate = False 

handler = RotatingFileHandler(
    filename=f'{Path(__file__).resolve().parent.parent.parent}/logs/etl_audit.log', 
    maxBytes=5 * 1024 * 1024, # 5 MB
    backupCount=5, 
    encoding="utf-8"
)

formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [Session: %(session_id)s] [%(task_name)s -> %(step_name)s]: %(message)s')
handler.setFormatter(formatter)
audit_logger.addHandler(handler)
