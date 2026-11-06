from abc import ABC, abstractmethod
from typing import Optional, List
from domain.academico.entities.alumno import Alumno

class AlumnoRepository(ABC):
    @abstractmethod
    def guardar(self, alumno: Alumno) -> Alumno: pass
    @abstractmethod
    def buscar_por_id(self, id_alumno: int) -> Optional[Alumno]: pass
    @abstractmethod
    def buscar_por_correo(self, correo: str) -> Optional[Alumno]: pass
    @abstractmethod
    def buscar_por_cedula(self, tipo_cedula: str, nro_cedula: str) -> Optional[Alumno]: pass
    @abstractmethod
    def listar_todos(self) -> List[Alumno]: pass
    @abstractmethod
    def actualizar(self, alumno: Alumno) -> None: pass
    @abstractmethod
    def eliminar(self, id_alumno: int) -> None: pass
