from infrastructure.repositories.sqlite_usuario_repository import SQLiteUsuarioRepository
from infrastructure.repositories.sqlite_alumno_repository import SQLiteAlumnoRepository
from infrastructure.repositories.sqlite_profesor_repository import SQLiteProfesorRepository
from infrastructure.repositories.sqlite_oferta_repository import SQLiteOfertaRepository
from infrastructure.repositories.sqlite_inscripcion_repository import SQLiteInscripcionRepository

from infrastructure.repositories.sqlite_catalogos_repository import (
    SQLiteHorarioRepository, 
    SQLiteDuracionRepository, 
    SQLiteFrecuenciaRepository
)

from application.use_cases.identidad.login_use_case import LoginUseCase
from application.use_cases.academico.alumnos.crear_alumno_use_case import CrearAlumnoUseCase
from application.use_cases.academico.alumnos.listar_alumnos_use_case import ListarAlumnosUseCase
from application.use_cases.academico.profesores.crear_profesor_use_case import CrearProfesorUseCase
from application.use_cases.academico.profesores.listar_profesores_use_case import ListarProfesoresUseCase
from application.use_cases.academico.ofertas.crear_oferta_use_case import CrearOfertaUseCase
from application.use_cases.academico.ofertas.listar_ofertas_use_case import ListarOfertasUseCase
from application.use_cases.academico.inscripciones.crear_inscripcion_use_case import CrearInscripcionUseCase
from application.use_cases.academico.inscripciones.listar_inscripciones_use_case import ListarInscripcionesUseCase

class Container:
    def __init__(self):
        self.usuario_repo = SQLiteUsuarioRepository()
        self.alumno_repo = SQLiteAlumnoRepository()
        self.profesor_repo = SQLiteProfesorRepository()
        self.oferta_repo = SQLiteOfertaRepository()
        self.inscripcion_repo = SQLiteInscripcionRepository()
        self.horario_repo = SQLiteHorarioRepository()
        self.duracion_repo = SQLiteDuracionRepository()
        self.frecuencia_repo = SQLiteFrecuenciaRepository()

    def login_use_case(self): return LoginUseCase(self.usuario_repo)
    def crear_alumno_use_case(self): return CrearAlumnoUseCase(self.alumno_repo, self.usuario_repo)
    def listar_alumnos_use_case(self): return ListarAlumnosUseCase(self.alumno_repo)
    def crear_profesor_use_case(self): return CrearProfesorUseCase(self.profesor_repo)
    def listar_profesores_use_case(self): return ListarProfesoresUseCase(self.profesor_repo)
    def crear_oferta_use_case(self): return CrearOfertaUseCase(self.oferta_repo)
    def listar_ofertas_use_case(self): return ListarOfertasUseCase(self.oferta_repo)
    def crear_inscripcion_use_case(self): return CrearInscripcionUseCase(self.inscripcion_repo, self.alumno_repo, self.oferta_repo)
    def listar_inscripciones_use_case(self): return ListarInscripcionesUseCase(self.inscripcion_repo)

container = Container()
