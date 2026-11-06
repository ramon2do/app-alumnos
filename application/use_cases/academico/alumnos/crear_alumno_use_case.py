import secrets, string
from werkzeug.security import generate_password_hash
from domain.academico.repositories.alumno_repository import AlumnoRepository
from domain.identidad.repositories.usuario_repository import UsuarioRepository
from domain.academico.entities.alumno import Alumno
from domain.identidad.entities.usuario import Usuario
from domain.identidad.value_objects.email import Email
from domain.identidad.value_objects.rol import Rol
from domain.academico.value_objects.whatsapp import WhatsApp
from domain.identidad.exceptions.identidad_exceptions import CorreoDuplicadoError
from domain.academico.events.alumno_registrado import AlumnoRegistrado
from infrastructure.event_handlers.alumno_registrado_handler import AlumnoRegistradoHandler
from application.dtos.alumno_dto import AlumnoDTO

class CrearAlumnoUseCase:
    def __init__(self, alumno_repo: AlumnoRepository, usuario_repo: UsuarioRepository):
        self.alumno_repo = alumno_repo
        self.usuario_repo = usuario_repo

    def execute(self, tipo_cedula, nro_cedula, nombres, apellidos, genero, fecha_nacimiento, whatsapp, correo, foto_cedula, foto_carnet) -> AlumnoDTO:
        if self.alumno_repo.buscar_por_correo(correo):
            raise CorreoDuplicadoError("El correo ya existe.")
        raw_pass = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
        u = self.usuario_repo.guardar(Usuario(None, f"{nombres} {apellidos}", Email(correo), generate_password_hash(raw_pass), Rol("alumno"), "Activo"))
        a = self.alumno_repo.guardar(Alumno(None, tipo_cedula, nro_cedula, nombres, apellidos, genero, fecha_nacimiento, WhatsApp(whatsapp), Email(correo), foto_cedula, foto_carnet, u.id))
        AlumnoRegistradoHandler.handle(AlumnoRegistrado(a.id, a.nombre_completo, a.correo.value, a.whatsapp.value, a.correo.value, raw_pass))
        return AlumnoDTO(a.id, a.tipo_cedula, a.nro_cedula, a.nombres, a.apellidos, a.genero, a.fecha_nacimiento, a.whatsapp.value, a.correo.value, a.foto_cedula, a.foto_carnet, a.id_usuario)
