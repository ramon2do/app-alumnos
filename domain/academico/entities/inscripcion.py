from dataclasses import dataclass
from typing import Optional

@dataclass
class Inscripcion:
    id: Optional[int]
    id_alumno: int
    id_oferta: int
    id_profesor: int
    id_horario: int
    id_duracion: int
    id_frecuencia: int
    fecha_inscripcion: str

    def validar(self):
        if not (self.id_alumno and self.id_oferta and self.id_profesor and self.id_horario and self.id_duracion and self.id_frecuencia):
            raise ValueError("Inscripción incompleta: Todos los campos y catálogos son obligatorios.")