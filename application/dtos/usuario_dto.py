from dataclasses import dataclass
from typing import Optional
@dataclass
class UsuarioDTO:
    id: Optional[int]
    nombre: str
    correo: str
    tipo_usuario: str
    estatus: str