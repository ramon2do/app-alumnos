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
        f_cedula = request.files.get('foto_cedula')
        f_carnet = request.files.get('foto_carnet')
        
        path_cedula = guardar_archivo(f_cedula, 'cedula') if f_cedula and f_cedula.filename != '' else request.form.get('temp_foto_cedula', '')
        path_carnet = guardar_archivo(f_carnet, 'carnet') if f_carnet and f_carnet.filename != '' else request.form.get('temp_foto_carnet', '')

        try:
            container.crear_alumno_use_case().execute(
                request.form.get('tipo_cedula'), request.form.get('nro_cedula'),
                request.form.get('nombres'), request.form.get('apellidos'), request.form.get('genero'),
                request.form.get('fecha_nacimiento'), request.form.get('whatsapp'), request.form.get('correo'),
                path_cedula, path_carnet
            )
            flash("Alumno registrado correctamente y notificaciones enviadas.", "success")
            return redirect(url_for('alumnos.index'))
        except Exception as e:
            error_msg = str(e).lower()
            if "unique constraint failed" in error_msg or "registrado" in error_msg or "duplicado" in error_msg:
                if "correo" in error_msg or "email" in error_msg:
                    mensaje = "⚠️ El correo electrónico ingresado ya se encuentra registrado por otro usuario. Por favor, escribe uno diferente."
                elif "cedula" in error_msg or "nro_cedula" in error_msg:
                    mensaje = "⚠️ La cédula de identidad ingresada ya pertenece a otro registro en el sistema."
                else:
                    mensaje = f"⚠️ Ya existe un registro con estos datos únicos ({str(e)})."
            else:
                mensaje = f"⚠️ {str(e)}"
            
            flash(mensaje, "danger")
            temp_alumno = type('TempAlumno', (object,), {
                'foto_cedula': path_cedula,
                'foto_carnet': path_carnet
            })()
            return render_template('alumnos/form.html', alumno=temp_alumno, form_data=request.form)
            
    return render_template('alumnos/form.html', alumno=None, form_data=None)

@alumnos_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    alumno = container.alumno_repo.buscar_por_id(id)
    if not alumno:
        flash("Alumno no encontrado.", "danger")
        return redirect(url_for('alumnos.index'))
        
    if request.method == 'POST':
        try:
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
        except Exception as e:
            error_msg = str(e).lower()
            if "unique constraint failed" in error_msg or "registrado" in error_msg or "duplicado" in error_msg:
                if "correo" in error_msg or "email" in error_msg:
                    mensaje = "⚠️ El correo electrónico ingresado ya se encuentra registrado por otro usuario."
                elif "cedula" in error_msg or "nro_cedula" in error_msg:
                    mensaje = "⚠️ La cédula de identidad ingresada ya pertenece a otro registro."
                else:
                    mensaje = f"⚠️ Ya existe un registro con estos datos únicos ({str(e)})."
            else:
                mensaje = f"⚠️ {str(e)}"
            
            flash(mensaje, "danger")
            return render_template('alumnos/form.html', alumno=alumno, form_data=request.form)
            
    return render_template('alumnos/form.html', alumno=alumno, form_data=None)

@alumnos_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    try:
        container.alumno_repo.eliminar(id)
        flash("Alumno eliminado correctamente.", "success")
    except Exception as e:
        flash(f"Error al eliminar: {e}", "danger")
    return redirect(url_for('alumnos.index'))