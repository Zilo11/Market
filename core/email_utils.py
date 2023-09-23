import smtplib
from email.message import EmailMessage

def send_mail(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['To'] = to
    
    user = "zilopostmarket@gmail.com"
    msg['From'] = user
    password = "wnib jpua jhps pxfx" 
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    
    server.quit()