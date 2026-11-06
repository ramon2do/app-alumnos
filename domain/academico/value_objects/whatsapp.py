from dataclasses import dataclass

@dataclass(frozen=True)
class WhatsApp:
    value: str
    def __post_init__(self):
        if not str(self.value).strip():
            raise ValueError("El número de WhatsApp es obligatorio.")
