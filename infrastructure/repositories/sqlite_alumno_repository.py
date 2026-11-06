from domain.academico.repositories.alumno_repository import AlumnoRepository
from domain.academico.entities.alumno import Alumno
from domain.identidad.value_objects.email import Email
from domain.academico.value_objects.whatsapp import WhatsApp
from infrastructure.database.db import get_db

class SQLiteAlumnoRepository(AlumnoRepository):
    def guardar(self, a: Alumno) -> Alumno:
        db = get_db()
        c = db.cursor()
        c.execute("INSERT INTO tbl_alumnos (Tipo_Cedula, Nro_Cedula, Nombres, Apellidos, Genero, Fecha_Nacimiento, WhatsApp, Correo, Foto_Cedula, Foto_Carnet, Id_Usuario) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (a.tipo_cedula, a.nro_cedula, a.nombres, a.apellidos, a.genero, a.fecha_nacimiento, a.whatsapp.value, a.correo.value, a.foto_cedula, a.foto_carnet, a.id_usuario))
        db.commit()
        a.id = c.lastrowid
        return a
    def buscar_por_id(self, id_alumno: int):
        row = get_db().execute("SELECT * FROM tbl_alumnos WHERE Id = ?", (id_alumno,)).fetchone()
        return Alumno(row['Id'], row['Tipo_Cedula'], row['Nro_Cedula'], row['Nombres'], row['Apellidos'], row['Genero'], row['Fecha_Nacimiento'], WhatsApp(row['WhatsApp']), Email(row['Correo']), row['Foto_Cedula'], row['Foto_Carnet'], row['Id_Usuario']) if row else None
    def buscar_por_correo(self, correo: str):
        row = get_db().execute("SELECT * FROM tbl_alumnos WHERE Correo = ?", (correo,)).fetchone()
        return Alumno(row['Id'], row['Tipo_Cedula'], row['Nro_Cedula'], row['Nombres'], row['Apellidos'], row['Genero'], row['Fecha_Nacimiento'], WhatsApp(row['WhatsApp']), Email(row['Correo']), row['Foto_Cedula'], row['Foto_Carnet'], row['Id_Usuario']) if row else None
    def buscar_por_cedula(self, tipo_cedula: str, nro_cedula: str):
        row = get_db().execute("SELECT * FROM tbl_alumnos WHERE Tipo_Cedula = ? AND Nro_Cedula = ?", (tipo_cedula, nro_cedula)).fetchone()
        return Alumno(row['Id'], row['Tipo_Cedula'], row['Nro_Cedula'], row['Nombres'], row['Apellidos'], row['Genero'], row['Fecha_Nacimiento'], WhatsApp(row['WhatsApp']), Email(row['Correo']), row['Foto_Cedula'], row['Foto_Carnet'], row['Id_Usuario']) if row else None
    def listar_todos(self):
        rows = get_db().execute("SELECT * FROM tbl_alumnos ORDER BY Id DESC").fetchall()
        return [Alumno(r['Id'], r['Tipo_Cedula'], r['Nro_Cedula'], r['Nombres'], r['Apellidos'], r['Genero'], r['Fecha_Nacimiento'], WhatsApp(r['WhatsApp']), Email(r['Correo']), r['Foto_Cedula'], r['Foto_Carnet'], r['Id_Usuario']) for r in rows]
    def actualizar(self, a: Alumno):
        db = get_db()
        db.execute("UPDATE tbl_alumnos SET Tipo_Cedula = ?, Nro_Cedula = ?, Nombres = ?, Apellidos = ?, Genero = ?, Fecha_Nacimiento = ?, WhatsApp = ?, Correo = ?, Foto_Cedula = ?, Foto_Carnet = ? WHERE Id = ?",
                   (a.tipo_cedula, a.nro_cedula, a.nombres, a.apellidos, a.genero, a.fecha_nacimiento, a.whatsapp.value, a.correo.value, a.foto_cedula, a.foto_carnet, a.id))
        db.commit()
    def eliminar(self, id_alumno: int):
        db = get_db()
        db.execute("DELETE FROM tbl_alumnos WHERE Id = ?", (id_alumno,))
        db.commit()
