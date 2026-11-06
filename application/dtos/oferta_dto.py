from dataclasses import dataclass
from typing import Optional
@dataclass
class OfertaDTO:
    id: Optional[int]
    oferta_academica: str
    tipo: str
    precio_en_divisas: float
    nro_partes_cuotas: int
    cada_una_de_en_divisas: float