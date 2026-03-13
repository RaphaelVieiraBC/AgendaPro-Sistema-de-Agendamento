from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(prefix="/servicos", tags=["servicos"])


@router.get("/", response_model=list[schemas.ServicoResponse])
def listar_servicos(db: Session = Depends(get_db)):
    return db.query(models.Servico).all()


@router.post("/", response_model=schemas.ServicoResponse)
def criar_servico(servico: schemas.ServicoCreate, db: Session = Depends(get_db)):
    db_servico = models.Servico(**servico.model_dump())
    db.add(db_servico)
    db.commit()
    db.refresh(db_servico)
    return db_servico