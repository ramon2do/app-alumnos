from dataclasses import dataclass
from typing import Optional
@dataclass
class ProfesorDTO:
    id: Optional[int]
    tipo_cedula: str
    nro_cedula: str
    nombres: str
    apellidos: str
    genero: str
    fecha_nacimiento: str
    area_conocimiento: str
    whatsapp: str
    correo: str
    foto_cedula: str
    foto_carnet: str

    @property
    def cedula(self) -> str:
        return f"{self.tipo_cedula}-{self.nro_cedula}"
