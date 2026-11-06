from dataclasses import dataclass
from typing import Optional
from domain.identidad.value_objects.email import Email
from domain.identidad.value_objects.rol import Rol

@dataclass
class Usuario:
    id: Optional[int]
    nombre: str
    correo: Email
    contrasena_hash: str
    tipo_usuario: Rol
    estatus: str = "Activo"

    def puede_iniciar_sesion(self) -> bool:
        return self.estatus.lower() == "activo"
