from domain.academico.repositories.inscripcion_repository import InscripcionRepository
from domain.academico.entities.inscripcion import Inscripcion
from infrastructure.database.db import get_db

class SQLiteInscripcionRepository(InscripcionRepository):
    def guardar(self, i: Inscripcion) -> Inscripcion:
            db = get_db()
            c = db.cursor()
            c.execute("""
                INSERT INTO tbl_inscripciones 
                (Id_Alumno, Id_Oferta, Id_Profesor, Id_Horario, Id_Duracion, Id_Frecuencia, Fecha_Inscripcion) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                i.id_alumno, 
                i.id_oferta, 
                i.id_profesor, 
                i.id_horario, 
                i.id_duracion, 
                i.id_frecuencia, 
                i.fecha_inscripcion
            ))
            db.commit()
            i.id = c.lastrowid
            return i
    def actualizar(self, i: Inscripcion) -> None:
        db = get_db()
        db.execute("""
            UPDATE tbl_inscripciones 
            SET Id_Alumno = ?, Id_Oferta = ?, Id_Profesor = ?, Id_Horario = ?, Id_Duracion = ?, Id_Frecuencia = ?
            WHERE Id = ?
        """, (
            i.id_alumno, 
            i.id_oferta, 
            i.id_profesor, 
            i.id_horario, 
            i.id_duracion, 
            i.id_frecuencia, 
            i.id
        ))
        db.commit()
    def buscar_por_id(self, id: int):
        row = get_db().execute("SELECT * FROM tbl_inscripciones WHERE Id = ?", (id,)).fetchone()
        if row:
            return Inscripcion(
                id=row["Id"],
                id_alumno=row["Id_Alumno"],
                id_oferta=row["Id_Oferta"],
                id_profesor=row["Id_Profesor"],
                id_horario=row["Id_Horario"],
                id_duracion=row["Id_Duracion"],
                id_frecuencia=row["Id_Frecuencia"],
                fecha_inscripcion=row["Fecha_Inscripcion"]
            )
        return None
    def listar_todas_detalle(self):
        q = """SELECT i.Id, i.Fecha_Inscripcion, 
                      (a.Nombres || ' ' || a.Apellidos) as AlumnoNombre, 
                      (a.Tipo_Cedula || '-' || a.Nro_Cedula) as AlumnoCedula, 
                      a.Foto_Carnet as FotoCarnet,
                      o.Oferta_Academica as OfertaNombre, 
                      (p.Nombres || ' ' || p.Apellidos) as ProfesorNombre,
                      h.Horario, d.Duracion, f.Frecuencia
               FROM tbl_inscripciones i 
               JOIN tbl_alumnos a ON i.Id_Alumno = a.Id 
               JOIN tbl_ofertas_academicas o ON i.Id_Oferta = o.Id 
               JOIN tbl_profesores p ON i.Id_Profesor = p.Id 
               JOIN tbl_horarios h ON i.Id_Horario = h.Id
               JOIN tbl_duracion d ON i.Id_Duracion = d.Id
               JOIN tbl_frecuencia f ON i.Id_Frecuencia = f.Id
               ORDER BY i.Id DESC"""
        return [dict(r) for r in get_db().execute(q).fetchall()]
    def listar_por_oferta_detalle(self, id_oferta: int):
        q = """SELECT i.Id, i.Fecha_Inscripcion, 
                      (a.Nombres || ' ' || a.Apellidos) as AlumnoNombre, 
                      (a.Tipo_Cedula || '-' || a.Nro_Cedula) as AlumnoCedula, 
                      a.Correo, a.WhatsApp, a.Foto_Carnet as FotoCarnet,
                      o.Oferta_Academica as OfertaNombre, 
                      (p.Nombres || ' ' || p.Apellidos) as ProfesorNombre,
                      h.Horario, d.Duracion, f.Frecuencia
               FROM tbl_inscripciones i 
               JOIN tbl_alumnos a ON i.Id_Alumno = a.Id 
               JOIN tbl_ofertas_academicas o ON i.Id_Oferta = o.Id 
               JOIN tbl_profesores p ON i.Id_Profesor = p.Id 
               JOIN tbl_horarios h ON i.Id_Horario = h.Id
               JOIN tbl_duracion d ON i.Id_Duracion = d.Id
               JOIN tbl_frecuencia f ON i.Id_Frecuencia = f.Id
               WHERE i.Id_Oferta = ? 
               ORDER BY i.Id DESC"""
        return [dict(r) for r in get_db().execute(q, (id_oferta,)).fetchall()]
    def eliminar(self, id_inscripcion: int):
        db = get_db()
        db.execute("DELETE FROM tbl_inscripciones WHERE Id = ?", (id_inscripcion,))
        db.commit()
