from dataclasses import dataclass, field
from typing import Optional, Dict, List

@dataclass
class Cliente:
    nome: str
    email: str
    tipo_servico: str
    status: str = "Novo"
    # Outros campos podem ser adicionados conforme necessário

@dataclass
class Task:
    id: Optional[str]
    nome: str
    custom_fields: Dict[str, str] = field(default_factory=dict)
    assignees: List[str] = field(default_factory=list)
    status: Optional[str] = None
    # Outros campos relevantes 