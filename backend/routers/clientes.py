from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models , schemas

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.get('/',response_model=list[schemas.ClienteResponse])
def listar_clientes(db:Session=Depends(get_db)):
    return db.query(models.Cliente).all()

@router.post('/' , response_model=schemas.ClienteResponse)
def criar_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = models.Cliente(**cliente.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente