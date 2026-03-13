from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ─── CLIENTE ────────────────────────────────────────────
class ClienteBase(BaseModel):
    nome:str
    telefone: Optional[str]=None
    email: Optional[str]=None

class ClienteCreate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True


# ─── SERVIÇO ─────────────────────────────────────────────
class ServicoBase(BaseModel):
    nome:str
    duracao_minutos:Optional[int]=None
    preco:float
    descricao:Optional[str]=None

class ServicoCreate(ServicoBase):
    pass

class ServicoResponse(ServicoBase):
    id: int

    class Config:
        from_attributes = True

# ─── AGENDAMENTO ─────────────────────────────────────────

class AgendamentoBase(BaseModel):
    cliente_id: int
    servico_id: int
    data_hora: datetime
    observacoes: Optional[str] = None


class AgendamentoCreate(AgendamentoBase):
    pass

class AgendamentoResponse(AgendamentoBase):
    id: int
    status: str
    cliente_nome: Optional[str] = None
    servico_nome: Optional[str] = None

    class Config:
        from_attributes = True