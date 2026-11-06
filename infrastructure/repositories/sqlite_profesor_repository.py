from domain.academico.repositories.profesor_repository import ProfesorRepository
from domain.academico.entities.profesor import Profesor
from domain.identidad.value_objects.email import Email
from domain.academico.value_objects.whatsapp import WhatsApp
from infrastructure.database.db import get_db

class SQLiteProfesorRepository(ProfesorRepository):
    def guardar(self, p: Profesor) -> Profesor:
        db = get_db()
        c = db.cursor()
        c.execute("INSERT INTO tbl_profesores (Tipo_Cedula, Nro_Cedula, Nombres, Apellidos, Genero, Fecha_Nacimiento, Area_Conocimiento, WhatsApp, Correo, Foto_Cedula, Foto_Carnet) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (p.tipo_cedula, p.nro_cedula, p.nombres, p.apellidos, p.genero, p.fecha_nacimiento, p.area_conocimiento, p.whatsapp.value, p.correo.value, p.foto_cedula, p.foto_carnet))
        db.commit()
        p.id = c.lastrowid
        return p
    def buscar_por_id(self, id_profesor: int):
        row = get_db().execute("SELECT * FROM tbl_profesores WHERE Id = ?", (id_profesor,)).fetchone()
        return Profesor(row['Id'], row['Tipo_Cedula'], row['Nro_Cedula'], row['Nombres'], row['Apellidos'], row['Genero'], row['Fecha_Nacimiento'], row['Area_Conocimiento'], WhatsApp(row['WhatsApp']), Email(row['Correo']), row['Foto_Cedula'], row['Foto_Carnet']) if row else None
    def buscar_por_correo(self, correo: str): pass
    def buscar_por_cedula(self, tipo_cedula: str, nro_cedula: str):
        row = get_db().execute("SELECT * FROM tbl_profesores WHERE Tipo_Cedula = ? AND Nro_Cedula = ?", (tipo_cedula, nro_cedula)).fetchone()
        return Profesor(row['Id'], row['Tipo_Cedula'], row['Nro_Cedula'], row['Nombres'], row['Apellidos'], row['Genero'], row['Fecha_Nacimiento'], row['Area_Conocimiento'], WhatsApp(row['WhatsApp']), Email(row['Correo']), row['Foto_Cedula'], row['Foto_Carnet']) if row else None
    def listar_todos(self):
        rows = get_db().execute("SELECT * FROM tbl_profesores ORDER BY Id DESC").fetchall()
        return [Profesor(r['Id'], r['Tipo_Cedula'], r['Nro_Cedula'], r['Nombres'], r['Apellidos'], r['Genero'], r['Fecha_Nacimiento'], r['Area_Conocimiento'], WhatsApp(r['WhatsApp']), Email(r['Correo']), r['Foto_Cedula'], r['Foto_Carnet']) for r in rows]
    def actualizar(self, p: Profesor):
        db = get_db()
        db.execute("UPDATE tbl_profesores SET Tipo_Cedula = ?, Nro_Cedula = ?, Nombres = ?, Apellidos = ?, Genero = ?, Fecha_Nacimiento = ?, Area_Conocimiento = ?, WhatsApp = ?, Correo = ?, Foto_Cedula = ?, Foto_Carnet = ? WHERE Id = ?",
                   (p.tipo_cedula, p.nro_cedula, p.nombres, p.apellidos, p.genero, p.fecha_nacimiento, p.area_conocimiento, p.whatsapp.value, p.correo.value, p.foto_cedula, p.foto_carnet, p.id))
        db.commit()
    def eliminar(self, id_profesor: int):
        db = get_db()
        db.execute("DELETE FROM tbl_profesores WHERE Id = ?", (id_profesor,))
        db.commit()
