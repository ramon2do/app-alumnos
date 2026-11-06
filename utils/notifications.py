import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Notifications")
def enviar_correo(dest, asunto, msg): logger.info(f"[MAIL MOCK] Para: {dest} | Asunto: {asunto}\n{msg}")
def enviar_whatsapp(num, msg): logger.info(f"[WHATSAPP MOCK] Para: {num} | {msg}")
