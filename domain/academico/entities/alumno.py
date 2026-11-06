from dataclasses import dataclass
from typing import Optional
from domain.identidad.value_objects.email import Email
from domain.academico.value_objects.whatsapp import WhatsApp

@dataclass
class Alumno:
    id: Optional[int]
    tipo_cedula: str
    nro_cedula: str
    nombres: str
    apellidos: str
    genero: str
    fecha_nacimiento: str
    whatsapp: WhatsApp
    correo: Email
    foto_cedula: str
    foto_carnet: str
    id_usuario: Optional[int] = None

    @property
    def cedula(self) -> str:
        return f"{self.tipo_cedula}-{self.nro_cedula}"

    @property
    def nombre_completo(self) -> str:
        return f"{self.nombres} {self.apellidos}"
