from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from database import get_db
import models, schemas

router = APIRouter(prefix="/agendamentos", tags=["agendamentos"])


@router.get("/", response_model=list[schemas.AgendamentoResponse])
def listar_agendamentos(
    data: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.Agendamento)

    if data:
        try:
            data_filtro = datetime.strptime(data, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de data inválido. Use YYYY-MM-DD")

        query = query.filter(
            models.Agendamento.data_hora >= data_filtro.replace(hour=0, minute=0, second=0),
            models.Agendamento.data_hora <= data_filtro.replace(hour=23, minute=59, second=59)
        )

    agendamentos = query.all()

    resultado = []
    for ag in agendamentos:
        ag_dict = {
            "id": ag.id,
            "cliente_id": ag.cliente_id,
            "servico_id": ag.servico_id,
            "data_hora": ag.data_hora,
            "status": ag.status,
            "observacoes": ag.observacoes,
            "cliente_nome": ag.cliente.nome if ag.cliente else None,
            "servico_nome": ag.servico.nome if ag.servico else None,
        }
        resultado.append(ag_dict)

    return resultado


@router.post("/", response_model=schemas.AgendamentoResponse)
def criar_agendamento(agendamento: schemas.AgendamentoCreate, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(models.Cliente.id == agendamento.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    servico = db.query(models.Servico).filter(models.Servico.id == agendamento.servico_id).first()
    if not servico:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")

    db_agendamento = models.Agendamento(**agendamento.model_dump())
    db.add(db_agendamento)
    db.commit()
    db.refresh(db_agendamento)

    return {
        "id": db_agendamento.id,
        "cliente_id": db_agendamento.cliente_id,
        "servico_id": db_agendamento.servico_id,
        "data_hora": db_agendamento.data_hora,
        "status": db_agendamento.status,
        "observacoes": db_agendamento.observacoes,
        "cliente_nome": cliente.nome,
        "servico_nome": servico.nome,
    }


@router.patch("/{agendamento_id}/cancelar", response_model=schemas.AgendamentoResponse)
def cancelar_agendamento(agendamento_id: int, db: Session = Depends(get_db)):
    agendamento = db.query(models.Agendamento).filter(models.Agendamento.id == agendamento_id).first()

    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    if agendamento.status == "cancelado":
        raise HTTPException(status_code=400, detail="Agendamento já está cancelado")

    agendamento.status = "cancelado"
    db.commit()
    db.refresh(agendamento)

    return {
        "id": agendamento.id,
        "cliente_id": agendamento.cliente_id,
        "servico_id": agendamento.servico_id,
        "data_hora": agendamento.data_hora,
        "status": agendamento.status,
        "observacoes": agendamento.observacoes,
        "cliente_nome": agendamento.cliente.nome if agendamento.cliente else None,
        "servico_nome": agendamento.servico.nome if agendamento.servico else None,
    }