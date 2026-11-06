from domain.academico.repositories.oferta_repository import OfertaRepository
from application.dtos.oferta_dto import OfertaDTO
class ListarOfertasUseCase:
    def __init__(self, oferta_repo: OfertaRepository): self.oferta_repo = oferta_repo
    def execute(self):
        return [OfertaDTO(o.id, o.oferta_academica, o.tipo, o.precio_en_divisas.valor, o.nro_partes_cuotas, o.cada_una_de_en_divisas) for o in self.oferta_repo.listar_todas()]
