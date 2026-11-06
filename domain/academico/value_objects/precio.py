from dataclasses import dataclass

@dataclass(frozen=True)
class Precio:
    valor: float
    def __post_init__(self):
        if self.valor < 0:
            raise ValueError("El precio no puede ser negativo.")
