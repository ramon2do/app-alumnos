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
            # Captura de datos del formulario de registro de operador/usuario
            nombres = request.form.get('nombres')
            apellidos = request.form.get('apellidos')
            correo = request.form.get('correo')
            password = request.form.get('password')
            
            # Instanciación posicional exacta que espera la entidad Usuario
            nuevo_usuario = Usuario(
                None, 
                f"{nombres} {apellidos}", 
                Email(correo), 
                generate_password_hash(password), 
                Rol("operador"), 
                "Activo"
            )
            
            # Se pasa el objeto entidad completo al repositorio
            container.usuario_repo.guardar(nuevo_usuario)
            
            flash("¡Registro exitoso! Ya puedes iniciar sesión con tus credenciales.", "success")
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            error_msg = str(e)
            if "UNIQUE constraint failed" in error_msg or "registrado" in error_msg.lower():
                if "correo" in error_msg.lower():
                    mensaje = "⚠️ El correo electrónico ingresado ya se encuentra registrado en el sistema."
                elif "cedula" in error_msg.lower():
                    mensaje = "⚠️ La cédula de identidad ingresada ya pertenece a otro usuario."
                else:
                    mensaje = "⚠️ Ya existe un usuario registrado con estos datos únicos."
            else:
                mensaje = f"⚠️ {error_msg}"
            
            flash(mensaje, "danger")
            return render_template('auth/registro.html', form_data=request.form)
            
    return render_template('auth/registro.html', form_data=None)

@auth_bp.route('/logout')
def logout():
    session.pop('usuario', None)
    flash("Has cerrado sesión correctamente.", "info")
    return redirect(url_for('auth.login'))