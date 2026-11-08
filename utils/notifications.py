import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import requests
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Notifications")

def enviar_correo(dest, asunto, msg):
    """Envía un correo electrónico real vía SMTP o hace un mock si faltan credenciales"""
    if not Config.MAIL_USERNAME or not Config.MAIL_PASSWORD:
        logger.info(f"[MAIL MOCK] Para: {dest} | Asunto: {asunto}\n{msg}")
        return

    try:
        mensaje = MIMEMultipart()
        # Puedes usar MAIL_FROM si deseas un remitente distinto al usuario logueado (sujeto a restricciones SMTP)
        remitente = getattr(Config, 'MAIL_FROM', None) or Config.MAIL_USERNAME
        mensaje['From'] = remitente
        mensaje['To'] = dest
        mensaje['Subject'] = asunto
        
        mensaje.attach(MIMEText(msg, 'plain'))

        servidor = smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT)
        servidor.starttls()
        servidor.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
        
        servidor.sendmail(remitente, dest, mensaje.as_string())
        servidor.quit()
        
        logger.info(f"[MAIL] Correo enviado exitosamente a {dest}")
    except Exception as e:
        logger.error(f"[MAIL ERROR] No se pudo enviar el correo a {dest}: {e}")

def enviar_whatsapp(num, msg):
    """Envía un mensaje de WhatsApp utilizando la API de Whapi.cloud"""
    if Config.NOTIFICATIONS_MOCK:
        logger.info(f"[WHATSAPP MOCK] Para: {num} | {msg}")
        return

    # Limpia el número quitando caracteres no numéricos (+, -, espacios)
    numero_limpio = "".join(filter(str.isdigit, str(num)))

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {Config.WHATSAPP_API_TOKEN}"
    }

    payload = {
        "to": numero_limpio,
        "body": msg
    }

    try:
        response = requests.post(Config.WHATSAPP_API_URL, json=payload, headers=headers, timeout=10)
        if response.status_code in (200, 201):
            logger.info(f"[WHATSAPP] Mensaje enviado con éxito a {numero_limpio}")
        else:
            logger.error(f"[WHATSAPP ERROR] Status: {response.status_code} | Response: {response.text}")
    except Exception as e:
        logger.error(f"[WHATSAPP EXCEPTION] Error al enviar mensaje: {e}")