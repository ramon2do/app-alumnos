from datetime import datetime
from domain.academico.repositories.inscripcion_repository import InscripcionRepository
from domain.academico.entities.inscripcion import Inscripcion
from application.dtos.inscripcion_dto import InscripcionDTO

class CrearInscripcionUseCase:
    def __init__(self, inscripcion_repo: InscripcionRepository, alumno_repo=None, oferta_repo=None):
        self.inscripcion_repo = inscripcion_repo

    def execute(self, id_alumno, id_oferta, id_profesor, id_horario, id_duracion, id_frecuencia) -> InscripcionDTO:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Instanciar la entidad pasando los IDs de los catálogos
        inscripcion = Inscripcion(
            id=None, 
            id_alumno=id_alumno, 
            id_oferta=id_oferta, 
            id_profesor=id_profesor, 
            id_horario=id_horario, 
            id_duracion=id_duracion, 
            id_frecuencia=id_frecuencia, 
            fecha_inscripcion=fecha
        )
        
        # Validar la entidad (si tienes el método validar dentro de la entidad)
        if hasattr(inscripcion, 'validar'):
            inscripcion.validar()

        i = self.inscripcion_repo.guardar(inscripcion)
        
        # Retornar el DTO con los atributos por ID
        return InscripcionDTO(
            i.id, 
            i.id_alumno, 
            i.id_oferta, 
            i.id_profesor, 
            i.id_horario, 
            i.id_duracion, 
            i.id_frecuencia, 
            i.fecha_inscripcion
        )