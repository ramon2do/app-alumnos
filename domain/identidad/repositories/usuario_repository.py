from abc import ABC, abstractmethod
from typing import Optional, List
from domain.identidad.entities.usuario import Usuario

class UsuarioRepository(ABC):
    @abstractmethod
    def guardar(self, usuario: Usuario) -> Usuario: pass
    @abstractmethod
    def buscar_por_id(self, id_usuario: int) -> Optional[Usuario]: pass
    @abstractmethod
    def buscar_por_correo(self, correo: str) -> Optional[Usuario]: pass
    @abstractmethod
    def listar_todos(self) -> List[Usuario]: pass
    @abstractmethod
    def actualizar(self, usuario: Usuario) -> None: pass
    @abstractmethod
    def eliminar(self, id_usuario: int) -> None: pass
