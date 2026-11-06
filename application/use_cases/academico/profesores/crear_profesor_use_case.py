from domain.academico.repositories.profesor_repository import ProfesorRepository
from domain.academico.entities.profesor import Profesor
from domain.identidad.value_objects.email import Email
from domain.academico.value_objects.whatsapp import WhatsApp
from application.dtos.profesor_dto import ProfesorDTO

class CrearProfesorUseCase:
    def __init__(self, profesor_repo: ProfesorRepository): self.profesor_repo = profesor_repo
    def execute(self, tipo_cedula, nro_cedula, nombres, apellidos, genero, fecha_nacimiento, area_conocimiento, whatsapp, correo, foto_cedula, foto_carnet) -> ProfesorDTO:
        p = self.profesor_repo.guardar(Profesor(None, tipo_cedula, nro_cedula, nombres, apellidos, genero, fecha_nacimiento, area_conocimiento, WhatsApp(whatsapp), Email(correo), foto_cedula, foto_carnet))
        return ProfesorDTO(p.id, p.tipo_cedula, p.nro_cedula, p.nombres, p.apellidos, p.genero, p.fecha_nacimiento, p.area_conocimiento, p.whatsapp.value, p.correo.value, p.foto_cedula, p.foto_carnet)
