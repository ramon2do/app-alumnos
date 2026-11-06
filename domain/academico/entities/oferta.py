from dataclasses import dataclass
from typing import Optional
from domain.academico.value_objects.precio import Precio

@dataclass
class Oferta:
    id: Optional[int]
    oferta_academica: str
    tipo: str
    precio_en_divisas: Precio
    nro_partes_cuotas: int
    cada_una_de_en_divisas: float
