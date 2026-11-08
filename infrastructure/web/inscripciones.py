from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from utils.decorators import login_required
from infrastructure.container import container

inscripciones_bp = Blueprint('inscripciones', __name__, url_prefix='/inscripciones')

@inscripciones_bp.route('/')
@login_required
def index():
    return render_template('inscripciones/list.html', inscripciones=container.listar_inscripciones_use_case().execute())

@inscripciones_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    ofertas = container.listar_ofertas_use_case().execute()
    if request.method == 'POST':
        try:
            container.crear_inscripcion_use_case().execute(
                request.form.get('id_alumno'),
                request.form.get('id_oferta')
            )
            flash("Inscripción realizada correctamente.", "success")
            return redirect(url_for('inscripciones.index'))
        except Exception as e:
            flash(str(e), "danger")
            return render_template('inscripciones/form.html', ofertas=ofertas, form_data=request.form)
            
    return render_template('inscripciones/form.html', ofertas=ofertas, form_data=None)

@inscripciones_bp.route('/api/alumno', methods=['GET'])
@login_required
def api_buscar_alumno():
    tipo = request.args.get('tipo', 'V')
    nro = request.args.get('nro', '')
    alumno = container.alumno_repo.buscar_por_cedula(tipo, nro)
    if alumno:
        return jsonify({
            "success": True,
            "id": alumno.id,
            "nombres": alumno.nombres,
            "apellidos": alumno.apellidos,
            "correo": alumno.correo.value,
            "whatsapp": alumno.whatsapp.value,
            "foto": alumno.foto_carnet or alumno.foto_cedula
        })
    return jsonify({"success": False})

@inscripciones_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    try:
        container.inscripcion_repo.eliminar(id)
        flash("Inscripción eliminada correctamente.", "success")
    except Exception as e:
        flash(f"Error al eliminar: {e}", "danger")
    return redirect(url_for('inscripciones.index'))