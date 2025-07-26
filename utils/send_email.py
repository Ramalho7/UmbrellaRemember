import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
from models.model import User, engine, City, State
from sqlalchemy.orm import sessionmaker, joinedload


load_dotenv()

DBSession = sessionmaker(bind=engine)

def get_smtp_config():
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
    smtp_user = os.getenv('SMTP_USER')
    smtp_password = os.getenv('SMTP_PASSWORD')
    return smtp_server, smtp_port, smtp_user, smtp_password

def send_email(subject, html_body, recipient):
    
    smtp_server, smtp_port, smtp_user, smtp_password = get_smtp_config()
    
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(html_body, 'html'))
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, recipient, msg.as_string())
    except Exception as e:
            print(f"Erro ao enviar e-mail para {recipient}: {e}")
    
        