from domain.academico.repositories.inscripcion_repository import InscripcionRepository
class ListarInscripcionesUseCase:
    def __init__(self, inscripcion_repo: InscripcionRepository): self.inscripcion_repo = inscripcion_repo
    def execute(self): return self.inscripcion_repo.listar_todas_detalle()
