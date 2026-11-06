from domain.academico.repositories.oferta_repository import OfertaRepository
from domain.academico.entities.oferta import Oferta
from domain.academico.value_objects.precio import Precio
from application.dtos.oferta_dto import OfertaDTO
class CrearOfertaUseCase:
    def __init__(self, oferta_repo: OfertaRepository): self.oferta_repo = oferta_repo
    def execute(self, oferta_academica, tipo, precio_en_divisas, nro_partes_cuotas, cada_una_de_en_divisas) -> OfertaDTO:
        o = self.oferta_repo.guardar(Oferta(None, oferta_academica, tipo, Precio(precio_en_divisas), nro_partes_cuotas, cada_una_de_en_divisas))
        return OfertaDTO(o.id, o.oferta_academica, o.tipo, o.precio_en_divisas.valor, o.nro_partes_cuotas, o.cada_una_de_en_divisas)
