from dataclasses import dataclass
from typing import Optional
@dataclass
class InscripcionDTO:
    id: Optional[int]
    id_alumno: int
    id_oferta: int
    id_profesor: int
    horario: str
    duracion: str
    frecuencia: str
    fecha_inscripcion: str