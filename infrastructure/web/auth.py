from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from infrastructure.container import container
from domain.identidad.exceptions.identidad_exceptions import IdentidadException
from domain.identidad.value_objects.email import Email
from domain.identidad.value_objects.rol import Rol
from domain.identidad.entities.usuario import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            dto = container.login_use_case().execute(request.form.get('correo'), request.form.get('contrasena'))
            session['usuario'] = {'id': dto.id, 'nombre': dto.nombre, 'correo': dto.correo, 'tipo_usuario': dto.tipo_usuario}
            flash(f"¡Bienvenido de nuevo, {dto.nombre}!", "success")
            return redirect(url_for('dashboard.index'))
        except IdentidadException as e: flash(str(e), "danger")
    return render_template('auth/login.html')

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre')
            correo = request.form.get('correo')
            contrasena = request.form.get('contrasena')
            
            # Validar si el correo ya existe
            if container.usuario_repo.buscar_por_correo(correo):
                flash("El correo electrónico ya está registrado.", "danger")
                return redirect(url_for('auth.registro'))
            
            # Crear usuario con rol operador por defecto
            contrasena_hash = generate_password_hash(contrasena)
            nuevo_usuario = Usuario(
                id=None,
                nombre=nombre,
                correo=Email(correo),
                contrasena_hash=contrasena_hash,
                tipo_usuario=Rol("operador"),
                estatus="Activo"
            )
            container.usuario_repo.guardar(nuevo_usuario)
            flash("¡Registro exitoso! Ahora puedes iniciar sesión como Operador.", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f"Error en el registro: {e}", "danger")
    return render_template('auth/registro.html')

@auth_bp.route('/logout')
def logout():
    session.pop('usuario', None)
    flash("Has cerrado sesión correctamente.", "info")
    return redirect(url_for('auth.login'))