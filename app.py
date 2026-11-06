import os
import sys
import subprocess
import webbrowser
import sqlite3
from threading import Timer
from werkzeug.security import generate_password_hash

REQUIRED_PACKAGES = ["Flask", "Werkzeug", "reportlab", "openpyxl", "requests", "python-dotenv"]

def check_and_install_dependencies():
    missing_packages = []
    for pkg in REQUIRED_PACKAGES:
        try:
            __import__(pkg.lower().replace("-", "_"))
        except ImportError:
            missing_packages.append(pkg)
    
    if missing_packages:
        print(f"[AppAlumnos] Instalando dependencias faltantes: {missing_packages}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)

check_and_install_dependencies()

from flask import Flask
from config import Config
from infrastructure.database.db import check_db_exists, close_db
from infrastructure.web.auth import auth_bp
from infrastructure.web.dashboard import dashboard_bp
from infrastructure.web.alumnos import alumnos_bp
from infrastructure.web.profesores import profesores_bp
from infrastructure.web.ofertas import ofertas_bp
from infrastructure.web.catalogos import catalogos_bp
from infrastructure.web.inscripciones import inscripciones_bp
from infrastructure.web.reportes import reportes_bp

def seed_default_admin():
    db_path = Config.DATABASE_PATH
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT Id FROM tbl_usuarios WHERE Correo = ?", (Config.ADMIN_CORREO,))
    row = cursor.fetchone()
    
    if not row:
        contrasena_hash = generate_password_hash(Config.ADMIN_PASSWORD)
        cursor.execute("""
            INSERT INTO tbl_usuarios (Nombre, Correo, Contrasena, Tipo_Usuario, Estatus)
            VALUES (?, ?, ?, ?, ?)
        """, (Config.ADMIN_NOMBRE, Config.ADMIN_CORREO, contrasena_hash, "administrador", "Activo"))
        conn.commit()
        print("\n" + "="*55)
        print(" [AppAlumnos] CUENTA DE ADMINISTRADOR CREADA:")
        print(f" Correo:     {Config.ADMIN_CORREO}")
        print(f" Contraseña: {Config.ADMIN_PASSWORD}")
        print("="*55 + "\n")
    conn.close()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    check_db_exists()
    seed_default_admin()
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(alumnos_bp)
    app.register_blueprint(profesores_bp)
    app.register_blueprint(ofertas_bp)
    app.register_blueprint(catalogos_bp)
    app.register_blueprint(inscripciones_bp)
    app.register_blueprint(reportes_bp)

    app.teardown_appcontext(close_db)

    return app

application = create_app()

def open_browser():
    try:
        webbrowser.open_new('http://127.0.0.1:5000/')
        if sys.platform == "win32":
            import pygetwindow as gw
            import time
            time.sleep(1)
            wins = gw.getWindowsWithTitle('AppAlumnos')
            if wins:
                wins[0].maximize()
    except Exception:
        pass

if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        Timer(1.5, open_browser).start()
    application.run(host='127.0.0.1', port=5000, debug=True)
