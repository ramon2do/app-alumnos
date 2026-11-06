from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from utils.decorators import login_required
from utils.notifications import enviar_correo, enviar_whatsapp
from infrastructure.container import container

inscripciones_bp = Blueprint('inscripciones', __name__, url_prefix='/inscripciones')

@inscripciones_bp.route('/')
@login_required
def index(): 
    return render_template('inscripciones/list.html', inscripciones=container.inscripcion_repo.listar_todas_detalle())

# Endpoint JSON para buscar alumno por Cédula (V/E + Nro) vía AJAX/Fetch
@inscripciones_bp.route('/api/alumno', methods=['GET'])
@login_required
def api_alumno():
    tipo = request.args.get('tipo')
    nro = request.args.get('nro')
    alumno = container.alumno_repo.buscar_por_cedula(tipo, nro)
    if alumno:
        return jsonify({
            'success': True,
            'id': alumno.id,
            'nombres': alumno.nombres,
            'apellidos': alumno.apellidos,
            'correo': alumno.correo.value,
            'whatsapp': alumno.whatsapp.value,
            'foto': alumno.foto_carnet
        })
    return jsonify({'success': False, 'message': 'Alumno no encontrado.'})

@inscripciones_bp.route('/nueva', methods=['GET', 'POST'])
@login_required
def nueva():
    if request.method == 'POST':
        try:
            id_alumno = int(request.form.get('id_alumno'))
            id_oferta = int(request.form.get('id_oferta'))
            id_profesor = int(request.form.get('id_profesor'))
            id_horario = int(request.form.get('id_horario'))
            id_duracion = int(request.form.get('id_duracion'))
            id_frecuencia = int(request.form.get('id_frecuencia'))

            # Guardar inscripción
            inscripcion_dto = container.crear_inscripcion_use_case().execute(
                id_alumno, id_oferta, id_profesor, id_horario, id_duracion, id_frecuencia
            )

            # Obtener datos de alumno y oferta para la notificación
            alumno = container.alumno_repo.buscar_por_id(id_alumno)
            oferta = container.oferta_repo.buscar_por_id(id_oferta)

            # Enviar Notificaciones (Correo y WhatsApp)
            if alumno and oferta:
                asunto = "¡Inscripción Exitosa en AppAlumnos!"
                mensaje_correo = f"Hola {alumno.nombre_completo}, te has inscrito exitosamente en la oferta académica: {oferta.oferta_academica}."
                mensaje_wa = f"¡Hola {alumno.nombres}! Tu inscripción en *{oferta.oferta_academica}* ha sido procesada con éxito."
                
                enviar_correo(alumno.correo.value, asunto, mensaje_correo)
                enviar_whatsapp(alumno.whatsapp.value, mensaje_wa)

            flash("Inscripción guardada correctamente y notificaciones enviadas.", "success")
            return redirect(url_for('inscripciones.index'))
        except Exception as e: 
            flash(f"Error: {e}", "danger")
            
    return render_template('inscripciones/form.html',
                           ofertas=container.oferta_repo.listar_todas(),
                           profesores=container.profesor_repo.listar_todos(),
                           horarios=container.horario_repo.listar_todos(),
                           duraciones=container.duracion_repo.listar_todos(),
                           frecuencias=container.frecuencia_repo.listar_todos())

@inscripciones_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    inscripcion = container.inscripcion_repo.buscar_por_id(id)
    if not inscripcion:
        flash("Inscripción no encontrada.", "danger")
        return redirect(url_for('inscripciones.index'))

    if request.method == 'POST':
        try:
            inscripcion.id_alumno = int(request.form.get('id_alumno'))
            inscripcion.id_oferta = int(request.form.get('id_oferta'))
            inscripcion.id_profesor = int(request.form.get('id_profesor'))
            inscripcion.id_horario = int(request.form.get('id_horario'))
            inscripcion.id_duracion = int(request.form.get('id_duracion'))
            inscripcion.id_frecuencia = int(request.form.get('id_frecuencia'))

            inscripcion.validar()
            container.inscripcion_repo.actualizar(inscripcion)

            flash("Inscripción actualizada correctamente.", "success")
            return redirect(url_for('inscripciones.index'))
        except Exception as e:
            flash(f"Error al actualizar: {e}", "danger")

    # Obtener el alumno actual para precargar sus datos en el formulario de edición
    alumno_actual = container.alumno_repo.buscar_por_id(inscripcion.id_alumno)

    return render_template('inscripciones/form.html',
                           inscripcion=inscripcion,
                           alumno_actual=alumno_actual,
                           ofertas=container.oferta_repo.listar_todas(),
                           profesores=container.profesor_repo.listar_todos(),
                           horarios=container.horario_repo.listar_todos(),
                           duraciones=container.duracion_repo.listar_todos(),
                           frecuencias=container.frecuencia_repo.listar_todos())

@inscripciones_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    try:
        container.inscripcion_repo.eliminar(id)
        flash("Inscripción eliminada correctamente.", "success")
    except Exception as e:
        flash(f"Error al eliminar: {e}", "danger")
    return redirect(url_for('inscripciones.index'))