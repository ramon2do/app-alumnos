from abc import ABC, abstractmethod
from typing import Optional, List
from domain.academico.entities.oferta import Oferta

class OfertaRepository(ABC):
    @abstractmethod
    def guardar(self, oferta: Oferta) -> Oferta: pass
    @abstractmethod
    def buscar_por_id(self, id_oferta: int) -> Optional[Oferta]: pass
    @abstractmethod
    def buscar_por_nombre(self, oferta_academica: str) -> Optional[Oferta]: pass
    @abstractmethod
    def listar_todas(self) -> List[Oferta]: pass
    @abstractmethod
    def actualizar(self, oferta: Oferta) -> None: pass
    @abstractmethod
    def eliminar(self, id_oferta: int) -> None: pass
