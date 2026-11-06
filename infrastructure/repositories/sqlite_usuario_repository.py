from domain.identidad.repositories.usuario_repository import UsuarioRepository
from domain.identidad.entities.usuario import Usuario
from domain.identidad.value_objects.email import Email
from domain.identidad.value_objects.rol import Rol
from infrastructure.database.db import get_db

class SQLiteUsuarioRepository(UsuarioRepository):
    def guardar(self, u: Usuario) -> Usuario:
        db = get_db()
        c = db.cursor()
        c.execute("INSERT INTO tbl_usuarios (Nombre, Correo, Contrasena, Tipo_Usuario, Estatus) VALUES (?, ?, ?, ?, ?)", (u.nombre, u.correo.value, u.contrasena_hash, u.tipo_usuario.value, u.estatus))
        db.commit()
        u.id = c.lastrowid
        return u
    def buscar_por_correo(self, correo: str):
        row = get_db().execute("SELECT * FROM tbl_usuarios WHERE Correo = ?", (correo,)).fetchone()
        return Usuario(row['Id'], row['Nombre'], Email(row['Correo']), row['Contrasena'], Rol(row['Tipo_Usuario']), row['Estatus']) if row else None
    def buscar_por_id(self, id_usuario: int): pass
    def listar_todos(self): pass
    def actualizar(self, usuario: Usuario): pass
    def eliminar(self, id_usuario: int): pass
