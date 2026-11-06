import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'app-alumnos-secret-key-2026-clean-architecture')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DATABASE_PATH = os.getenv('DATABASE_PATH', str(BASE_DIR / 'bdalumnos.db'))
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', str(BASE_DIR / 'static' / 'uploads'))
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
    
    # Credenciales por defecto del Administrador (Modificables al levantar la app por primera vez)
    ADMIN_NOMBRE = os.getenv('ADMIN_NOMBRE', 'Administrador Principal')
    ADMIN_CORREO = os.getenv('ADMIN_CORREO', 'admin@appalumnos.com')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')
    
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    
    WHATSAPP_API_URL = os.getenv('WHATSAPP_API_URL', '')
    WHATSAPP_API_TOKEN = os.getenv('WHATSAPP_API_TOKEN', '')
    
    NOTIFICATIONS_MOCK = os.getenv('NOTIFICATIONS_MOCK', 'True').lower() in ('true', '1', 't')
