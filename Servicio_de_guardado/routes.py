from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Progreso

router = APIRouter()

# Obtener una sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/guardar")
def guardar_progreso(id_usuario: str, id_nivel: str, estado: dict, db: Session = Depends(get_db)):
    progreso = Progreso(id_usuario=id_usuario, id_nivel=id_nivel, estado=estado)
    db.add(progreso)
    db.commit()
    return {"mensaje": "Progreso guardado correctamente"}

@router.get("/recuperar")
def recuperar_progreso(id_usuario: str, id_nivel: str, db: Session = Depends(get_db)):
    progreso = db.query(Progreso).filter_by(id_usuario=id_usuario, id_nivel=id_nivel).first()
    if not progreso:
        raise HTTPException(status_code=404, detail="Progreso no encontrado")
    return progreso
