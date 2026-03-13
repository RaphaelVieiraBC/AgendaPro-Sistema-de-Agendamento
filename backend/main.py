from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
from routers import clientes, servicos, agendamentos

# Cria as tabelas no banco se ainda não existirem
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AgendaPro API", version="1.0.0")

# ─── CORS ────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── ROUTERS ─────────────────────────────────────────────
app.include_router(clientes.router)
app.include_router(servicos.router)
app.include_router(agendamentos.router)

# ─── HEALTH CHECK ────────────────────────────────────────
@app.get("/")
def root():
    return {"status": "ok", "message": "AgendaPro API rodando"} 