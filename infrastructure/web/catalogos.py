from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.decorators import login_required
from infrastructure.container import container

catalogos_bp = Blueprint('catalogos', __name__)

# --- HORARIOS ---
@catalogos_bp.route('/horarios')
@login_required
def horarios_index():
    return render_template('catalogos/horarios_list.html', horarios=container.horario_repo.listar_todos())

@catalogos_bp.route('/horarios/nuevo', methods=['GET', 'POST'])
@login_required
def horarios_nuevo():
    if request.method == 'POST':
        container.horario_repo.guardar(request.form.get('horario'))
        flash("Horario registrado exitosamente.", "success")
        return redirect(url_for('catalogos.horarios_index'))
    return render_template('catalogos/horarios_form.html', horario=None)

@catalogos_bp.route('/horarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def horarios_editar(id):
    horario = container.horario_repo.buscar_por_id(id)
    if request.method == 'POST':
        container.horario_repo.actualizar(id, request.form.get('horario'))
        flash("Horario actualizado.", "success")
        return redirect(url_for('catalogos.horarios_index'))
    return render_template('catalogos/horarios_form.html', horario=horario)

@catalogos_bp.route('/horarios/eliminar/<int:id>', methods=['POST'])
@login_required
def horarios_eliminar(id):
    container.horario_repo.eliminar(id)
    flash("Horario eliminado.", "success")
    return redirect(url_for('catalogos.horarios_index'))


# --- DURACION ---
@catalogos_bp.route('/duracion')
@login_required
def duracion_index():
    return render_template('catalogos/duracion_list.html', duraciones=container.duracion_repo.listar_todos())

@catalogos_bp.route('/duracion/nuevo', methods=['GET', 'POST'])
@login_required
def duracion_nuevo():
    if request.method == 'POST':
        container.duracion_repo.guardar(request.form.get('duracion'))
        flash("Duración registrada con éxito.", "success")
        return redirect(url_for('catalogos.duracion_index'))
    return render_template('catalogos/duracion_form.html', duracion=None)

@catalogos_bp.route('/duracion/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def duracion_editar(id):
    duracion = container.duracion_repo.buscar_por_id(id)
    if request.method == 'POST':
        container.duracion_repo.actualizar(id, request.form.get('duracion'))
        flash("Duración actualizada.", "success")
        return redirect(url_for('catalogos.duracion_index'))
    return render_template('catalogos/duracion_form.html', duracion=duracion)

@catalogos_bp.route('/duracion/eliminar/<int:id>', methods=['POST'])
@login_required
def duracion_eliminar(id):
    container.duracion_repo.eliminar(id)
    flash("Duración eliminada.", "success")
    return redirect(url_for('catalogos.duracion_index'))


# --- FRECUENCIA ---
@catalogos_bp.route('/frecuencia')
@login_required
def frecuencia_index():
    return render_template('catalogos/frecuencia_list.html', frecuencias=container.frecuencia_repo.listar_todos())

@catalogos_bp.route('/frecuencia/nuevo', methods=['GET', 'POST'])
@login_required
def frecuencia_nuevo():
    if request.method == 'POST':
        container.frecuencia_repo.guardar(request.form.get('frecuencia'))
        flash("Frecuencia registrada con éxito.", "success")
        return redirect(url_for('catalogos.frecuencia_index'))
    return render_template('catalogos/frecuencia_form.html', frecuencia=None)

@catalogos_bp.route('/frecuencia/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def frecuencia_editar(id):
    frecuencia = container.frecuencia_repo.buscar_por_id(id)
    if request.method == 'POST':
        container.frecuencia_repo.actualizar(id, request.form.get('frecuencia'))
        flash("Frecuencia actualizada.", "success")
        return redirect(url_for('catalogos.frecuencia_index'))
    return render_template('catalogos/frecuencia_form.html', frecuencia=frecuencia)

@catalogos_bp.route('/frecuencia/eliminar/<int:id>', methods=['POST'])
@login_required
def frecuencia_eliminar(id):
    container.frecuencia_repo.eliminar(id)
    flash("Frecuencia eliminada.", "success")
    return redirect(url_for('catalogos.frecuencia_index'))