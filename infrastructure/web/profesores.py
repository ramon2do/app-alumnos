from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.decorators import login_required
from utils.uploads import guardar_archivo
from infrastructure.container import container
from domain.academico.entities.profesor import Profesor
from domain.identidad.value_objects.email import Email
from domain.academico.value_objects.whatsapp import WhatsApp

profesores_bp = Blueprint('profesores', __name__, url_prefix='/profesores')

@profesores_bp.route('/')
@login_required
def index():
    return render_template('profesores/list.html', profesores=container.listar_profesores_use_case().execute())

@profesores_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    if request.method == 'POST':
        f_cedula = request.files.get('foto_cedula')
        f_carnet = request.files.get('foto_carnet')
        
        path_cedula = guardar_archivo(f_cedula, 'cedula') if f_cedula and f_cedula.filename != '' else request.form.get('temp_foto_cedula', '')
        path_carnet = guardar_archivo(f_carnet, 'carnet') if f_carnet and f_carnet.filename != '' else request.form.get('temp_foto_carnet', '')

        try:
            # Orden estricto y correcto alineado con CrearProfesorUseCase.execute()
            container.crear_profesor_use_case().execute(
                request.form.get('tipo_cedula'),       # 1
                request.form.get('nro_cedula'),        # 2
                request.form.get('nombres'),           # 3
                request.form.get('apellidos'),         # 4
                request.form.get('genero'),            # 5 -> Género
                request.form.get('fecha_nacimiento'),  # 6 -> Fecha de Nacimiento
                request.form.get('area_conocimiento'), # 7 -> Área de Conocimiento
                request.form.get('whatsapp'),          # 8
                request.form.get('correo'),            # 9
                path_cedula,                           # 10
                path_carnet                            # 11
            )
            flash("Profesor registrado correctamente.", "success")
            return redirect(url_for('profesores.index'))
        except Exception as e:
            error_msg = str(e).lower()
            if "unique constraint failed" in error_msg or "registrado" in error_msg or "duplicado" in error_msg:
                if "correo" in error_msg or "email" in error_msg:
                    mensaje = "⚠️ El correo electrónico ingresado ya se encuentra registrado por otro profesor."
                elif "cedula" in error_msg or "nro_cedula" in error_msg:
                    mensaje = "⚠️ La cédula de identidad ingresada ya pertenece a otro profesor."
                else:
                    mensaje = f"⚠️ Ya existe un profesor con estos datos únicos ({str(e)})."
            else:
                mensaje = f"⚠️ {str(e)}"
            
            flash(mensaje, "danger")
            temp_profesor = type('TempProfesor', (object,), {
                'foto_cedula': path_cedula,
                'foto_carnet': path_carnet
            })()
            return render_template('profesores/form.html', profesor=temp_profesor, form_data=request.form)
            
    return render_template('profesores/form.html', profesor=None, form_data=None)

@profesores_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    profesor = container.profesor_repo.buscar_por_id(id)
    if not profesor:
        flash("Profesor no encontrado.", "danger")
        return redirect(url_for('profesores.index'))
        
    if request.method == 'POST':
        try:
            profesor.tipo_cedula = request.form.get('tipo_cedula')
            profesor.nro_cedula = request.form.get('nro_cedula')
            profesor.nombres = request.form.get('nombres')
            profesor.apellidos = request.form.get('apellidos')
            profesor.area_conocimiento = request.form.get('area_conocimiento')
            profesor.genero = request.form.get('genero')
            profesor.fecha_nacimiento = request.form.get('fecha_nacimiento')
            profesor.whatsapp = WhatsApp(request.form.get('whatsapp'))
            profesor.correo = Email(request.form.get('correo'))
            
            f_cedula = request.files.get('foto_cedula')
            if f_cedula and f_cedula.filename != '':
                profesor.foto_cedula = guardar_archivo(f_cedula, 'cedula')
                
            f_carnet = request.files.get('foto_carnet')
            if f_carnet and f_carnet.filename != '':
                profesor.foto_carnet = guardar_archivo(f_carnet, 'carnet')

            container.profesor_repo.actualizar(profesor)
            flash("Profesor actualizado correctamente.", "success")
            return redirect(url_for('profesores.index'))
        except Exception as e:
            error_msg = str(e).lower()
            if "unique constraint failed" in error_msg or "registrado" in error_msg or "duplicado" in error_msg:
                if "correo" in error_msg or "email" in error_msg:
                    mensaje = "⚠️ El correo electrónico ingresado ya se encuentra registrado por otro profesor."
                elif "cedula" in error_msg or "nro_cedula" in error_msg:
                    mensaje = "⚠️ La cédula de identidad ingresada ya pertenece a otro profesor."
                else:
                    mensaje = f"⚠️ Ya existe un profesor con estos datos únicos ({str(e)})."
            else:
                mensaje = f"⚠️ {str(e)}"
            
            flash(mensaje, "danger")
            return render_template('profesores/form.html', profesor=profesor, form_data=request.form)
            
    return render_template('profesores/form.html', profesor=profesor, form_data=None)

@profesores_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    try:
        container.profesor_repo.eliminar(id)
        flash("Profesor eliminado correctamente.", "success")
    except Exception as e:
        flash(f"Error al eliminar: {e}", "danger")
    return redirect(url_for('profesores.index'))