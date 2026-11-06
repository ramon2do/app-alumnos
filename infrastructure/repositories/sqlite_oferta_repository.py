from domain.academico.repositories.oferta_repository import OfertaRepository
from domain.academico.entities.oferta import Oferta
from domain.academico.value_objects.precio import Precio
from infrastructure.database.db import get_db

class SQLiteOfertaRepository(OfertaRepository):
    def guardar(self, o: Oferta) -> Oferta:
        db = get_db()
        c = db.cursor()
        c.execute("INSERT INTO tbl_ofertas_academicas (Oferta_Academica, Tipo, Precio_en_Divisas, NroPartesCuotas, CadaUnaDe_En_divisas) VALUES (?, ?, ?, ?, ?)",
                  (o.oferta_academica, o.tipo, o.precio_en_divisas.valor, o.nro_partes_cuotas, o.cada_una_de_en_divisas))
        db.commit()
        o.id = c.lastrowid
        return o
    def buscar_por_id(self, id_oferta: int):
        row = get_db().execute("SELECT * FROM tbl_ofertas_academicas WHERE Id = ?", (id_oferta,)).fetchone()
        return Oferta(row['Id'], row['Oferta_Academica'], row['Tipo'], Precio(row['Precio_en_Divisas']), row['NroPartesCuotas'], row['CadaUnaDe_En_divisas']) if row else None
    def buscar_por_nombre(self, oferta_academica: str): pass
    def listar_todas(self):
        rows = get_db().execute("SELECT * FROM tbl_ofertas_academicas ORDER BY Id DESC").fetchall()
        return [Oferta(r['Id'], r['Oferta_Academica'], r['Tipo'], Precio(r['Precio_en_Divisas']), r['NroPartesCuotas'], r['CadaUnaDe_En_divisas']) for r in rows]
    def actualizar(self, o: Oferta):
        db = get_db()
        db.execute("UPDATE tbl_ofertas_academicas SET Oferta_Academica = ?, Tipo = ?, Precio_en_Divisas = ?, NroPartesCuotas = ?, CadaUnaDe_En_divisas = ? WHERE Id = ?",
                   (o.oferta_academica, o.tipo, o.precio_en_divisas.valor, o.nro_partes_cuotas, o.cada_una_de_en_divisas, o.id))
        db.commit()
    def eliminar(self, id_oferta: int):
        db = get_db()
        db.execute("DELETE FROM tbl_ofertas_academicas WHERE Id = ?", (id_oferta,))
        db.commit()
