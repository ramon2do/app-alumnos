from infrastructure.database.db import get_db

class SQLiteHorarioRepository:
    def guardar(self, horario: str):
        db = get_db()
        c = db.cursor()
        c.execute("INSERT INTO tbl_horarios (Horario) VALUES (?)", (horario,))
        db.commit()
        return c.lastrowid

    def listar_todos(self):
        return [dict(r) for r in get_db().execute("SELECT * FROM tbl_horarios ORDER BY Id DESC").fetchall()]

    def buscar_por_id(self, id_horario: int):
        row = get_db().execute("SELECT * FROM tbl_horarios WHERE Id = ?", (id_horario,)).fetchone()
        return dict(row) if row else None

    def actualizar(self, id_horario: int, horario: str):
        db = get_db()
        db.execute("UPDATE tbl_horarios SET Horario = ? WHERE Id = ?", (horario, id_horario))
        db.commit()

    def eliminar(self, id_horario: int):
        db = get_db()
        db.execute("DELETE FROM tbl_horarios WHERE Id = ?", (id_horario,))
        db.commit()


class SQLiteDuracionRepository:
    def guardar(self, duracion: str):
        db = get_db()
        c = db.cursor()
        c.execute("INSERT INTO tbl_duracion (Duracion) VALUES (?)", (duracion,))
        db.commit()
        return c.lastrowid

    def listar_todos(self):
        return [dict(r) for r in get_db().execute("SELECT * FROM tbl_duracion ORDER BY Id DESC").fetchall()]

    def buscar_por_id(self, id_duracion: int):
        row = get_db().execute("SELECT * FROM tbl_duracion WHERE Id = ?", (id_duracion,)).fetchone()
        return dict(row) if row else None

    def actualizar(self, id_duracion: int, duracion: str):
        db = get_db()
        db.execute("UPDATE tbl_duracion SET Duracion = ? WHERE Id = ?", (duracion, id_duracion))
        db.commit()

    def eliminar(self, id_duracion: int):
        db = get_db()
        db.execute("DELETE FROM tbl_duracion WHERE Id = ?", (id_duracion,))
        db.commit()


class SQLiteFrecuenciaRepository:
    def guardar(self, frecuencia: str):
        db = get_db()
        c = db.cursor()
        c.execute("INSERT INTO tbl_frecuencia (Frecuencia) VALUES (?)", (frecuencia,))
        db.commit()
        return c.lastrowid

    def listar_todos(self):
        return [dict(r) for r in get_db().execute("SELECT * FROM tbl_frecuencia ORDER BY Id DESC").fetchall()]

    def buscar_por_id(self, id_frecuencia: int):
        row = get_db().execute("SELECT * FROM tbl_frecuencia WHERE Id = ?", (id_frecuencia,)).fetchone()
        return dict(row) if row else None

    def actualizar(self, id_frecuencia: int, frecuencia: str):
        db = get_db()
        db.execute("UPDATE tbl_frecuencia SET Frecuencia = ? WHERE Id = ?", (frecuencia, id_frecuencia))
        db.commit()

    def eliminar(self, id_frecuencia: int):
        db = get_db()
        db.execute("DELETE FROM tbl_frecuencia WHERE Id = ?", (id_frecuencia,))
        db.commit()