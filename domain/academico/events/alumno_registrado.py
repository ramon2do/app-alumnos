from dataclasses import dataclass
from domain.shared.domain_event import DomainEvent

@dataclass
class AlumnoRegistrado(DomainEvent):
    alumno_id: int
    nombre_completo: str
    correo: str
    whatsapp: str
    usuario_generado: str
    contrasena_generada: str
