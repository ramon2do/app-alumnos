from werkzeug.security import check_password_hash
from domain.identidad.repositories.usuario_repository import UsuarioRepository
from domain.identidad.exceptions.identidad_exceptions import CredencialesInvalidasError, UsuarioInactivoError
from application.dtos.usuario_dto import UsuarioDTO

class LoginUseCase:
    def __init__(self, usuario_repo: UsuarioRepository):
        self.usuario_repo = usuario_repo

    def execute(self, correo: str, contrasena: str) -> UsuarioDTO:
        usuario = self.usuario_repo.buscar_por_correo(correo)
        if not usuario or not check_password_hash(usuario.contrasena_hash, contrasena):
            raise CredencialesInvalidasError("Correo o contraseña incorrectos.")
        if not usuario.puede_iniciar_sesion():
            raise UsuarioInactivoError("El usuario está inactivo.")
        return UsuarioDTO(id=usuario.id, nombre=usuario.nombre, correo=usuario.correo.value, tipo_usuario=usuario.tipo_usuario.value, estatus=usuario.estatus)
