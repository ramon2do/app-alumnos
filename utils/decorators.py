from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            flash("Debe iniciar sesión para acceder al sistema.", "warning")
            return redirect(url_for('auth.login'))
        
        # Permitir acceso si es administrador u operador
        tipo_usuario = session['usuario'].get('tipo_usuario')
        if tipo_usuario not in ['administrador', 'operador']:
            flash("No tienes permisos suficientes para acceder a esta sección.", "danger")
            return redirect(url_for('dashboard.index'))
            
        return f(*args, **kwargs)
    return decorated_function