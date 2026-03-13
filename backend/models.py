from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    telefone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    criado_em = Column(DateTime, default=datetime.now)

    agendamentos = relationship("Agendamento", back_populates="cliente")


class Servico(Base):
    __tablename__ = "servicos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    duracao_minutos = Column(Integer, nullable=True)
    preco = Column(Float, nullable=False)
    descricao = Column(String, nullable=True)

    agendamentos = relationship("Agendamento", back_populates="servico")


class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    servico_id = Column(Integer, ForeignKey("servicos.id"), nullable=False)
    data_hora = Column(DateTime, nullable=False)
    status = Column(String, default="agendado")
    observacoes = Column(Text, nullable=True)

    cliente = relationship("Cliente", back_populates="agendamentos")
    servico = relationship("Servico", back_populates="agendamentos")