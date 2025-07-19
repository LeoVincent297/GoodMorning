import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(content, email, token, destinataire):
    """Envoie l'email avec les informations du jour"""
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = destinataire
    msg['Subject'] = "Info du jour"

    msg.attach(MIMEText(content, 'plain'))

    # Envoi de l'email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, token)
        server.send_message(msg)
        server.quit()
        print("Email envoyé avec succès!")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {str(e)}")