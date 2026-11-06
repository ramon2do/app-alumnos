from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.decorators import login_required
from infrastructure.container import container
from domain.academico.value_objects.precio import Precio

ofertas_bp = Blueprint('ofertas', __name__, url_prefix='/ofertas')

@ofertas_bp.route('/')
@login_required
def index(): return render_template('ofertas/list.html', ofertas=container.listar_ofertas_use_case().execute())

@ofertas_bp.route('/nueva', methods=['GET', 'POST'])
@login_required
def nueva():
    if request.method == 'POST':
        try:
            container.crear_oferta_use_case().execute(
                request.form.get('oferta_academica'), request.form.get('tipo'),
                float(request.form.get('precio_en_divisas', 0)), int(request.form.get('nro_partes_cuotas', 1)),
                float(request.form.get('cada_una_de_en_divisas', 0))
            )
            flash("Oferta académica registrada con éxito.", "success")
            return redirect(url_for('ofertas.index'))
        except Exception as e: flash(str(e), "danger")
    return render_template('ofertas/form.html', oferta=None)

@ofertas_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    oferta = container.oferta_repo.buscar_por_id(id)
    if not oferta:
        flash("Oferta no encontrada.", "danger")
        return redirect(url_for('ofertas.index'))
    if request.method == 'POST':
        try:
            oferta.oferta_academica = request.form.get('oferta_academica')
            oferta.tipo = request.form.get('tipo')
            oferta.precio_en_divisas = Precio(float(request.form.get('precio_en_divisas', 0)))
            oferta.nro_partes_cuotas = int(request.form.get('nro_partes_cuotas', 1))
            oferta.cada_una_de_en_divisas = float(request.form.get('cada_una_de_en_divisas', 0))
            container.oferta_repo.actualizar(oferta)
            flash("Oferta actualizada correctamente.", "success")
            return redirect(url_for('ofertas.index'))
        except Exception as e: flash(str(e), "danger")
    return render_template('ofertas/form.html', oferta=oferta)

@ofertas_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    try:
        container.oferta_repo.eliminar(id)
        flash("Oferta eliminada correctamente.", "success")
    except Exception as e:
        flash(f"Error al eliminar: {e}", "danger")
    return redirect(url_for('ofertas.index'))
