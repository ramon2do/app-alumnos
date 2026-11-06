from domain.academico.repositories.profesor_repository import ProfesorRepository
from application.dtos.profesor_dto import ProfesorDTO
class ListarProfesoresUseCase:
    def __init__(self, profesor_repo: ProfesorRepository): self.profesor_repo = profesor_repo
    def execute(self):
        return [ProfesorDTO(p.id, p.tipo_cedula, p.nro_cedula, p.nombres, p.apellidos, p.genero, p.fecha_nacimiento, p.area_conocimiento, p.whatsapp.value, p.correo.value, p.foto_cedula, p.foto_carnet) for p in self.profesor_repo.listar_todos()]
