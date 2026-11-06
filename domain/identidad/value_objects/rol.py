from dataclasses import dataclass

@dataclass(frozen=True)
class Rol:
    value: str
    VALID_ROLES = {"administrador", "operador", "alumno"}

    def __post_init__(self):
        if self.value.lower() not in self.VALID_ROLES:
            raise ValueError(f"Rol inválido: {self.value}")
