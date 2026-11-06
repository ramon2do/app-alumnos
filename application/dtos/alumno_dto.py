from dataclasses import dataclass
from typing import Optional
@dataclass
class AlumnoDTO:
    id: Optional[int]
    tipo_cedula: str
    nro_cedula: str
    nombres: str
    apellidos: str
    genero: str
    fecha_nacimiento: str
    whatsapp: str
    correo: str
    foto_cedula: str
    foto_carnet: str
    id_usuario: Optional[int] = None

    @property
    def cedula(self) -> str:
        return f"{self.tipo_cedula}-{self.nro_cedula}"
