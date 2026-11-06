from domain.academico.repositories.alumno_repository import AlumnoRepository
from application.dtos.alumno_dto import AlumnoDTO
class ListarAlumnosUseCase:
    def __init__(self, alumno_repo: AlumnoRepository): self.alumno_repo = alumno_repo
    def execute(self):
        return [AlumnoDTO(a.id, a.tipo_cedula, a.nro_cedula, a.nombres, a.apellidos, a.genero, a.fecha_nacimiento, a.whatsapp.value, a.correo.value, a.foto_cedula, a.foto_carnet, a.id_usuario) for a in self.alumno_repo.listar_todos()]
