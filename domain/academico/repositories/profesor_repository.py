from abc import ABC, abstractmethod
from typing import Optional, List
from domain.academico.entities.profesor import Profesor

class ProfesorRepository(ABC):
    @abstractmethod
    def guardar(self, profesor: Profesor) -> Profesor: pass
    @abstractmethod
    def buscar_por_id(self, id_profesor: int) -> Optional[Profesor]: pass
    @abstractmethod
    def buscar_por_correo(self, correo: str) -> Optional[Profesor]: pass
    @abstractmethod
    def buscar_por_cedula(self, tipo_cedula: str, nro_cedula: str) -> Optional[Profesor]: pass
    @abstractmethod
    def listar_todos(self) -> List[Profesor]: pass
    @abstractmethod
    def actualizar(self, profesor: Profesor) -> None: pass
    @abstractmethod
    def eliminar(self, id_profesor: int) -> None: pass
