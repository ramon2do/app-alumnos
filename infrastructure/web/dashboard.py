from flask import Blueprint, render_template
from utils.decorators import login_required
from infrastructure.container import container

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    metrics = {
        'alumnos': len(container.alumno_repo.listar_todos()),
        'profesores': len(container.profesor_repo.listar_todos()),
        'ofertas': len(container.oferta_repo.listar_todas()),
        'inscripciones': len(container.inscripcion_repo.listar_todas_detalle())
    }
    return render_template('dashboard.html', metrics=metrics)
