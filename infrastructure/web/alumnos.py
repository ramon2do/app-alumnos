from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.decorators import login_required
from utils.uploads import guardar_archivo
from infrastructure.container import container
from domain.academico.entities.alumno import Alumno
from domain.identidad.value_objects.email import Email
from domain.academico.value_objects.whatsapp import WhatsApp

alumnos_bp = Blueprint('alumnos', __name__, url_prefix='/alumnos')

@alumnos_bp.route('/')
@login_required
def index():
    return render_template('alumnos/list.html', alumnos=container.listar_alumnos_use_case().execute())

@alumnos_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    if request.method == 'POST':
        try:
            # CREACIÓN: Invoca al caso de uso que SÍ dispara las notificaciones (Correo y Whapi)
            container.crear_alumno_use_case().execute(
                request.form.get('tipo_cedula'), request.form.get('nro_cedula'),
                request.form.get('nombres'), request.form.get('apellidos'), request.form.get('genero'),
                request.form.get('fecha_nacimiento'), request.form.get('whatsapp'), request.form.get('correo'),
                guardar_archivo(request.files.get('foto_cedula'), 'cedula'),
                guardar_archivo(request.files.get('foto_carnet'), 'carnet')
            )
            flash("Alumno registrado correctamente y notificaciones enviadas.", "success")
            return redirect(url_for('alumnos.index'))
        except Exception as e: flash(str(e), "danger")
    return render_template('alumnos/form.html', alumno=None)

@alumnos_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    alumno = container.alumno_repo.buscar_por_id(id)
    if not alumno:
        flash("Alumno no encontrado.", "danger")
        return redirect(url_for('alumnos.index'))
    if request.method == 'POST':
        try:
            # EDICIÓN: Actualiza directamente en base de datos de forma SILENCIOSA (Sin notificaciones)
            alumno.tipo_cedula = request.form.get('tipo_cedula')
            alumno.nro_cedula = request.form.get('nro_cedula')
            alumno.nombres = request.form.get('nombres')
            alumno.apellidos = request.form.get('apellidos')
            alumno.genero = request.form.get('genero')
            alumno.fecha_nacimiento = request.form.get('fecha_nacimiento')
            alumno.whatsapp = WhatsApp(request.form.get('whatsapp'))
            alumno.correo = Email(request.form.get('correo'))
            
            f_cedula = request.files.get('foto_cedula')
            if f_cedula and f_cedula.filename != '':
                alumno.foto_cedula = guardar_archivo(f_cedula, 'cedula')
                
            f_carnet = request.files.get('foto_carnet')
            if f_carnet and f_carnet.filename != '':
                alumno.foto_carnet = guardar_archivo(f_carnet, 'carnet')

            container.alumno_repo.actualizar(alumno)
            flash("Alumno actualizado correctamente.", "success")
            return redirect(url_for('alumnos.index'))
        except Exception as e: flash(str(e), "danger")
    return render_template('alumnos/form.html', alumno=alumno)

@alumnos_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    try:
        container.alumno_repo.eliminar(id)
        flash("Alumno eliminado correctamente.", "success")
    except Exception as e:
        flash(f"Error al eliminar: {e}", "danger")
    return redirect(url_for('alumnos.index'))