from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class DomainEvent:
    occurred_on: datetime = field(default_factory=datetime.now, init=False)
