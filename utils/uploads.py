import os
import secrets
from werkzeug.utils import secure_filename
from flask import current_app

def guardar_archivo(file, tipo_doc: str) -> str:
    if not file or file.filename == '': return ''
    original_filename = secure_filename(file.filename)
    ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'bin'
    
    random_code = secrets.token_hex(8)
    unique_name = f"{random_code}_{tipo_doc}.{ext}"
    
    os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name)
    file.save(filepath)
    return f"/static/uploads/{unique_name}"
