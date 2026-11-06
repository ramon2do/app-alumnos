from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.decorators import login_required
from utils.uploads import guardar_archivo
from infrastructure.container import container
from domain.identidad.value_objects.email import Email
from domain.academico.value_objects.whatsapp import WhatsApp

profesores_bp = Blueprint('profesores', __name__, url_prefix='/profesores')

@profesores_bp.route('/')
@login_required
def index(): return render_template('profesores/list.html', profesores=container.listar_profesores_use_case().execute())

@profesores_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    if request.method == 'POST':
        try:
            container.crear_profesor_use_case().execute(
                request.form.get('tipo_cedula'), request.form.get('nro_cedula'),
                request.form.get('nombres'), request.form.get('apellidos'), request.form.get('genero'),
                request.form.get('fecha_nacimiento'), request.form.get('area_conocimiento'),
                request.form.get('whatsapp'), request.form.get('correo'),
                guardar_archivo(request.files.get('foto_cedula'), 'cedula'),
                guardar_archivo(request.files.get('foto_carnet'), 'carnet')
            )
            flash("Profesor registrado correctamente.", "success")
            return redirect(url_for('profesores.index'))
        except Exception as e: flash(str(e), "danger")
    return render_template('profesores/form.html', profesor=None)

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
            profesor.genero = request.form.get('genero')
            profesor.fecha_nacimiento = request.form.get('fecha_nacimiento')
            profesor.area_conocimiento = request.form.get('area_conocimiento')
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
        except Exception as e: flash(str(e), "danger")
    return render_template('profesores/form.html', profesor=profesor)

@profesores_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    try:
        container.profesor_repo.eliminar(id)
        flash("Profesor eliminado correctamente.", "success")
    except Exception as e:
        flash(f"Error al eliminar: {e}", "danger")
    return redirect(url_for('profesores.index'))
