from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from domain.academico.entities.inscripcion import Inscripcion

class InscripcionRepository(ABC):
    @abstractmethod
    def guardar(self, inscripcion: Inscripcion) -> Inscripcion: pass
    @abstractmethod
    def buscar_por_id(self, id_inscripcion: int) -> Optional[Inscripcion]: pass
    @abstractmethod
    def listar_todas_detalle(self) -> List[Dict[str, Any]]: pass
    @abstractmethod
    def listar_por_oferta_detalle(self, id_oferta: int) -> List[Dict[str, Any]]: pass
    @abstractmethod
    def eliminar(self, id_inscripcion: int) -> None: pass
